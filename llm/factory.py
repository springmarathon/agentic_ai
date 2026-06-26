import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def create_llm_client():
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )