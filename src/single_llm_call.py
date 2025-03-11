from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

def llm_response(system_prompt: str, user_prompt: str) -> str | None:
    completion = client.chat.completions.create(
        model='llama3.2',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
    )
    return completion.choices[0].message.content

def main() -> None:
    system_prompt = 'You are a helpful AI assistant'
    user_prompt = input('> User Prompt: ')
    print('> LLM Response:\n', llm_response(system_prompt, user_prompt))

if __name__ == '__main__':
    main()
