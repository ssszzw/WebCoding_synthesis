import os
from openai import OpenAI
import base64
import datetime

#gemini-3-pro
api_key="ipyezule1b95gc953qf8dvd00p8ct6fz6yu5"
model="app-wcy0kf-1764751667098941604"
url="https://wanqing-api.corp.kuaishou.com/api/agent/v1/apps/chat/completions"
url="https://wanqing-api.corp.kuaishou.com/api/agent/v1/apps"


#claude-4.5
# api_key="w8hd39mwy1umpnp6s7dh49tn1uyy4hta0fj6"
# model="ep-5b9ezm-1768964270166908191"
# url="https://wanqing-api.corp.kuaishou.com/api/gateway/v1/endpoints"


video_path="/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/resourses/full_prompt_images/番茄时钟/video_images/image (7).gif"
def encode_image_to_base64(image_path):
    """将图片编码为base64格式"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

messages=[
    {"role": "user", "content": "你是谁？"}
]
messages=[
        {
            "role": "user",
            "content": [
                {"type": "text","text": "这是什么"},
                # 使用公有云部署模型，需传入公网可访问的图片链接
                # 使用私有部署模型，需传入 IDC 可访问的图片链接
                {"type": "image_url","image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}}
            ]
        }
]

    


messages = [
        {"role": "system", "content": "你是一个 AI 人工智能助手"},
        {"role": "user", "content": "基于Three.js实现3D鞭炮连锁爆炸仿真，包含自定义物理碰撞与爆炸冲击波系统。具备引线燃烧动画、多米诺式连锁引爆逻辑，以及逼真的碎屑堆积、烟雾粒子特效和动态光照。请给出html代码网页"},
    ]


client = OpenAI(
    base_url=url,
    api_key=api_key
)



completion = client.chat.completions.create(
    model=model,  # 使用变量 model
    messages=messages
)
# print(completion.choices[0].message.content)
with open(f"output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html", "w", encoding="utf-8") as f:
    f.write(completion.choices[0].message.content)