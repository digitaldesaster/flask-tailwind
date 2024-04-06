import os

def load_env():
    # Load the .env file and set environment variables
    with open('.env', 'r') as file:
        for line in file:
            print (line)
            # Skip lines that are comments or empty
            if line.startswith('#') or not line.strip():
                continue
            # Split the line into key and value at the first '='
            key, value = line.strip().split('=', 1)
            if key !="":
                os.environ[key] = value
    return os.environ
