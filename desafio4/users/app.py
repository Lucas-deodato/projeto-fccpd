from flask import Flask, jsonify

app = Flask(__name__)

import os
API_KEY = os.environ.get('API_KEY', 'changeme')

def require_api_key():
    from flask import request, abort
    key = request.headers.get('X-API-Key')
    if not key or key != API_KEY:
        abort(401)

@app.route('/users')
def users():
    require_api_key()
    data = [
        {"id": 1, "name": "Alice", "active_since": "2023-01-10"},
        {"id": 2, "name": "Bob", "active_since": "2024-02-05"}
    ]
    return jsonify(data)

@app.route('/openapi.yaml')
def openapi():
    from flask import send_file
    return send_file('openapi/users.yaml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

