import os

import openai
from tenacity import retry, stop_after_attempt, wait_random

from functions import FUNCTIONS


@retry(wait=wait_random(min=2, max=4), stop=stop_after_attempt(6))
def chat_completion(**kwargs):
    openai.api_type = os.environ.get("openai_api_type")
    openai.api_version = os.environ.get("openai_api_version")  # 2023-07-01-preview
    openai.api_key = os.environ.get("openai_api_key_gpt4")
    openai.api_base = os.environ.get("openai_api_base_gpt4")
    engine = os.environ.get("gpt4_engine")

    response = openai.ChatCompletion.create(
        **kwargs,
        engine=engine,
        temperature=0,
        max_tokens=768,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response


if __name__ == "__main__":
    result0 = chat_completion(
        messages=[{"role": "user", "content": "greeting to alex"}],
        functions=FUNCTIONS,
        function_call={"name": "send_email"}
    )
    print(result0["choices"])
    print(type(result0))

    result1 = chat_completion(
        messages=[{"role": "user", "content": "greeting to alex"}]
    )
    print(result1)