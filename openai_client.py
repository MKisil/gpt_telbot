import os

from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI

load_dotenv(find_dotenv())

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
