import os,json
from openai import OpenAI
import anthropic

from dotenv import load_dotenv
load_dotenv()
openai_api_key=os.getenv("OPENAI_API_KEY")
together_api_key=os.getenv("TOGETHER_API_KEY")
anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")

mode = "anthropic"

if mode =='together':
    model = "meta-llama/Llama-2-70b-chat-hf"
    #model = "mistralai/Mixtral-8x7B-v0.1"
    client = OpenAI(
        api_key=together_api_key,
        base_url='https://api.together.xyz/v1',
    )
elif mode == 'anthropic':
  model = "claude-3-haiku-20240307"
  client = anthropic.Anthropic(api_key=anthropic_api_key)
else:
    client = OpenAI(api_key=openai_api_key)
    model = "gpt-3.5-turbo"


def askChatGPT(prompt, system_message='', model=model):
    if system_message == '':
        system_message = "Du bist ein hilfreicher Assistent"
    if mode=='anthropic':
        message = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0,
            system=system_message,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    else:
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
    system_message = "Du bist ein hilfreicher Assistent"
    if mode == 'anthropic':
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0,
            system=messages[0]['content'],
            messages=messages[1:],
            stream=True
        )
        input_tokens = 0
        output_tokens = 0
        for line in response:
            if line.type == 'message_start':
                input_tokens = line.message.usage.input_tokens
            elif line.type == 'message_delta':
                output_tokens = line.usage.output_tokens
            elif line.type == 'content_block_delta':
                yield line.delta.text
        yield "###STOP###" + json.dumps({"prompt_tokens": input_tokens, "completion_tokens": output_tokens, "total_tokens": input_tokens + output_tokens})
        

         
            
    else:
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
                    print (line.usage)
                    try:
                        yield "###STOP###" + json.dumps(line.usage)
                    except:
                        pass
