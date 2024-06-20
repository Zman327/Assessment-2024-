from flask import Flask, render_template
import sqlite3
import base64

app = Flask(__name__, template_folder='templates', static_folder='Static')


def do_sql(sql):
    conn = sqlite3.connect('Fencing_hub.db')
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()  # Ensure to close the connection
    return result

def get_fencers_with_images():
    fencers = do_sql("SELECT * FROM Male_Fencers")
    fencers_with_images = []
    for fencer in fencers:
        fencer_with_image = list(fencer)
        if fencer_with_image[3]:  # Check if fencer_photo is not None
            fencer_with_image[3] = base64.b64encode(fencer_with_image[3]).decode('utf-8')  # Encode image data to base64
        fencers_with_images.append(fencer_with_image)
    return fencers_with_images

@app.route('/home')
def homepage():
    return render_template('index.html')

@app.route('/events')
def eventspage():
    return render_template('events.html')


@app.route('/about_fencing')
def aboutfencingpage():
    return render_template('about_fencing.html')

@app.route('/calendar')
def calendarpage():
    events = do_sql("SELECT * FROM Male_Events ORDER BY start_date ASC")
    return render_template('calendar.html', events=events)

@app.route('/rankings')
def rankingpage():
    Mepee = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC")
    Mfoil = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC")
    Msabre = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC")
    Fepee = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC")
    Ffoil = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC")
    Fsabre = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC")
    male_fencers = get_fencers_with_images()
    return render_template('rankings.html', Fepee=Fepee, Ffoil=Ffoil, Fsabre=Fsabre, Mepee=Mepee, Mfoil=Mfoil, Msabre=Msabre, male_fencers=male_fencers)

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/register')
def registerpage():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)