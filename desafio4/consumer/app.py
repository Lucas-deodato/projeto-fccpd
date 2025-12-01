import requests
from flask import Flask, jsonify

app = Flask(__name__)

import os
USERS_URL = 'http://users:5001/users'
API_KEY = os.environ.get('API_KEY', 'changeme')

@app.route('/combined')
def combined():
    r = requests.get(USERS_URL, timeout=5, headers={'X-API-Key': API_KEY})
    users = r.json()
    out = []
    for u in users:
        out.append(f"Usuário {u['name']} ativo desde {u['active_since']}")
    return jsonify(out)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
