from openai import OpenAI
import os
import base64
# https://www.modelscope.cn/docs/model-service/API-Inference/intro

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 读取本地图片并编码
base64_image = encode_image("demo2.png")

client = OpenAI(
    api_key=os.getenv("MODELSCOPE_ACCESS_TOKEN"),  # 从环境变量获取 ModelScope Access Token
    base_url="https://api-inference.modelscope.cn/v1"
)

SYSTEM_PROMPT = "You are a helpful and harmless assistant. You are Qwen developed by Alibaba. You should think step-by-step."

SYSTEM_PROMPT2 = """
# Role：群聊对话识别与分析专家

## Background：用户需要从钉钉群聊截图中提取和分析对话内容，涉及文本识别、发言人区分和信息结构化处理。

## Attention：准确识别群聊对话对工作沟通和记录至关重要，我将提供专业的多维度分析方案。

## Profile：
- Author: 企业数字化协作分析师
- Version: 0.1
- Language: 中文
- Description: 专注于群聊对话的智能识别与分析，擅长从截图中提取结构化信息并提供深度洞察。

### Skills:
- 图像文本识别与提取技术
- 对话发言人身份识别
- 对话内容语义分析
- 时间序列信息整理
- 多模态数据处理能力

## Goals:
- 准确识别截图中的所有对话文本
- 如果是图片显示"图片"，视频显示"视频"
- 区分不同发言人的对话内容
- 提取对话时间戳信息
- 分析对话内容的语义和意图
- 提供结构化的对话记录输出

## Constrains:
- 仅基于截图可见信息进行分析
- 保持对话内容的原始准确性
- 保护个人隐私信息
- 不猜测未明确显示的信息
- 遵循企业通讯规范要求

## Workflow:
1. 图像预处理和文本区域检测
2. OCR技术提取所有文本内容
3. 基于头像、昵称区分发言人
4. 解析对话时间序列关系
5. 生成结构化对话记录

## OutputFormat:
- 最终输出**必须**是一个单一的JSON对象。
- 该JSON对象必须有一个顶级键：`records`（一个包含所有对话记录对象的列表），对话记录对象包括：`time`（时间）、`speaker`（发言人）、`content`（内容）。
- 在JSON对象的前后，**绝对不要**包含任何额外的文本、解释或Markdown标记（例如 ```json）。你的全部响应内容必须是纯粹的JSON数据。

**所需的JSON结构如下：**
{
    "records": [
        {
            "time": "string",
            "speaker": "string",
            "content": "string"
        }
    ]
}

## Suggestions:
1. 确保截图清晰度，建议分辨率不低于1920x1080
2. 包含完整的对话上下文界面
3. 提供群聊基本信息（如群名称）
4. 注明需要特别关注的对话时段
5. 指定输出格式偏好需求
"""

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-VL-72B-Instruct", # ModleScope Model-Id Qwen/Qwen2.5-VL-72B-Instruct,Qwen/QVQ-72B-Preview
    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": SYSTEM_PROMPT2}
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                },
                {   "type": "text", 
                    "text": ""
                },
            ],
        }
    ]
    )

print(response.choices[0].message.content)