from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("MODELSCOPE_ACCESS_TOKEN"), # 请替换成您的ModelScope Access Token
    base_url="https://api-inference.modelscope.cn/v1"
)

response = client.chat.completions.create(
    model="Qwen/QVQ-72B-Preview", # ModleScope Model-Id
    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": "You are a helpful and harmless assistant. You are Qwen developed by Alibaba. You should think step-by-step."}
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/QVQ/demo.png"}
                },
                {   "type": "text", 
                    "text": "What value should be filled in the blank space?"
                },
            ],
        }
    ],
    stream=True
    )


for chunk in response:
    print(chunk.choices[0].delta.content, end='', flush=True)