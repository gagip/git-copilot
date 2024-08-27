from typing import Optional
from openai import OpenAI


class Copilot:
    def __init__(self):
        self.client = OpenAI()

    def summarize_commits(self, commit_infos, prompt_file: str) -> Optional[str]:
        with open(prompt_file, 'r', encoding="utf-8") as file:
            system_message = file.read()

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": commit_infos,
                },
            ],
        )

        return completion.choices[0].message.content