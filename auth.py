from flask import Blueprint, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
# Import database functions from db.py
from db import ensure_users_table_exists,get_user,add_user

my_auth = Blueprint('my_auth', __name__)

WHITELISTED_USERNAMES = {'alexander.fillips@gmail.com', 'nina.fillips@web.de'}

@my_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = get_user(username)
        if user_data:
            if check_password_hash(user_data[1], password):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return render_template('login.html', status='Wrong Password!')
        else:
            if username in WHITELISTED_USERNAMES:
                password_hash = generate_password_hash(password)
                add_user(username,password_hash)
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return render_template('login.html', status="User not whitelisted!")
    return render_template('login.html')

@my_auth.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))

ensure_users_table_exists()
