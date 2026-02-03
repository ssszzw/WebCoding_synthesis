import os
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
MAX_WORKERS = 25  # 最大并发线程数

# 文件锁，用于写入JSONL
file_lock = Lock()


def generate_prompt_summary(client, prompt_content, project_name):
    """调用模型生成prompt的功能特点总结
    
    Args:
        client: OpenAI客户端
        prompt_content: prompt内容
        project_name: 项目名称
    
    Returns:
        str: 功能特点总结
    """
    system_message = """你是一个专业的技术文档分析专家。你的任务是分析前端Web开发的prompt，并生成简洁的功能特点描述。

重要说明：
- 这个描述将被用作该prompt的分类依据
- 描述必须简洁明了，突出核心功能特点，反映该prompt的主要目标
- 控制在80字以内
- 直接描述功能，不要添加"类型"、"技术栈"等标签

输出要求：
1. 用2-3句话概括项目的核心功能和特点
2. 聚焦于功能本身，而非技术实现
3. 使用简洁、清晰的语言
4. 突出项目的独特性和主要用途

输出格式示例：
实现了一个交互式音乐播放器，支持播放列表管理、歌词显示和可视化效果。用户可以上传本地音频文件，控制播放进度，并查看动态频谱动画。

注意：
- 直接输出功能描述，不要添加任何标签或分类
- 不要冗长描述，只提取核心功能
- 聚焦于可用于分类的关键特征
- 避免过于详细的技术实现细节"""

    user_message = f"""请分析以下prompt，生成简洁的功能特点描述（80字以内）：

项目名称：{project_name}

Prompt内容：
---
{prompt_content}
---

请直接输出功能描述，不要添加任何额外的说明文字或标签。"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    # 调用API
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,  # 较低的温度保证总结的稳定性和准确性
        )
        
        summary = completion.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"  ✗ 调用API时出错：{e}")
        return None


def process_single_prompt(project_name, prompt_content, source_file, output_file):
    """处理单个prompt，生成总结并写入JSONL文件
    
    Args:
        project_name: 项目名称
        prompt_content: prompt内容
        source_file: 源jsonl文件路径
        output_file: 输出的JSONL文件路径
    
    Returns:
        dict: 包含处理结果的字典
    """
    print(f"[线程] 处理项目: {project_name}")
    
    # 创建OpenAI客户端（每个线程独立的客户端）
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    
    # 生成总结
    print(f"  [{project_name}] 正在生成功能特点总结...")
    summary = generate_prompt_summary(client, prompt_content, project_name)
    
    if summary:
        # 构建JSONL条目
        jsonl_entry = {
            "source_file": source_file,
            "project_name": project_name,
            "original_prompt": prompt_content,
            "summary": summary,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 使用锁保证线程安全地写入文件
        with file_lock:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(jsonl_entry, ensure_ascii=False) + "\n")
        
        print(f"  [{project_name}] ✓ 成功生成并写入总结")
        print(f"  [{project_name}] 总结: {summary}")
        return {
            "project": project_name,
            "status": "success",
            "summary_length": len(summary)
        }
    else:
        print(f"  [{project_name}] ✗ 总结生成失败")
        return {
            "project": project_name,
            "status": "failed",
            "reason": "generation failed"
        }


def process_prompts_concurrent(input_jsonl, output_dir, max_workers=10):
    """使用多线程并发处理JSONL文件中的所有prompts
    
    Args:
        input_jsonl: 输入的JSONL文件路径
        output_dir: 输出目录
        max_workers: 最大并发线程数
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_jsonl):
        print(f"✗ 错误：输入文件不存在: {input_jsonl}")
        return
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成输出文件名
    output_file = os.path.join(output_dir, "summaries.jsonl")
    
    # 如果输出文件已存在，备份
    if os.path.exists(output_file):
        backup_file = output_file.replace(".jsonl", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
        os.rename(output_file, backup_file)
        print(f"⚠️  输出文件已存在，已备份到: {backup_file}")
    
    print(f"{'='*80}")
    print(f"开始并发处理prompts总结")
    print(f"{'='*80}")
    print(f"输入文件: {input_jsonl}")
    print(f"输出文件: {output_file}")
    print(f"最大并发数: {max_workers}")
    print(f"{'='*80}\n")
    
    # 读取输入JSONL文件
    prompts_data = []
    with open(input_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    # 每行是一个字典，key是项目名，value是prompt
                    for project_name, prompt_content in data.items():
                        prompts_data.append({
                            "project_name": project_name,
                            "prompt_content": prompt_content
                        })
                except json.JSONDecodeError as e:
                    print(f"✗ 解析JSON行时出错: {e}")
                    continue
    
    total_prompts = len(prompts_data)
    print(f"找到 {total_prompts} 个prompts待处理\n")
    
    if total_prompts == 0:
        print("✗ 没有找到任何prompts需要处理")
        return
    
    # 记录开始时间
    start_time = time.time()
    
    # 使用线程池并发处理
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_project = {
            executor.submit(
                process_single_prompt,
                item["project_name"],
                item["prompt_content"],
                input_jsonl,
                output_file
            ): item["project_name"]
            for item in prompts_data
        }
        
        # 处理完成的任务
        completed = 0
        for future in as_completed(future_to_project):
            project_name = future_to_project[future]
            try:
                result = future.result()
                results.append(result)
                completed += 1
                print(f"\n进度: [{completed}/{total_prompts}] 完成")
            except Exception as e:
                print(f"\n✗ 处理 {project_name} 时发生异常: {e}")
                results.append({
                    "project": project_name,
                    "status": "error",
                    "reason": str(e)
                })
                completed += 1
    
    # 计算统计信息
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    success_count = sum(1 for r in results if r.get("status") == "success")
    failed_count = sum(1 for r in results if r.get("status") in ["failed", "error"])
    
    # 输出最终统计
    print(f"\n\n{'='*80}")
    print(f"所有任务完成！")
    print(f"{'='*80}")
    print(f"总prompts数: {total_prompts}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"成功率: {success_count/total_prompts*100:.1f}%")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"平均耗时: {elapsed_time/total_prompts:.2f} 秒/prompt")
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
    # 输入文件路径
    input_jsonl = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/generated_prompt/prompts_20260129_141125.jsonl"
    output_dir = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/summaried_prompt"
    
    # 使用10个并发线程处理
    results = process_prompts_concurrent(input_jsonl, output_dir, max_workers=MAX_WORKERS)
    
    # 可选：保存详细的结果报告
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/summaried_prompt/report_{timestamp}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump({
                "input_file": input_jsonl,
                "timestamp": timestamp,
                "total": len(results),
                "results": results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"详细报告已保存到: {report_file}")
