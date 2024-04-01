from flask import Flask, request, redirect, url_for, render_template, session,Response
import time, json, os

from llm import streamChatGPT
from config import getConfig

from db import update_chat_entry,list_chat_history,get_chat_messages

try:
    secret_key=os.environ("SECRET_KEY")
except:
    from dotenv import load_dotenv
    load_dotenv()
    secret_key=os.getenv("SECRET_KEY")


app = Flask(__name__)
app.secret_key = secret_key

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
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    config = getConfig()
    if request.method == 'POST':
        config['username'] = request.form.get('username')
        config['chat_started'] = request.form.get('chat_started')
        config['messages'] = json.loads(get_chat_messages(config['username'], config['chat_started']))
        return render_template('chat.html', config=config)
    else:
        config['username'] = session['username']
        config['chat_started'] = int(time.time())
        return render_template('chat.html', config=config)


@app.route('/stream', methods=['POST'])
@login_required
def stream():
    messages = request.get_json()
    response_stream = streamChatGPT(messages)
    return Response(response_stream, mimetype='text/event-stream')

@app.route('/save_chat', methods=['POST'])
@login_required
def save_chat():
    username = request.form.get('username')
    chat_started = request.form.get('chat_started')
    messages = request.form.get('messages')
    
    update_result = update_chat_entry(username, chat_started, messages)

    print (list_chat_history)

    if update_result:
        return 'Chat aktualisiert!'
    else:
        return 'Neuer Chat erstellt!'

@app.route('/list_chat_history', methods=['GET'])
@login_required
def list_chat_history_endpoint():
    chat_history = list_chat_history()
    return render_template('chat_history.html',chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)