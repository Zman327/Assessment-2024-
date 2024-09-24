from flask import Flask, render_template, request, redirect, url_for, session, flash, session   # noqa:
import sqlite3
import hashlib
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Define the folder to save uploaded images to ensure that images are stored
# in the correct place
UPLOAD_FOLDER = 'Static/Images/profile'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Function to check allowed file extensions to maintain data integrity
# and ensure user does not insert wrong files types e.g ZIPs
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   # noqa:


app = Flask(__name__, template_folder='templates', static_folder='Static')
app.secret_key = os.urandom(24)  # Secret key for session management
# Using os.urandom(24) generates a 24-byte random key,
# ensuring that the secret key is unique and unpredictable.

# Set the upload folder in app configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def do_sql(sql, params=None):
    conn = sqlite3.connect('Fencing_hub.db')
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


@app.route('/register', methods=['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Validate that the username and email do not exceed 20 characters to
        # ensure data consistency and database integrity
        if len(username) > 20:
            flash("Username must not exceed 20 characters!", "error")
            return redirect(url_for('registerpage'))

        if len(email) > 30:
            flash("Username must not exceed 20 characters!", "error")
            return redirect(url_for('registerpage'))

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template('register.html')

        # Securely hash the password using SHA-256 to store it safely, used
        # SHA-256 as it converts it into a fixed-size string
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            do_sql("INSERT INTO Login (username, email, password) VALUES (?, ?, ?)",  # noqa:
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
        # Retrieve form data from the website
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA256 due to its ability to convert text
        # into a fixed-size string that doesn't reveal the original text
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Query the database to find the user to ensure that username AND
        # password are both correct
        user = do_sql("SELECT * FROM Login WHERE username = ? AND password = ?", (username, hashed_password))  # noqa:

        # Check if user exists
        if user:
            # Store username in session, this is so that if user is to open
            # page again, it will save the session
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('homepage'))
        else:
            # Display error for when username does not exist in database
            flash("Incorrect username or password.", "error")
            return render_template('login.html')

    return render_template('login.html')


@app.route('/forgot-password')
def forgotpasswordpage():
    return render_template('forgot_password.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('homepage'))


def get_fencers_with_images():
    fencers = do_sql("SELECT * FROM Male_Fencers")
    fencers_with_images = []
    for fencer in fencers:
        fencer_with_image = list(fencer)
        if fencer_with_image[3]:  # Check if fencer_photo is not None
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
    events = do_sql("SELECT event_id, event_name, start_date, gender, location, weapon FROM Events ORDER BY start_date ASC")  # noqa:
    return render_template('calendar.html', events=events)


@app.route('/rankings')
def rankingpage():
    Mepee = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC")  # noqa:
    Mfoil = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC")  # noqa:
    Msabre = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC")  # noqa:
    Fepee = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC")  # noqa:
    Ffoil = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC")  # noqa:
    Fsabre = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC")  # noqa:
    male_fencers = get_fencers_with_images()
    return render_template('rankings.html', Fepee=Fepee, Ffoil=Ffoil, Fsabre=Fsabre, Mepee=Mepee, Mfoil=Mfoil, Msabre=Msabre, male_fencers=male_fencers)  # noqa:


@app.route('/stories')
def storiespage():
    Mepee = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC LIMIT 5")   # noqa:
    Mfoil = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC LIMIT 5")  # noqa:
    Msabre = do_sql("SELECT * FROM Male_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC LIMIT 5")  # noqa:
    Fepee = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Epee' ORDER BY rank ASC LIMIT 5")  # noqa:
    Ffoil = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Foil' ORDER BY rank ASC LIMIT 5")  # noqa:
    Fsabre = do_sql("SELECT * FROM Female_Fencers WHERE weapon = 'Sabre' ORDER BY rank ASC LIMIT 5")  # noqa:
    return render_template('stories.html', Fepee=Fepee, Ffoil=Ffoil, Fsabre=Fsabre, Mepee=Mepee, Mfoil=Mfoil, Msabre=Msabre)  # noqa:


@app.route('/about_us')
def aboutuspage():
    return render_template('about_us.html')


@app.route('/privacy_policy')
def privacypage():
    return render_template('privacy-policy.html')


@app.route('/profile', methods=['GET', 'POST'])
def profilepage():
    if 'username' in session:
        username = session['username']

        if request.method == 'POST':
            new_username = request.form['username']
            new_email = request.form['email']
            new_phone = request.form['phone']
            new_address = request.form['address']

            # Handle the file upload
            if 'profile-pic' in request.files:
                file = request.files['profile-pic']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Save the file to the specified folder
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))    # noqa:
                    # Create the path to save in the database
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)    # noqa:
                    # Update the database with the new profile picture path
                    do_sql("UPDATE Login SET profile_pic = ? WHERE username = ?", (file_path, username))    # noqa:

            # Update the user's other information
            do_sql("UPDATE Login SET username = ?, email = ?, phone = ?, address = ? WHERE username = ?",    # noqa:
                   (new_username, new_email, new_phone, new_address, username))

            # Update session with new username if it was changed
            # this will make sure that the correct session is displayed
            session['username'] = new_username

            flash("Profile updated successfully!", "success")
            return redirect(url_for('homepage'))

        user_info = do_sql("SELECT username, email, phone, address, profile_pic FROM Login WHERE username = ?", (username,))    # noqa:
        if user_info:
            user_data = {
                "username": user_info[0][0],
                "email": user_info[0][1],
                "phone": user_info[0][2],
                "address": user_info[0][3],
                "profile_pic": user_info[0][4]
            }
            return render_template('profile.html', user_data=user_data)
    else:
        flash("You need to log in first!", "error")
        return redirect(url_for('loginpage'))


# testing page
@app.route('/test')
def testpage():
    return render_template('Test.html')


# 404 page to display when a page is not found
# helps re-direct users back to home page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
