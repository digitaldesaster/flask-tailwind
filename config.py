def getConfig():
    system_message = "Du bist ein hilfreicher Assistent! Antworte immer auf Deutsch! Wenn du Code generierst dann setze den Code in backticks"
    welcome_message = "Hallo wie kann ich helfen?"
    messages=[]
    models = [
        {'provider':'openai','model':'gpt-3.5-turbo','name':'gpt-3.5-turbo'},
        {'provider':'openai','model':'gpt-4-turbo-preview','name':'gpt-4-turbo'},
        {'provider':'together','model':'meta-llama/Llama-2-70b-chat-hf','name':'meta-llama-2-70b'},
        {'provider':'anthropic','model':'claude-3-haiku-20240307','name':'claude-3-haiku'},
        {'provider':'anthropic','model':'claude-3-opus-20240229','name':'claude-3-opus'}
        ]
    return {"system_message":system_message,"welcome_message":welcome_message,'messages':messages,'models':models,'use_prompt_template':'False'}
