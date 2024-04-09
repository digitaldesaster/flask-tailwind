from flask import Flask, request, redirect, url_for, render_template, session,Response
import time, json, os

from llm import streamChatGPT
from config import getConfig

from db import update_chat_entry,list_chat_history,get_chat_messages,delete_db_table,add_prompt_database,list_prompts_database,get_prompt_by_id

try:
    secret_key=os.environ["SECRET_KEY"]
except:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        secret_key=os.getenv("SECRET_KEY")
    except ImportError:
        print ('dotenv is not installed')
        

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
@app.route('/prompt/<prompt_id>')
@app.route('/', methods=['GET', 'POST'])
@login_required
def index(prompt_id=None):
    config = getConfig()
        
    if request.method == 'POST':
        config['username'] = request.form.get('username')
        config['chat_started'] = request.form.get('chat_started')
        # try:
        #     rendered = request.form.get('chat_started')
        #     if rendered =='True':
        #         rendered=True
        # except:
        #     rendered = False
        config['messages'] = json.loads(get_chat_messages(config['username'], config['chat_started']))
        #if (rendered):
        #   return render_template('chat_messages_rendered.html', config=config)
        return render_template('chat.html', config=config)
    else:
        if prompt_id:
            prompt = get_prompt_by_id(prompt_id)
            
            config['messages']=[]
            config['messages'].append({'role':'system_message','content':prompt['system_message']})
            config['messages'].append({'role':'user','content':prompt['prompt']})
            config['use_prompt_template']='True'
      
        config['username'] = session['username']
        config['chat_started'] = int(time.time())
        return render_template('chat.html', config=config)


@app.route('/stream', methods=['POST'])
@login_required
def stream():
    data = request.get_json()
    print (data)
    response_stream = streamChatGPT(data['messages'],data['model'])
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

@app.route('/load_ui/<template>')
def load_ui(template):
    return render_template(template)

@app.route('/show_prompts', methods=['GET'])
@login_required
def show_prompts():
    prompts = list_prompts_database()
    return render_template('show_prompts.html', prompts=prompts)

@app.route('/test')
def test():
    return render_template('flowbite.html')

@app.route('/create_prompt')
def create_prompt():
    return render_template('create_prompt.html')

@app.route('/add_prompt', methods=['POST'])
def add_prompt():
    data = request.get_json()
    name = data.get('_name')
    system_message = data.get('_system_message')
    prompt = data.get('_prompt')

    add_prompt_database(name, system_message, prompt)
    return ({'status': 'ok', 'message': 'Prompt added!'})

@app.route('/delete/<table>')
def delete_table(table):
    delete_db_table(table)
    return {'status':'ok','message':'history deleted!'}


@app.route('/modal')
def modal():
    return render_template('test_modal.html')

if __name__ == '__main__':
    app.run(debug=True)