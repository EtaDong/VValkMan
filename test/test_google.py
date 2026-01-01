from langchain_google_genai.chat_models import ChatGoogleGenerativeAI


def test_google_ai(google_client: ChatGoogleGenerativeAI):
    response = google_client.invoke(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
        ]
    )
    assert response.content is not None
    assert len(response.content) > 0
    print("Google Generative AI test passed with response:", response.content)
