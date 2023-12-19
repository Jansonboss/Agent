import json
from typing import Dict, List

from agent.utils import chat_completion
from functions.functions import public_search, send_email, FUNCTIONS



FUNCTION_TO_CALL: Dict[str, callable] = {
    "public_search": public_search,
    "send_email": send_email,
}

PERSONA = """
You are Maya, a technical support specialist responsible for answering questions about IT related question only.
You will use the search tool to find relevant knowledge articles to create the answer.
Being smart in your research. If the search does not come back with the answer, rephrase the question and try again.
Review the result of the search and use it to guide your next search if needed. Only answer with the search results that is relevant with what user is asking.
Based on the search result and user request, extract and summarize the given search results to write specific, numbered, actionable instructions or comprehensible content to respond to and resolve the user request. The final response should be written using formatted HTML but only with bold and italics tags.
If the question is complex, and contain multiple request, break down to smaller search steps and find the answer in multiple steps.
Answer ONLY with the facts from the search tool. If there isn't enough information, say you don't know. Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.
Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brackets to reference the source, e.g. [info1.txt]. Don't combine sources, list each source separately, e.g. [info1.txt][info2.pdf].
"""


class Agent:

    def __init__(self, persona: str):
        self.messages: List[Dict] = [
            {"role": "system", "content": persona}
        ]

    def generate_function_response(self, messages: List[Dict], functions: List[Dict], mode: str = "auto"):
        response = chat_completion(messages=messages, functions=functions, function_call=mode)
        function_call_response: Dict[str, str] = response["choices"][0]["message"].get("function_call", "")
        if not function_call_response:
            self.messages.append({
                "role": "function",
                "name": "None",
                "content": "None."
            })
            return 0

        func_name = function_call_response.get("name", "")

        # TODO: check func_name is valid
        # if func_name not in [fk for fk in FUNCTIONS.keys()]:
        #     func = FUNCTION_TO_CALL[func_name]

        # TODO: check func_args are valid
        #   func_args = function_response["arguments"]

        func = FUNCTION_TO_CALL[func_name]
        func_args = json.loads(function_call_response["arguments"])
        print(func_args)
        func_output = func(**func_args)
        message = {
                "role": "function",
                "name": func.__name__,
                "content": func_output
            }
        self.messages.append(message)
        return 1

    def generate_stream_response(self, messages):
        response = chat_completion(messages)
        for chunk in response:
            chunk_msg = chunk["choices"][0]["delta"].get("content", "")
            yield chunk_msg

    def generate_response(self, messages):
        response = chat_completion(messages=messages)
        result = response["choices"][0]["message"].get("content", "")
        self.messages.append({
            "role": "assistant",
            "content": result
        })
        return result

    def get_function_mode(self):
        # return {"name": "public_search"}
        return "auto"

    def run(self, messages: List[Dict]):
        self.messages.append(messages)

        while True:
            response = self.generate_function_response(
                self.messages, FUNCTIONS, self.get_function_mode()
            )
            if not response:
                break

        response = self.generate_response(self.messages)
        return response


if __name__ == "__main__":
    agent = Agent(persona=PERSONA)
    while True:
        request = input("User: ").strip()
        response = agent.run(
            {"role": "user", "content": request}
        )
        print(f"Agent: {response}")
