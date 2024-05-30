from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


def do_sql(sql):
    conn = sqlite3.connect('Fencing_hub.db')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


@app.route('/events')
def aboutpage():
    x = do_sql("SELECT * FROM Male_Fencers")
    return render_template('templates/events.html', male_fencers = x)

if __name__ == "__main__":  # Last lines
    app.run(debug=True)
