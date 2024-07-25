from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import base64
import json
import hashlib  # For password hashing
import os

app = Flask(__name__, template_folder='templates', static_folder='Static')
app.secret_key = os.urandom(24)  # Secret key for session management


def do_sql(sql, params=None):
    conn = sqlite3.connect('Fencing_hub.db')
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    result = cur.fetchall()
    conn.commit()  # Ensure changes are committed
    conn.close()  # Ensure to close the connection
    return result


@app.route('/register', methods=['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template('register.html')

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert into the database
        try:
            do_sql("INSERT INTO Login (username, email, password) VALUES (?, ?, ?)",
                   (username, email, hashed_password))
            flash("Registration successful!", "success")
            return redirect(url_for('loginpage'))
        except sqlite3.IntegrityError:
            flash("Username or Email already exists!", "error")
            return render_template('register.html')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = do_sql("SELECT * FROM Login WHERE username = ? AND password = ?", (username, hashed_password))

        if user:
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('homepage'))
        else:
            flash("Invalid username or password!", "error")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('loginpage'))


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
    events = do_sql("SELECT start_date, event_name FROM Male_Events ORDER BY start_date ASC")
    # Convert the event dates to strings for JSON serialization
    events = [{'date': event[0], 'title': event[1]} for event in events]
    return render_template('calendar.html', events=json.dumps(events))


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


@app.route('/stories')
def storiespage():
    return render_template('stories.html')


@app.route('/about_us')
def aboutuspage():
    return render_template('about_us.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)


from flask import render_template