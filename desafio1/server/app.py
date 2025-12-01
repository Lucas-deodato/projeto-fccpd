from flask import Flask, jsonify

app = Flask(__name__)

# simple in-memory message store (not persistent, for demo)
MESSAGES = []

@app.route('/')
def hello():
    return jsonify({'message': 'Hello from Desafio1 Server'})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/messages', methods=['GET'])
def get_messages():
    # return all messages
    return jsonify(MESSAGES)

@app.route('/messages', methods=['POST'])
def post_message():
    from flask import request
    payload = request.get_json() or {}

    msg = {
        'from': payload.get('from', 'unknown'),
        'text': payload.get('text', ''),
        'id': payload.get('id')
    }
    MESSAGES.append(msg)
    return jsonify({'status': 'ok', 'stored': msg})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
