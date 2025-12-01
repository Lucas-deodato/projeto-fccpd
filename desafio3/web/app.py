import os
from flask import Flask, jsonify
import time

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
CACHE_HOST = os.environ.get('CACHE_HOST', 'cache')

@app.route('/info')
def info():
    return jsonify({'db': DB_HOST, 'cache': CACHE_HOST, 'time': time.time()})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
