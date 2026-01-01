import os
from openai import OpenAI


def test_deep_api(deepseek_client: OpenAI):
    response = deepseek_client.chat.completions.create(
        model=os.getenv("DEEPSEEK_MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False,
    )
    assert response.choices[0].message.content is not None
    assert len(response.choices[0].message.content) > 0
    print(
        "DeepSeek API test passed with response:", response.choices[0].message.content
    )
