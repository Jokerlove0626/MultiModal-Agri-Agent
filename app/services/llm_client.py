import os
from openai import AsyncOpenAI

class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model_name = os.getenv("LLM_MODEL_NAME", "qwen-turbo")

    async def generate_response(self, messages):
        response = await self.client.chat.completions.create(
            model=self.model_name, # 👈 使用动态名字
            messages=messages
        )
        return response
    async def chat_text(self, messages: list, temperature: float = 0.3) -> str:
        """调用纯文本大模型"""
        response = await self.client.chat.completions.create(
            model="qwen-plus", 
            messages=messages,
            temperature=temperature 
        )
        return response.choices[0].message.content

    async def chat_vision(self, sys_prompt: str, base64_image: str) -> str:
        """调用多模态视觉大模型"""
        response = await self.client.chat.completions.create(
            model="qwen-vl-max",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": sys_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ]
        )
        return response.choices[0].message.content.strip()