import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek


import httpx
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()


def init_deepseek():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("警告: 环境变量 DEEPSEEK_API_KEY 未设置")

    # 使用 trust_env=False 忽略系统代理环境变量
    http_client = httpx.Client(trust_env=False)

    _model = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        max_tokens=3000,
        timeout=None,
        max_retries=2,
        api_key=api_key,
        http_client=http_client,
    )
    return _model


model = init_deepseek()

messages = [
    ("system", "You are a helpful translator. Translate the user sentence to French."),
    ("human", "I love programming."),
]

print(model.invoke(messages))

# print(messages)
