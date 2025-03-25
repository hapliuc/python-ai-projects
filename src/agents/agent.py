import os
from dotenv import load_dotenv
from openai import OpenAI
from agent_pkg.llm import completion, function_call, load_tools
from agent_pkg.tools import create_file, create_folder


def main() -> None:
    load_dotenv()
    tool_path = str(os.getenv("TOOL_PATH"))
    tools: list = []
    messages: list = []
    function_list = [create_folder, create_file]

    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    load_tools(tool_path, tools)
    system_prompt: dict = {
        "role": "system",
        "content": "You are a helpful AI chatbot with agentic capabilities. Use the tools you have acces to, to fulfill user requests",
    }
    messages.append(system_prompt)

    user_input: str = input("> User Prompt: ")
    user_prompt: dict = {"role": "user", "content": user_input}
    messages.append(user_prompt)

    completion_1 = completion(client, "llama3.2", messages, tools)
    function_call(completion_1, messages, function_list)
    completion_2 = completion(client, "llama3.2", messages, tools)
    print(f"> LLM Response:", completion_2.choices[0].message.content)


if __name__ == "__main__":
    main()
