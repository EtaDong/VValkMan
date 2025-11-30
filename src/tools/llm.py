from .config import load_environment

import os
from google import genai
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


def init_deepseek_chat():
    llm = ChatOpenAI(
        model=os.getenv("DEEPSEEK_MODEL"),
        base_url=os.getenv("DEEPSEEK_ENDPOINT"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        # stream_usage=True,
        # temperature=None,
        # max_tokens=None,
        # timeout=None,
        # reasoning_effort="low",
        # max_retries=2,
        # api_key="...",  # If you prefer to pass api key in directly
        # base_url="...",
        # organization="...",
        # other
        # params...
    )
    return llm


def init_google_llm():
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_MODEL"),
        temperature=0,
        max_tokens=None,
        timeout=60,
        max_retries=0,
        transport="rest",
    )
    return llm


def init_gemini_llm():
    client = genai.Client()
    return client
