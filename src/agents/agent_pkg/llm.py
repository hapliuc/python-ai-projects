import os
import json
import logging
from json.decoder import JSONDecodeError
from openai import OpenAI, APIConnectionError
from openai.types.chat import ChatCompletion


logger = logging.getLogger(__name__)


def completion(
    client: OpenAI, model: str, messages: list, tools: list
) -> ChatCompletion:
    try:
        return client.chat.completions.create(
            model=model, messages=messages, tools=tools
        )
    except APIConnectionError as e:
        logger.critical(f"Exception: {e.__class__.__name__} - {e}", exc_info=True)
        exit(1)


def completion_structured(
    client: OpenAI, model: str, messages: list, tools: list, response_format
):
    try:
        return client.beta.chat.completions.parse(
            model=model, messages=messages, tools=tools, response_format=response_format
        )
    except APIConnectionError as e:
        logger.critical(f"Exception: {e.__class__.__name__} - {e}", exc_info=True)
        exit(1)
    except TypeError as e:
        logger.critical(f"Exception: {e.__class__.__name__} - {e}", exc_info=True)
        exit(1)


def load_tools(path: str, tools: list) -> None:
    try:
        for file in os.listdir(path):
            if file.endswith(".json"):
                with open(f"{path}/{file}", "r") as f:
                    tools.append(json.loads(f.read()))

    except JSONDecodeError as e:
        logger.critical(f"Exception: {e.__class__.__name__} - {e}", exc_info=True)
        exit(1)


def function_call(
    completion: ChatCompletion, messages: list, function_list: list
) -> None:
    try:
        if completion.choices[0].message.tool_calls:

            def call_function(name, args):
                nonlocal function_list
                for function in function_list:
                    if name == function.__name__:
                        return function(**args)

            for tool_call in completion.choices[0].message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = call_function(name, args)
                messages.append(completion.choices[0].message)
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                )
    except AttributeError as e:
        logger.critical(f"Exception: {e.__class__.__name__} - {e}", exc_info=True)
        exit(1)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    main()
