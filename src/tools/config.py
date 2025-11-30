import os
from dotenv import load_dotenv


def load_environment(path: str = ".env"):
    load_dotenv(dotenv_path=".env")


def list_environment_variables():
    for key, value in os.environ.items():
        print(f"{key:<40}: {value}")


def setup_proxy(http_proxy: str, https_proxy: str):
    os.environ["HTTP_PROXY"] = http_proxy
    os.environ["HTTPS_PROXY"] = https_proxy
