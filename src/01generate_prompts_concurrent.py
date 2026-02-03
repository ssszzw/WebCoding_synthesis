import os
import base64
from openai import OpenAI
import json
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# 配置模型参数
# gemini-3-pro
api_key = "ipyezule1b95gc953qf8dvd00p8ct6fz6yu5"
model = "app-wcy0kf-1764751667098941604"
url = "https://wanqing-api.corp.kuaishou.com/api/agent/v1/apps"

# claude-4.5
# api_key="w8hd39mwy1umpnp6s7dh49tn1uyy4hta0fj6"
# model="ep-5b9ezm-1768964270166908191"
# url="https://wanqing-api.corp.kuaishou.com/api/gateway/v1/endpoints"

# 并发配置
MAX_WORKERS = 30  # 最大并发线程数

# 文件锁，用于写入JSONL
file_lock = Lock()


def encode_image_to_base64(image_path):
    """将图片编码为base64格式"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def read_prompt_file(prompt_path):
    """读取prompt文件"""
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def get_images_in_folder(folder_path):
    """获取文件夹中的所有图片（包括video_images子目录）"""
    # 支持的图片格式
    image_extensions = ['.png', '.jpg', '.jpeg', '.webp', '.bmp']
    
    media_files = []
    
    # 检查是否存在video_images子目录
    video_images_path = os.path.join(folder_path, 'video_images')
    if os.path.exists(video_images_path) and os.path.isdir(video_images_path):
        # 遍历video_images目录中的文件
        for file in os.listdir(video_images_path):
            file_lower = file.lower()
            if any(file_lower.endswith(ext) for ext in image_extensions):
                media_files.append(os.path.join(video_images_path, file))
    
    return media_files


def generate_prompt_from_images(client, folder_name, prompt_text, media_paths):
    """调用模型生成提示词"""
    
    # 根据是否有图片文件构建不同的提示文本
    if media_paths:
        prompt_instruction = f"""请根据提供的图片和简短描述，生成一个详细的、能够实现图片中效果的完整提示词。

项目名称：{folder_name}
原始描述：{prompt_text}

要求：
1. 分析图片中的所有视觉效果、交互元素、动画效果、功能模块等。
2. 生成一个详细的提示词，包含：
   - 整体效果描述
   - 技术实现要点
   - 交互功能说明
   - 视觉效果细节
   - 动画和特效说明
3. 提示词应该清晰、具体、可执行
4. 明确要求所有代码（HTML, CSS, JS）必须合并在一个 `index.html` 文件中，并确保可以在浏览器中直接渲染出来。

输出格式要求：
- 必须使用中文输出提示词
- 请直接输出完整的提示词内容，使用 Markdown 格式
- 不要添加任何引导性文字、解释说明或额外的评论"""
    else:
        prompt_instruction = f"""请根据提供的简短描述，生成一个详细的、完整的Web开发提示词。

项目名称：{folder_name}
原始描述：{prompt_text}

要求：
1. 基于原始描述，补充和扩展功能细节。
2. 生成一个详细的提示词，包含：
   - 整体效果描述
   - 技术实现要点
   - 交互功能说明
   - 视觉效果细节
   - 动画和特效说明（如适用）
3. 提示词应该清晰、具体、可执行
4. 明确要求所有代码（HTML, CSS, JS）必须合并在一个 `index.html` 文件中，并确保可以在浏览器中直接渲染出来。

输出格式要求：
- 必须使用中文输出提示词
- 请直接输出完整的提示词内容，使用 Markdown 格式
- 不要添加任何引导性文字、解释说明或额外的评论"""
    
    # 构建消息内容
    content = [
        {
            "type": "text",
            "text": prompt_instruction
        }
    ]
    
    # 添加所有图片（如果有的话）
    if media_paths:
        for media_path in media_paths:
            file_ext = os.path.splitext(media_path)[1].lower()
            
            # 处理图片
            base64_image = encode_image_to_base64(media_path)
            # 根据实际格式设置 MIME 类型
            mime_type = "image/png" if file_ext == '.png' else f"image/{file_ext[1:]}"
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}"
                }
            })
    
    messages = [
        {
            "role": "user",
            "content": content
        }
    ]
    
    # 调用API
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"  ✗ 调用API时出错：{e}")
        return None


def process_single_folder(folder_name, base_folder, output_file):
    """处理单个文件夹，生成prompt并写入JSONL文件
    
    Args:
        folder_name: 文件夹名称
        base_folder: 基础目录路径
        output_file: 输出的JSONL文件路径
    
    Returns:
        dict: 包含处理结果的字典
    """
    folder_path = os.path.join(base_folder, folder_name)
    
    # 跳过非文件夹
    if not os.path.isdir(folder_path):
        return {"folder": folder_name, "status": "skipped", "reason": "not a directory"}
    
    print(f"[线程] 处理文件夹: {folder_name}")
    
    # 创建OpenAI客户端（每个线程独立的客户端）
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    
    # 优先读取origin_prompt.md，如果不存在则读取prompt.md
    origin_prompt_file = os.path.join(folder_path, "origin_prompt.md")
    prompt_file = os.path.join(folder_path, "prompt.md")
    
    if os.path.exists(origin_prompt_file):
        prompt_text = read_prompt_file(origin_prompt_file)
    elif os.path.exists(prompt_file):
        prompt_text = read_prompt_file(prompt_file)
    else:
        prompt_text = ""
    
    # 获取所有图片
    media_files = get_images_in_folder(folder_path)
    if not media_files:
        print(f"  [{folder_name}] 警告：未找到图片文件，将仅使用文本prompt生成")
    else:
        print(f"  [{folder_name}] 找到 {len(media_files)} 个图片文件")
    
    # 调用模型生成提示词
    print(f"  [{folder_name}] 正在调用模型生成提示词...")
    generated_prompt = generate_prompt_from_images(client, folder_name, prompt_text, media_files)
    
    if generated_prompt:
        # 构建JSONL条目
        jsonl_entry = {
            folder_name: generated_prompt
        }
        
        # 使用锁保证线程安全地写入文件
        with file_lock:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(jsonl_entry, ensure_ascii=False) + "\n")
        
        print(f"  [{folder_name}] ✓ 成功生成并写入prompt")
        return {
            "folder": folder_name,
            "status": "success",
            "prompt_length": len(generated_prompt)
        }
    else:
        print(f"  [{folder_name}] ✗ 生成失败")
        return {
            "folder": folder_name,
            "status": "failed",
            "reason": "generation failed"
        }


def process_folders_concurrent(base_folder, output_folder, max_workers=5):
    """使用多线程并发处理所有文件夹
    
    Args:
        base_folder: 包含所有项目文件夹的基础目录
        max_workers: 最大并发线程数
    """
    # 创建输出目录
    output_dir = output_folder
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成输出文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"prompts_{timestamp}.jsonl")
    
    print(f"{'='*80}")
    print(f"开始并发处理文件夹")
    print(f"{'='*80}")
    print(f"基础目录: {base_folder}")
    print(f"输出文件: {output_file}")
    print(f"最大并发数: {max_workers}")
    print(f"{'='*80}\n")
    
    # 获取所有子文件夹
    folder_names = [f for f in os.listdir(base_folder) 
                   if os.path.isdir(os.path.join(base_folder, f))]
    
    total_folders = len(folder_names)
    print(f"找到 {total_folders} 个文件夹待处理\n")
    
    # 记录开始时间
    start_time = time.time()
    
    # 使用线程池并发处理
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_folder = {
            executor.submit(process_single_folder, folder_name, base_folder, output_file): folder_name
            for folder_name in folder_names
        }
        
        # 处理完成的任务
        completed = 0
        for future in as_completed(future_to_folder):
            folder_name = future_to_folder[future]
            try:
                result = future.result()
                results.append(result)
                completed += 1
                print(f"\n进度: [{completed}/{total_folders}] 完成")
            except Exception as e:
                print(f"\n✗ 处理 {folder_name} 时发生异常: {e}")
                results.append({
                    "folder": folder_name,
                    "status": "error",
                    "reason": str(e)
                })
                completed += 1
    
    # 计算统计信息
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    success_count = sum(1 for r in results if r.get("status") == "success")
    failed_count = sum(1 for r in results if r.get("status") in ["failed", "error"])
    skipped_count = sum(1 for r in results if r.get("status") == "skipped")
    
    # 输出最终统计
    print(f"\n\n{'='*80}")
    print(f"所有任务完成！")
    print(f"{'='*80}")
    print(f"总文件夹数: {total_folders}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"跳过: {skipped_count}")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"平均耗时: {elapsed_time/total_folders:.2f} 秒/文件夹")
    print(f"输出文件: {output_file}")
    print(f"{'='*80}\n")
    
    # 验证输出文件
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"✓ JSONL文件已生成，共 {len(lines)} 条记录")
    else:
        print(f"✗ 输出文件未生成")
    
    return results


if __name__ == "__main__":
    base_folder = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/resourses/full_prompt_images"
    output_folder = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/generated_prompt"
    
    # 使用5个并发线程处理
    results = process_folders_concurrent(base_folder, output_folder=output_folder, max_workers=MAX_WORKERS)
    
    # 可选：保存详细的结果报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/generated_prompt/report_{timestamp}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "total": len(results),
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"详细报告已保存到: {report_file}")
