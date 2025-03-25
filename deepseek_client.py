# Deepseek调用
from openai import OpenAI
from conf.config import MODEL

class DeepSeekClient:
    def __init__(self, api_key, base_url="https://api.deepseek.com", tech_direction="JAVA"):
        self.api_key = api_key
        self.base_url = base_url
        self.tech_direction = tech_direction
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def call(self, prompt, model=MODEL, temperature=0.3):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a {self.tech_direction} expert."},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {str(e)}")
            return None
