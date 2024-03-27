from flask import Flask, render_template,request,Response
from llm import streamChatGPT

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/stream', methods=['POST'])
def stream():
  messages = request.get_json()
  response_stream = streamChatGPT(messages)
  return Response(response_stream, mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)