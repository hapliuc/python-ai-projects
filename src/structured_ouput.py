from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


class StructuredOutput(BaseModel):
    project_name: str
    year_founded: int
    founder_name: str


def llm_response(system_prompt: str, user_prompt: str) -> str | None:
    completion = client.beta.chat.completions.parse(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=StructuredOutput,
    )
    return completion.choices[0].message.content


def main() -> None:
    system_prompt = "You are a helpful AI assistant, you role is to provide information about open-source projects"
    user_prompt = input("> User Prompt: ")
    print("> LLM Response:\n", llm_response(system_prompt, user_prompt))


if __name__ == "__main__":
    main()
