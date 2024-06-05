from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='Static')


def do_sql(sql):
    conn = sqlite3.connect('Fencing_hub.db')
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()  # Ensure to close the connection
    return result


@app.route('/home')
def homepage():
    return render_template('index.html')


@app.route('/calendar')
def calendarpage():
    return render_template('calendar.html')


@app.route('/events')
def eventspage():
    return render_template('events.html')


@app.route('/about_fencing')
def aboutfencingpage():
    return render_template('about_fencing.html')


@app.route('/rankings')
def rankingpage():
    Mepee = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC")
    Mfoil = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC")
    Msabre = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC")
    Fepee = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC")
    Ffoil = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC")
    Fsabre = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC")
    return render_template('rankings.html', Fepee=Fepee, Ffoil=Ffoil, Fsabre=Fsabre, Mepee=Mepee, Mfoil=Mfoil, Msabre=Msabre)


if __name__ == "__main__":
    app.run(debug=True)
