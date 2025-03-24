import os
from dotenv import load_dotenv
from openai import OpenAI
from llm_functions import llm_completion, llm_function_call, llm_load_tools


def create_folder(path: str) -> str:
    os.popen(f"mkdir {path}")
    return f"Created directory {path}"


def create_file(name: str) -> str:
    os.popen(f"touch {name}")
    return f"Created file {name}"


def main() -> None:
    load_dotenv()
    tool_path = str(os.getenv("TOOL_PATH"))
    tools: list = []
    messages: list = []
    function_list = [create_folder, create_file]

    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    llm_load_tools(tool_path, tools)
    system_prompt: dict = {
        "role": "system",
        "content": "You are a helpful AI chatbot with agentic capabilities. Use the tools you have acces to, to fulfill user requests",
    }
    messages.append(system_prompt)

    user_input: str = input("> User Prompt: ")
    user_prompt: dict = {"role": "user", "content": user_input}
    messages.append(user_prompt)

    completion_1 = llm_completion(client, "llama3.2", messages, tools)
    llm_function_call(completion_1, messages, function_list)
    completion_2 = llm_completion(client, "llama3.2", messages, tools)
    print(f"> LLM Response:", completion_2.choices[0].message.content)


if __name__ == "__main__":
    main()
