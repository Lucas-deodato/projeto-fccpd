import requests
from flask import Flask, jsonify, Response
from flask import request as flask_request
import time
import threading

app = Flask(__name__)

USERS_URL = 'http://users:6001/users'
ORDERS_URL = 'http://orders:6002/orders'

# Simple circuit-breaker state per service
CIRCUIT = {
    'users': {'failures': 0, 'state': 'CLOSED', 'opened_at': None},
    'orders': {'failures': 0, 'state': 'CLOSED', 'opened_at': None}
}

LOCK = threading.Lock()

def is_open(name, timeout=10):
    s = CIRCUIT[name]
    if s['state'] == 'OPEN':
        # remain open for timeout seconds
        if time.time() - s['opened_at'] > timeout:
            # half-open
            s['state'] = 'HALF'
            s['failures'] = 0
            return False
        return True
    return False

def record_failure(name):
    with LOCK:
        s = CIRCUIT[name]
        s['failures'] += 1
        if s['failures'] >= 3:
            s['state'] = 'OPEN'
            s['opened_at'] = time.time()

def record_success(name):
    with LOCK:
        s = CIRCUIT[name]
        s['failures'] = 0
        s['state'] = 'CLOSED'

def call_with_retry(name, url, retries=2, backoff=0.5, timeout=3):
    if is_open(name):
        return None, 503, f'circuit_open for {name}'

    attempt = 0
    while attempt <= retries:
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                record_success(name)
                return r.content, r.status_code, r.headers.get('Content-Type','application/json')
            else:
                record_failure(name)
        except Exception:
            record_failure(name)
        attempt += 1
        time.sleep(backoff * attempt)

    return None, 502, 'upstream_error'


@app.route('/users')
def proxy_users():
    content, status, ctype = call_with_retry('users', USERS_URL)
    if content is None:
        return jsonify({'error': ctype}), status
    return Response(content, status=status, content_type=ctype)


@app.route('/orders')
def proxy_orders():
    content, status, ctype = call_with_retry('orders', ORDERS_URL)
    if content is None:
        return jsonify({'error': ctype}), status
    return Response(content, status=status, content_type=ctype)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
