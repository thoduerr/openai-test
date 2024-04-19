import os
import re
import sys
import json
import logging
import requests
from typing import List, Dict
from pypdf import PdfReader
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from dataclasses import dataclass

# Setup logging
logging.basicConfig(level=os.getenv('LOGLEVEL', 'INFO').upper(),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(find_dotenv())

@dataclass
class Config:
    api_key: str
    model: str = "gpt-4-turbo"
    temperature: float = 0.3
    max_tokens: int = 4096
    topic: str = "test"

def get_config() -> Config:
    METHOD_NAME = "get_config"
    logger.debug(f" > {METHOD_NAME}")
    
    result = Config(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", 0.3)),
        max_tokens=int(os.getenv("OPENAI_TOKENS", 4096)),
        topic=os.getenv("OPENAI_TOPIC", "test")
    )
    
    logger.debug(f" < {METHOD_NAME} {result}")
    return result

def read_file_content(file_path: Path) -> str:
    METHOD_NAME = "read_file_content"
    logger.debug(f" > {METHOD_NAME} {file_path}")

    result = ''
    try:
        result = file_path.read_text(encoding='utf-8')
    except:
        message = f" E ERROR: File '{file_path}' not found."
        logger.error(message)
        raise Exception(message)
    
    logger.debug(f" < {METHOD_NAME} ...{result[-20:]}")
    return result

def read_pdf_content(file_path: Path) -> str:
    METHOD_NAME = "read_pdf_content"
    logger.debug(f" > {METHOD_NAME} {file_path}")

    result = ''
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            result += page.extract_text() + "\n"
    except:
        message = f" E ERROR: File '{file_path}' not found."
        logger.error(message)
        raise Exception(message)
    
    logger.debug(f" < {METHOD_NAME} ...{result[-20:]}")
    return result

def read_web_content(url: str) -> str:
    METHOD_NAME = "read_web_content"
    logger.debug(f" > {METHOD_NAME} {url}")

    result = ''
    try:
        response = requests.get(url, verify=False)
        logger.info(response)
        result = response.text
    except:
        message = f" E ERROR: GET request to '{url}' failed."
        logger.error(message)
        raise Exception(message)
    
    logger.debug(f" < {METHOD_NAME} ...{result[-20:]}")
    return result

def replace_reference_with_content(input_string: str) -> str:
    METHOD_NAME = "replace_reference_with_content"
    logger.debug(f" > {METHOD_NAME} ...{input_string[-20:]}")

    pattern = r"file:([^:\s]+)"
    result = re.sub(pattern, lambda match: read_file_content(Path(match.group(1))), input_string)

    pattern = r"pdf:([^:\s]+)"
    result = re.sub(pattern, lambda match: read_pdf_content(Path(match.group(1))), result)
    
    pattern = r"web:(((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*)"
    result = re.sub(pattern, lambda match: read_web_content(match.group(1)), result)

    logger.debug(f" < {METHOD_NAME} ...{result[-20:]}")
    return result

def load_or_initialize_chat(file_path: Path, prompt: str, role: str) -> List[Dict[str, str]]:
    METHOD_NAME = "load_or_initialize_chat"
    logger.debug(f" > {METHOD_NAME} {file_path} ...{prompt[-20:]} {role}")

    result = []
    try:
        result = json.loads(file_path.read_text())
        result.append({"role": "user", "content": prompt})
    except:
        system_message = read_file_content(Path("./role/") / f"{role}.md").replace("\n", "")
        result = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]

    logger.debug(f" < {METHOD_NAME} ...{result[-20:]}")
    return result

def save_chat(file_path: Path, chat: List[Dict[str, str]]) -> None:
    METHOD_NAME = "save_chat"
    logger.debug(f" > {METHOD_NAME} {file_path} {chat[-20:]}")

    save_file(file_path, json.dumps(chat, indent=4))

    logger.debug(" < {METHOD_NAME}")
    
def save_file(file_path: Path, content: str) -> None:
    METHOD_NAME = "save_file"
    logger.debug(f" > {METHOD_NAME} {file_path} {content[-20:]}")

    try:
        file_path.write_text(content, encoding='utf-8')
    except:
        message = f" E ERROR: Path '{file_path}' not found."
        logger.error(message)
        raise Exception(message)

    logger.debug(" < {METHOD_NAME}")

def process(config, topic, role, prompt):
    METHOD_NAME = "process"
    logger.debug(f" > {METHOD_NAME} {config} {topic} {role} ...{prompt[-20:]}")
  
    chat_file_path = Path("./chats/") / f"{topic}_{role}.json"
    
    prompt = replace_reference_with_content(prompt)
    chat = load_or_initialize_chat(chat_file_path, prompt, role)

    client = OpenAI(api_key=config.api_key)
    completion = client.chat.completions.create(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            messages=chat
        )

    answer = {"role": completion.choices[0].message.role, "content": completion.choices[0].message.content}
    chat.append(answer)
    save_chat(chat_file_path, chat)
    
    result = answer['content']
    logger.debug(f" < {METHOD_NAME} ...{result[-20:]}")
    return result

def read_last_answer(file_path: Path) -> str:
    METHOD_NAME = "read_last_answer"
    logger.debug(f" > {METHOD_NAME} {file_path}")

    result = ''
    try:
        result = file_path.read_text(encoding='utf-8')
    except:
        message = f" W WARNING: File '{file_path}' not found."
        logger.warning(message)

    logger.debug(f" < {METHOD_NAME} ...{result[-20:]}")
    return result

def store_last_answer(file_path: Path, content: str) -> str:
    METHOD_NAME = "store_last_answer"
    logger.debug(f" > {METHOD_NAME} {file_path} ...{content[-20:]}")

    save_file(file_path, content)

    logger.debug(f" < {METHOD_NAME}")


def main():
    logger.info("Starting...")

    if len(sys.argv) < 3:
        logger.error(" E ERROR: Insufficient command line arguments provided. Usage: main.py <topic> <role>")
        sys.exit(1)

    config = get_config()
    topic, role = sys.argv[1:3]
    prompt = read_last_answer(Path("./workflow/prompt.txt"))

    try:
        if not prompt:
            prompt = input("prompt$ ")

        result = process(config, topic, role, prompt)

        store_last_answer(Path("./workflow/prompt.txt"), result)
        logger.info(result)
    except Exception as e:
        logger.error(f" E ERROR: An unexpected error occurred: {e}")

    logger.info("Completed.")

if __name__ == "__main__":
    main()