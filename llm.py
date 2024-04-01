import os,json
from openai import OpenAI

try:
    api_key=os.environ["OPENAI_API_KEY"]
    together_api_key=os.environ["TOGETHER_API_KEY"]
except:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key=os.getenv("OPENAI_API_KEY")
        together_api_key=os.getenv("TOGETHER_API_KEY")
    except ImportError:
        print ('dotenv is not installed')

mode = "together"

if mode =='together':
    model = "meta-llama/Llama-2-70b-chat-hf"
    client = OpenAI(
        api_key=together_api_key,
        base_url='https://api.together.xyz/v1',
    )
else:
    client = OpenAI(api_key=api_key)
    model = "gpt-3.5-turbo"


def askChatGPT(prompt, system_message='', model='gpt-3.5-turbo'):
    if system_message == '':
        system_message = "Du bist ein hilfreicher Assistent"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def streamChatGPT(messages, model=model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    for line in response:
        if line.choices[0].delta.content != None and line.choices[0].delta.content !="" :
            yield line.choices[0].delta.content.encode('utf-8')
        else:
            if line.choices[0].finish_reason =='eos' or line.choices[0].finish_reason =='stop':
                try:
                    yield "###STOP###" + json.dumps(line.usage)
                except:
                    pass