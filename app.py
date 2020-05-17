from flask import Flask, render_template
from flask_mail import Mail
from utility import *

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='smts65142@gmail.com',
    MAIL_PASSWORD='wethinkcode'
    )
app.config['SECRET_KEY'] = 'secret_key'
mail = Mail(app)


# Index
@app.route('/')
def index():
    return render_template('index.html')


# Home
@app.route('/index')
def home():
    return render_template('index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    validate_registration(request.method, mail)
    return render_template('register.html')


# Verify
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    verify_registration(request.method)
    return render_template('verify.html')


# Forgot Password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    forgot(request.method, mail)
    return render_template('forgot_password.html')


# Change Password
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    change(request.method)
    return render_template('change_password.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    define_login(request.method)
    return render_template('login.html')



# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    # change to offline and update last seen
    # secret key for sessions (look up)
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# App Run
if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True)