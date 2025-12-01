import requests
import time
import os

SERVER_HOST = os.environ.get('SERVER_HOST', 'desafio1_server')
SERVER_PORT = os.environ.get('SERVER_PORT', '8080')
URL = f'http://{SERVER_HOST}:{SERVER_PORT}/'

def main():
    import uuid
    client_id = os.environ.get('CLIENT_ID', f'client-{uuid.uuid4().hex[:6]}')
    print('Client starting, id=', client_id, 'will poll', URL, flush=True)
    counter = 0
    while True:
        try:
            payload = {'from': client_id, 'text': f'hello {counter}', 'id': counter}
            try:
                rpost = requests.post(URL + 'messages', json=payload, timeout=5)
                print('posted:', rpost.json(), flush=True)
            except Exception as e:
                print('post error:', e, flush=True)

            r = requests.get(URL + 'messages', timeout=5)
            print('messages:', r.json(), flush=True)
        except Exception as e:
            print('error:', e, flush=True)
        counter += 1
        time.sleep(5)

if __name__ == '__main__':
    main()
