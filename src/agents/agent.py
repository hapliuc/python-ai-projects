import os
from dotenv import load_dotenv
from openai import OpenAI
from agent_pkg.llm import completion, function_call, load_json
from agent_pkg.tools import create_file, create_folder


def main() -> None:
    try:
        load_dotenv()
        tool_path = str(os.getenv("TOOL_PATH"))
        sys_path = str(os.getenv("SYS_PATH"))
        tools: list = []
        messages: list = []
        function_list = [create_folder, create_file]

        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

        load_json(sys_path, messages)
        while True:
            user_input: str = input("> User Prompt: ")
            user_prompt: dict = {"role": "user", "content": user_input}
            messages.append(user_prompt)
            load_json(tool_path, tools)

            completion_1 = completion(client, "llama3.2", messages, tools)
            function_call(completion_1, messages, function_list)
            completion_2 = completion(client, "llama3.2", messages, tools)
            print(f"> LLM Response:", completion_2.choices[0].message.content)
    except KeyboardInterrupt:
        print("\nBye!")
        exit()


if __name__ == "__main__":
    main()
