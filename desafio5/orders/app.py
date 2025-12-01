from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/orders')
def orders():
    return jsonify([
        {"id": 100, "user_id": 1, "total": 29.9},
        {"id": 101, "user_id": 2, "total": 99.0}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002)
