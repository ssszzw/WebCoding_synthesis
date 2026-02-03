"""
从refresh的prompt生成HTML代码

功能：读取refresh后的prompt文件，使用prompt让模型生成HTML代码
"""

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
INPUT_JSONL_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/01generated_prompt/prompts_20260129_141125_refresh.jsonl"
OUTPUT_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/06generated_html_from_refresh"
MAX_WORKERS = 50  # 并发工作线程数


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
                    prompts.append({
                        "line_number": line_num,
                        "project_name": data.get("project_name", ""),
                        "prompt": data.get("prompt", ""),
                        "metadata": data.get("metadata", {})
                    })
                except json.JSONDecodeError as e:
                    print(f"✗ 解析第 {line_num} 行时出错: {e}")
                    continue
    return prompts


def generate_html(client, project_name, prompt_text):
    """调用模型根据prompt生成HTML代码
    
    Args:
        client: OpenAI客户端
        project_name: 项目名称
        prompt_text: prompt文本
    
    Returns:
        dict: 包含html_code和full_response的字典
    """
    system_message = """你是一个专业的Web前端开发专家。请将代码放在```html ```代码块中。"""

    user_message = f"""项目名称：{project_name}

需求描述：
{prompt_text}

如果需求描述中的某些需求不合理，可以适当修改。请将代码放在```html ```代码块中。"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            timeout=180.0,
        )
        
        full_response = completion.choices[0].message.content.strip()
        
        # 从```html ```代码块中提取HTML代码
        html_code = None
        
        # 查找```html和```之间的内容
        if "```html" in full_response:
            start_marker = "```html"
            start_idx = full_response.find(start_marker)
            if start_idx != -1:
                # 跳过```html和后面的换行
                code_start = start_idx + len(start_marker)
                # 查找结束的```
                end_idx = full_response.find("```", code_start)
                if end_idx != -1:
                    html_code = full_response[code_start:end_idx].strip()
        
        # 如果没找到```html，尝试查找普通的```代码块
        if not html_code and "```" in full_response:
            lines = full_response.split("\n")
            in_code_block = False
            code_lines = []
            for line in lines:
                if line.strip().startswith("```"):
                    if in_code_block:
                        break
                    else:
                        in_code_block = True
                        continue
                if in_code_block:
                    code_lines.append(line)
            if code_lines:
                html_code = "\n".join(code_lines).strip()
        
        # 如果还是没找到，查找<!DOCTYPE html>开头的内容
        if not html_code and "<!DOCTYPE html>" in full_response:
            start_idx = full_response.find("<!DOCTYPE html>")
            html_code = full_response[start_idx:].strip()
        
        if not html_code:
            # 如果都没找到，返回完整响应
            html_code = full_response
        
        return {"html_code": html_code, "full_response": full_response}
        
    except Exception as e:
        print(f"  ✗ 生成失败：{e}")
        return None


def process_single_project(client, prompt_data, idx, total):
    """处理单个项目，生成HTML文件
    
    Args:
        client: OpenAI客户端
        prompt_data: prompt数据字典
        idx: 当前索引
        total: 总数量
    
    Returns:
        dict: 处理结果
    """
    project_name = prompt_data["project_name"]
    prompt_text = prompt_data["prompt"]
    
    print(f"[{idx}/{total}] 正在处理: {project_name}")
    
    result = generate_html(client, project_name, prompt_text)
    
    if result:
        print(f"  ✓ 生成成功 ({len(result['html_code'])}字符)")
        return {
            "status": "success",
            "project_name": project_name,
            "html_code": result["html_code"],
            "full_response": result["full_response"],
            "metadata": prompt_data["metadata"]
        }
    else:
        print(f"  ✗ 生成失败")
        return {
            "status": "failed",
            "project_name": project_name,
            "error": "Generation failed"
        }


def save_html_files(results, output_base_dir):
    """保存生成的HTML文件
    
    Args:
        results: 处理结果列表
        output_base_dir: 输出基础目录
    
    Returns:
        dict: 保存统计信息
    """
    stats = {
        "total_files": 0,
        "successful": 0,
        "failed": 0
    }
    
    for result in results:
        if result["status"] != "success":
            stats["failed"] += 1
            continue
            
        project_name = result["project_name"]
        # 清理项目名称，用作文件夹名
        safe_project_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in project_name)
        
        project_dir = os.path.join(output_base_dir, safe_project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        # 保存HTML文件
        html_filename = f"{safe_project_name}.html"
        html_filepath = os.path.join(project_dir, html_filename)
        
        with open(html_filepath, "w", encoding="utf-8") as f:
            f.write(result["html_code"])
        
        # 保存完整响应
        full_response_filename = f"{safe_project_name}_full_response.txt"
        full_response_filepath = os.path.join(project_dir, full_response_filename)
        
        with open(full_response_filepath, "w", encoding="utf-8") as f:
            f.write(result["full_response"])
        
        stats["total_files"] += 1
        stats["successful"] += 1
    
    return stats


def main():
    """主函数"""
    print(f"{'='*80}")
    print(f"从Refresh Prompts生成HTML工具")
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
    
    # 并发处理所有项目
    all_results = []
    results_lock = threading.Lock()
    
    print(f"开始并发生成HTML（{MAX_WORKERS}个工作线程）...\n")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_single_project, client, prompt, idx, len(prompts)): prompt
            for idx, prompt in enumerate(prompts, 1)
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
    print(f"生成完成！")
    print(f"{'='*80}")
    print(f"总数: {len(all_results)}")
    print(f"成功: {len(successful)}")
    print(f"失败: {len(failed)}")
    
    # 保存HTML文件
    print(f"\n正在保存HTML文件...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(OUTPUT_DIR, f"generated_{timestamp}")
    
    save_stats = save_html_files(all_results, output_dir)
    print(f"✓ 已保存 {save_stats['total_files']} 个HTML文件到: {output_dir}")
    
    # 保存生成报告
    report_file = os.path.join(OUTPUT_DIR, f"generation_report_{timestamp}.json")
    report_data = {
        "metadata": {
            "input_file": INPUT_JSONL_FILE,
            "output_dir": output_dir,
            "processing_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "timestamp": timestamp,
            "total_projects": len(all_results),
            "successful": len(successful),
            "failed": len(failed),
            "max_workers": MAX_WORKERS
        },
        "statistics": {
            "total_files": save_stats["total_files"],
            "successful": save_stats["successful"],
            "failed": save_stats["failed"]
        },
        "results": all_results
    }
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"详细报告已保存到: {report_file}")
    
    print(f"\n{'='*80}")
    print(f"✓ 任务完成！")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
