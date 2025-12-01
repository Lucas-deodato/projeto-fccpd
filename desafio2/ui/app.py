from flask import Flask, render_template_string, request, redirect
import os

try:
  import psycopg2  # type: ignore
except Exception:  # pragma: no cover - linter/IDE fallback
  psycopg2 = None

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', '5432'))
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'examplepass')

TEMPLATE = '''
<html>
<head><title>Desafio2 - Notes UI</title></head>
<body>
  <h1>Notes</h1>
  <form method="post">
    <input name="text" placeholder="nova nota" />
    <button type="submit">Adicionar</button>
  </form>
  <ul>
  {% for id, text in notes %}
    <li>{{id}} - {{text}}</li>
  {% endfor %}
  </ul>
</body>
</html>
'''

def get_conn():
  if psycopg2 is None:
    raise RuntimeError(
      "psycopg2 is not installed in this environment.\n"
      "Install with: pip install -r ui/requirements.txt or run the UI via Docker where deps are installed."
    )
  return psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO notes(text) VALUES(%s)', (text,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')

    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, text FROM notes ORDER BY id')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(TEMPLATE, notes=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
