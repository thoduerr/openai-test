import os
import re
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

def replace_reference_with_content(input_string):
    pattern = r"file:([^:\s]+)"
    
    def read_file(filename):
        if os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return f"[Error: File '{filename}' not found]"

    result = re.sub(pattern, lambda match: read_file(match.group(1)), input_string)
    
    return result

# load .env file
_ = load_dotenv(find_dotenv())

# arguments
print(sys.argv)
topic = sys.argv[1]
role = sys.argv[2]
chat_file = "./chats/" + topic + "_" + role + ".json"
print(chat_file)

# prompt
prompt = input("prompt$ ")
prompt = replace_reference_with_content(prompt)

# load existing chat if present
chat = []
try:
    with open(chat_file, "r") as file:
        chat = json.load(file)

    chat.append({"role": "user", "content": prompt})
except:
    # load prepared system_message for role
    with open("./role/" + role + ".md", "r") as file:
        system_message = file.read().replace("\n", "")
    # assemble new chat
    chat = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]

# openapi client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

model = os.environ.get("OPENAI_MODEL", "gpt-4-turbo")
temperature = os.environ.get("OPENAI_TEMPERATURE", 0.3)
max_tokens = os.environ.get("OPENAI_TOKENS", 4096)
topic = os.environ.get("OPENAI_TOPIC", "test")

# call
completion = client.chat.completions.create(
    model=model,
    temperature=temperature,
    max_tokens=max_tokens,
    messages=chat,
)

answer = {}
answer["role"] = completion.choices[0].message.role
answer["content"] = completion.choices[0].message.content

chat.append(answer)

# save chat
with open(chat_file, "w") as file:
    json.dump(chat, file, indent=4)

# print result
print(f"{completion.choices[0].message.content}")

