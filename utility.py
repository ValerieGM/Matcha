import re
from passlib.hash import sha256_crypt
from flask import redirect, request, session, flash, url_for, render_template
from flask_mail import Message
from functools import wraps
from database import *

##################################
# CHECK FOR // IN REDIRECT LINES #
##################################

# Global
def session_starter(username):
    # needs completion with picture and geolocation etc
    user = find_user(username)

    session['LoggedIn'] = True
    session['UserName'] = user['UserName']
    session['FirstName'] = user['FirstName']
    session['SurName'] = user['SurName']
    session['Email'] = user['Email']
    session['Gender'] = user['Gender']
    session['SexualPreference'] = user['SexualPreference']
    session['Age'] = user['Age']
    session['Biography'] = user['Biography']


# Registration
def validate_registration(method, mail):
    if method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if (username.isalpha() == False or firstname.isalpha() == False or surname.isalpha() == False):
            flash('Letters Only Naming Convention', 'danger')
            return redirect(url_for('register'))
        
        if (username.len() > 8):
            flash('Username Needs to Be No More Than 8 Characters', 'danger')
            return redirect(url_for('register'))

        if (password.len() > 8):
            flash('Passwords Nees to Be No More Than 8 Characters', 'danger')
            return redirect(url_for('register'))
        elif (password.isalpha() == True or password.isnumeric() == True):
            flash('Password Need To Be Alphanumeric', 'danger')
            return redirect(url_for('register'))
        elif (password.isalnum() == True):
            if password != confirm:
                flash('Passwords Do Not Match', 'danger')
                return redirect(url_for('register'))
            else:
                password = sha256_crypt.encrypt(password)

        # database insertion
        registration_insert(username, firstname, surname, email, password)

        # Verification Email
        msg = Message('Verification', sender='smts65142@gmail.com', recipients=[email])
        mess = 'Thanks for signing up! Your account has been created, ' \
               'you can login with the following credentials after you have ' \
               'activated your account by pressing the url below. Please click ' \
               'this link to activate your account: http://127.0.0.1:5000/verify?username=' + username
        msg.body = mess
        mail.send(msg)

        flash('Email Verification Sent', 'success')
        return redirect(url_for('login'))


def verify_registration(method):
    if method == 'POST':
        username = request.args.get('username')
        verify_insert(username)
        flash('Account Verified. You May Now Login.', 'success')
        return redirect(url_for('login'))


# Forgot Password
def forgot(method, mail):
    if method == 'POST':
        email = request.form['recovery_email']
        user = find_user_by_email(email)

        if user['Email'] == email:
            msg = Message('Password Reminder', sender='smts65142@gmail.com', recipients=[email])
            mess = 'Oops!! ' \
                   '' \
                   'You Seem To have forgotten your password. For security reasons we ' \
                   'request you change it on this link: ' \
                   'http://127.0.0.1:5000/change_password?email=' + email
            msg.body = mess
            mail.send(msg)
            flash("Further instructions Have Been Sent To Your Email", "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid Email Address", "danger")
            return redirect(url_for('forgot_password'))


# Change Password
def change(method):
    if method == 'POST':
        email = request.args.get('email')
        password = request.form['password']
        new_password = request.form['confirm']

        if str(password).isalnum():
            if password != new_password:
                flash('Passwords Do Not Match', 'danger')
                return redirect(url_for('change_password'))
            else:
                encrypted_password = sha256_crypt.encrypt(password)
                password_change(email, encrypted_password)
                flash("Password Changed. Please Log In Again", "success")
                return redirect(url_for('login'))
        else:
            flash("Password Must Be Alphanumeric", "danger")
            return redirect(url_for('change_password'))
    return redirect(url_for('change_password')) 


# Login
def define_login(method):
    if method == 'POST':
        username = request.form['username']
        temp_password = request.form['password']

        user = find_user(username)

        if user:
            password = user['Password']
            verified = user['AccountVerification']
            if verified == '1':
                if sha256_crypt.verify(temp_password,password):
                    if user['ProfileCompletion'] == '0':
                        flash('Please Fill Out Your Profile To Continue', 'success')
                        return redirect(url_for('dashboard'))
                    else:
                        online_status(username)
                        session_starter(username)
                        flash('Welcome' + user['FirstName'], 'success')
                        return redirect(url_for('profile'))
                else:
                    flash("Passwords Do Not Match", "danger")
                    return redirect(url_for('login'))
            else:
                flash("Please Verify Your Account In The Email Sent To You", "danger")
                return redirect(url_for('login'))
        else:
            flash("Username Does Not Exist", "danger")
            return redirect(url_for("login"))
    return redirect(url_for('login'))


# Dashboard
def update(method):
    return redirect(url_for('dashboard'))


# Is Logged In
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'LoggedIn' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised Access, Please Login Or Register', 'danger')
            return redirect(url_for('login'))
    return wrap