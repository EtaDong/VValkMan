import os
import pytest
from openai import OpenAI
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


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
    https://reference.langchain.com/python/integrations/langchain_openai/ChatOpenAI/
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_ENDPOINT")

    if not api_key or not base_url:
        pytest.fail(
            "DEEPSEEK_API_KEY or DEEPSEEK_ENDPOINT environment variables not set."
        )

    client = OpenAI(api_key=api_key, base_url=base_url)
    return client


@pytest.fixture(scope="module")
def google_client():
    """
    Creates a module-scoped fixture that initializes the Google Generative AI chat client once
    per test module (file).
    https://reference.langchain.com/python/integrations/langchain_google_genai
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GOOGLE_MODEL")

    if not api_key or not model:
        pytest.fail("GOOGLE_API_KEY or GOOGLE_MODEL environment variables not set.")

    client = ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        max_tokens=None,
        timeout=60,
        max_retries=0,
        transport="rest",
    )
    return client
