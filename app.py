import os
from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)


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
  <title>Visitor counter — Week 2</title>
</head>
<body>
  <h1>Visitor counter</h1>
  <p>This page has been loaded <strong>{{ visits }}</strong> times.</p>
</body>
</html>
"""


@app.route("/")
def index():
    visits = increment_and_get_visits()
    return render_template_string(PAGE, visits=visits)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
