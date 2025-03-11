from typing import Any, Iterable
from pydantic import BaseModel
from openai import OpenAI
import json
import os

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

class StructuredOutput(BaseModel):
    command_executed: str
    explanation: str

def create_folder(path: str) -> None:
    os.popen(f'mkdir {path}')

def create_file(name: str) -> None:
    os.popen(f'touch {name}')

def call_function(name: str, args: Any) -> None:
    if name == 'create_folder':
        return create_folder(**args)
    elif name == 'create_file':
        return create_file(**args)

def llm_tool_calls(messages: Iterable, tools: Iterable) -> list | None:
    completion = client.chat.completions.create(
        model='llama3.2',
        messages=messages,
        tools=tools
    )
    return completion.choices[0].message.tool_calls

def llm_tool_execution(tool_calls) -> str:
    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        call_function(name, args)
    return os.popen('ls -al').read()

def main() -> None:
    system_prompt = 'You are a helpful AI assistant' 
    user_prompt = input('> User Prompt: ')
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    tools = [
        {
            'type': 'function',
            'function': {
                'name': 'create_folder',
                'description': 'Create a folder',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'path': {
                            'type': 'string',
                            'description': 'Path in which to create the folder'
                        }
                    },
                    'required': [
                        'path'
                    ],
                    'additionalProperties': False
                },
                'strict': True
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'create_file',
                'description': 'Create a file with a given name',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'Name of the file or directory'
                        },
                    },
                    'required': [
                        'name',
                    ],
                    'additionalProperties': False
                },
                'strict': True
            }
        }
    ]
    print('> LLM Response:\n', llm_tool_execution(llm_tool_calls(messages, tools)))

if __name__ == '__main__':
    main()
