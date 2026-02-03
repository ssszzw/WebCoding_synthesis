import os
from openai import OpenAI
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 配置模型参数
# gemini-3-pro
api_key = "ipyezule1b95gc953qf8dvd00p8ct6fz6yu5"
model = "app-wcy0kf-1764751667098941604"
url = "https://wanqing-api.corp.kuaishou.com/api/agent/v1/apps"

# claude-4.5
# api_key="w8hd39mwy1umpnp6s7dh49tn1uyy4hta0fj6"
# model="ep-5b9ezm-1768964270166908191"
# url="https://wanqing-api.corp.kuaishou.com/api/gateway/v1/endpoints"

# 配置变量
INPUT_JSONL_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/01generated_prompt/prompts_20260129_141125.jsonl"
OUTPUT_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/01generated_prompt"
MAX_WORKERS = 25  # 并发工作线程数


def read_prompts_from_jsonl(jsonl_file):
    """从JSONL文件读取所有prompts
    
    Args:
        jsonl_file: JSONL文件路径
    
    Returns:
        list: 包含所有prompt数据的列表
    """
    prompts = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    # JSONL格式是 {项目名: prompt内容}
                    # 需要提取第一个键值对
                    if data:
                        project_name = list(data.keys())[0]
                        prompt = data[project_name]
                        prompts.append({
                            "line_number": line_num,
                            "original_data": data,
                            "project_name": project_name,
                            "prompt": prompt
                        })
                except json.JSONDecodeError as e:
                    print(f"✗ 解析第 {line_num} 行时出错: {e}")
                    continue
    return prompts


def clean_prompt(client, prompt_text, project_name):
    """调用模型清理prompt，提取功能描述内容
    
    Args:
        client: OpenAI客户端
        prompt_text: 原始prompt文本
        project_name: 项目名称
    
    Returns:
        str: 清理后的prompt
    """
    system_message = """你是一个prompt提取专家。你的任务是从给定的文本中提取纯粹的项目需求内容，去除所有markdown标记和附属说明。提供给你的prompt只是一个可能有一定表述或者格式问题的提示词，返回给我他原本的想表达的完整提示词。

**提取原则**：
1. 去除所有markdown标记（如 #、*、`、[]、-、> 等）
2. 保留所有功能描述、技术要求、交互说明等实际需求
3. 整理成流畅的段落文本

**输出要求**：
- 直接输出提取后的需求文本
- 不要添加任何标记或格式
- 保持内容完整和逻辑清晰"""

    user_message = f"""项目：{project_name}

原始内容：
{prompt_text}

---

请提取上述内容中的项目需求，去除所有markdown标记和格式化内容。"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
        )
        
        cleaned_prompt = completion.choices[0].message.content.strip()
        
        # 去除可能的markdown代码块标记
        if cleaned_prompt.startswith("```"):
            lines = cleaned_prompt.split("\n")
            cleaned_prompt = "\n".join(lines[1:-1] if len(lines) > 2 else lines)
            cleaned_prompt = cleaned_prompt.strip()
        
        return cleaned_prompt
        
    except Exception as e:
        print(f"  ✗ 清理失败：{e}")
        return None


def process_single_prompt(client, prompt_data, idx, total):
    """处理单个prompt的清理任务
    
    Args:
        client: OpenAI客户端
        prompt_data: prompt数据字典
        idx: 当前索引
        total: 总数量
    
    Returns:
        dict: 处理结果
    """
    project_name = prompt_data["project_name"]
    original_prompt = prompt_data["prompt"]
    
    print(f"[{idx}/{total}] 正在清理: {project_name}")
    
    cleaned_prompt = clean_prompt(client, original_prompt, project_name)
    
    if cleaned_prompt:
        print(f"  ✓ 清理成功 (原:{len(original_prompt)}字 → 新:{len(cleaned_prompt)}字)")
        return {
            "status": "success",
            "line_number": prompt_data["line_number"],
            "project_name": project_name,
            "original_prompt": original_prompt,
            "cleaned_prompt": cleaned_prompt,
            "original_length": len(original_prompt),
            "cleaned_length": len(cleaned_prompt),
            "reduction_ratio": (len(original_prompt) - len(cleaned_prompt)) / len(original_prompt) if len(original_prompt) > 0 else 0
        }
    else:
        print(f"  ✗ 清理失败")
        return {
            "status": "failed",
            "line_number": prompt_data["line_number"],
            "project_name": project_name,
            "original_prompt": original_prompt,
            "error": "Model returned empty result"
        }


def main():
    """主函数"""
    # 提取原文件名（不含扩展名）
    input_filename = os.path.basename(INPUT_JSONL_FILE)
    base_filename = os.path.splitext(input_filename)[0]  # 去除.jsonl扩展名
    
    print(f"{'='*80}")
    print(f"Prompt清理工具")
    print(f"{'='*80}")
    print(f"输入文件: {INPUT_JSONL_FILE}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"并发线程数: {MAX_WORKERS}")
    print(f"{'='*80}\n")
    
    # 读取prompts
    print("正在读取prompts...")
    prompts = read_prompts_from_jsonl(INPUT_JSONL_FILE)
    print(f"✓ 读取了 {len(prompts)} 个prompts\n")
    
    if not prompts:
        print("✗ 没有找到任何prompts")
        return
    
    # 创建OpenAI客户端
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    
    # 并发处理所有prompts
    all_results = []
    results_lock = threading.Lock()
    
    print(f"开始并发清理prompts（{MAX_WORKERS}个工作线程）...\n")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_single_prompt, client, prompt_data, idx, len(prompts)): prompt_data
            for idx, prompt_data in enumerate(prompts, 1)
        }
        
        for future in as_completed(futures):
            try:
                result = future.result()
                with results_lock:
                    all_results.append(result)
            except Exception as e:
                print(f"  ✗ 处理任务时出错: {e}")
    
    # 统计结果
    successful = [r for r in all_results if r["status"] == "success"]
    failed = [r for r in all_results if r["status"] == "failed"]
    
    print(f"\n{'='*80}")
    print(f"清理完成！")
    print(f"{'='*80}")
    print(f"总数: {len(all_results)}")
    print(f"成功: {len(successful)}")
    print(f"失败: {len(failed)}")
    
    if successful:
        avg_reduction = sum(r["reduction_ratio"] for r in successful) / len(successful)
        print(f"平均压缩率: {avg_reduction*100:.1f}%")
    
    # 保存结果
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 保存清理后的prompts（JSONL格式）
    output_jsonl_file = os.path.join(OUTPUT_DIR, f"{base_filename}_refresh.jsonl")
    with open(output_jsonl_file, "w", encoding="utf-8") as f:
        for result in successful:
            output_data = {
                "project_name": result["project_name"],
                "prompt": result["cleaned_prompt"],
                "metadata": {
                    "original_length": result["original_length"],
                    "cleaned_length": result["cleaned_length"],
                    "reduction_ratio": result["reduction_ratio"]
                }
            }
            f.write(json.dumps(output_data, ensure_ascii=False) + "\n")
    
    print(f"\n清理后的prompts已保存到: {output_jsonl_file}")
    
    # 保存详细报告（JSON格式）
    report_file = os.path.join(OUTPUT_DIR, f"{base_filename}_refresh_report.json")
    report_data = {
        "metadata": {
            "input_file": INPUT_JSONL_FILE,
            "output_file": output_jsonl_file,
            "processing_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_prompts": len(prompts),
            "successful": len(successful),
            "failed": len(failed),
            "max_workers": MAX_WORKERS
        },
        "statistics": {
            "average_reduction_ratio": sum(r["reduction_ratio"] for r in successful) / len(successful) if successful else 0,
            "total_original_chars": sum(r["original_length"] for r in successful),
            "total_cleaned_chars": sum(r["cleaned_length"] for r in successful),
            "total_chars_removed": sum(r["original_length"] - r["cleaned_length"] for r in successful)
        },
        "results": all_results
    }
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"详细报告已保存到: {report_file}")
    
    # 显示部分清理示例
    if successful:
        print(f"\n{'='*80}")
        print(f"清理示例（前3个）：")
        print(f"{'='*80}")
        for i, result in enumerate(successful[:3], 1):
            print(f"\n{i}. [{result['project_name']}]")
            print(f"   原始 ({result['original_length']}字): {result['original_prompt'][:80]}...")
            print(f"   清理后 ({result['cleaned_length']}字): {result['cleaned_prompt'][:80]}...")
            print(f"   压缩率: {result['reduction_ratio']*100:.1f}%")
    
    if failed:
        print(f"\n{'='*80}")
        print(f"失败的项目：")
        for i, result in enumerate(failed, 1):
            print(f"  {i}. {result['project_name']} - {result.get('error', 'Unknown error')}")
    
    print(f"\n{'='*80}")
    print(f"✓ 任务完成！")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
