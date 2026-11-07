import os
from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

REPO_URL = "https://github.com/Jebachu/viikko2-visitor-counter"

# täydennä testin jälkeen
REBOOT_RESULT = "Not tested yet."


def get_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )


def increment_and_get_visits():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Laskurin kasvatus SQL:ssä
        cursor.execute("UPDATE counter SET visits = visits + 1 WHERE id = 1")
        cursor.execute("SELECT visits FROM counter WHERE id = 1")
        visits = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return visits
    finally:
        conn.close()


PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Visitor Counter - Week 2</title>
  <style>
    body {
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      font-family: sans-serif;
      line-height: 1.6;
      background: #121820;
      color: #d8e2ec;
    }
    h1, h2 { color: #4fc3f7; }
    a { color: #4fc3f7; }
    .counter {
      text-align: center;
      background: #1c2733;
      border-radius: 12px;
      padding: 24px;
      margin: 24px 0;
    }
    .counter .number {
      font-size: 4rem;
      font-weight: bold;
      color: #4fc3f7;
    }
    code { background: #1c2733; padding: 2px 6px; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Visitor Counter</h1>
  <p>Welcome to my Week 2 project!</p>

  <div class="counter">
    <div>This page has been loaded</div>
    <div class="number">{{ visits }}</div>
    <div>times</div>
  </div>

  <h2>Which database is used?</h2>
  <p>MySQL 8.4, running on the same Ubuntu virtual machine in CSC cPouta.</p>

  <h2>How is the counter stored?</h2>
  <p>The database has a table called <code>counter</code> with one row.
     Every time the page loads, the Python app adds 1 to that number
     in the database and shows the new value.
     The number is saved on disk in the database, not in the memory
     of the Python program, so it is not lost when the app restarts.</p>

  <h2>Restart test result</h2>
  <p>{{ reboot_result }}</p>

  <h2>How does it work?</h2>
  <p>Browser &rarr; Nginx (port 80) &rarr; Gunicorn + Flask (only on 127.0.0.1)
     &rarr; MySQL. Nginx, the Python app (systemd service) and MySQL
     all start automatically after a reboot.</p>

  <h2>Source code</h2>
  <p><a href="{{ repo_url }}">{{ repo_url }}</a></p>

  <h2>Week 1</h2>
  <p><a href="/">Go to my Week 1 page</a></p>
</body>
</html>
"""


@app.route("/")
def index():
    visits = increment_and_get_visits()
    return render_template_string(
        PAGE, visits=visits, reboot_result=REBOOT_RESULT, repo_url=REPO_URL
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
