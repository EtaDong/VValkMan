from langchain_ollama import ChatOllama

llm = ChatOllama(model="gpt-oss:latest", validate_model_on_init=False, temperature=0)

messages = [
    ("system", "You are a helpful translator. Translate the user sentence to French."),
    ("human", "I love programming."),
]
print(llm.invoke(messages))
