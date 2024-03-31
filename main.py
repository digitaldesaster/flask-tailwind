from flask import Flask, request, redirect, url_for, render_template, session,Response

from llm import streamChatGPT
from config import getConfig

app = Flask(__name__)
app.secret_key = 'asdlfakjsADSFLl23423400asdf_adf234234'

from flask import Flask
from auth import my_auth  # Import the Blueprint you defined

app.register_blueprint(my_auth, url_prefix='/auth')  # R

from functools import wraps
from flask import session, redirect, url_for

# Define a decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('my_auth.login'))  # Redirect to the login page
        return f(*args, **kwargs)
    return decorated_function

# Apply the login_required decorator to routes that require authentication
@app.route('/')
@login_required
def index():
    print(session['username'])
    return render_template('chat.html', config=getConfig())

@app.route('/stream', methods=['POST'])
@login_required
def stream():
    messages = request.get_json()
    response_stream = streamChatGPT(messages)
    return Response(response_stream, mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)