import os
import pytest
from openai import OpenAI
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    A session-scoped, auto-used fixture that loads the .env file once
    at the beginning of the test session.
    """
    load_dotenv(dotenv_path=".env")

@pytest.fixture(scope="module")
def deepseek_client():
    """
    Creates a module-scoped fixture that initializes the DeepSeek client once
    per test module (file).
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_ENDPOINT")
    
    if not api_key or not base_url:
        pytest.fail("DEEPSEEK_API_KEY or DEEPSEEK_ENDPOINT environment variables not set.")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    return client
