import os
from google import genai

# https://ai.google.dev/gemini-api/docs/migrate?hl=zh_cn


def test_gemini_api():
    client = genai.Client()
    response = client.models.generate_content(
        model=os.getenv("GOOGLE_MODEL"),
        contents="Explain how AI works in a few words",
    )
    assert response.text is not None
    assert len(response.text) > 0
    print("Google API test passed with response:", response.text)
