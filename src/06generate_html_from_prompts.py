"""
从多级别Prompt生成HTML代码

功能：读取多级别prompt文件，使用不同详细程度的prompt让模型生成HTML代码
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
INPUT_JSONL_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/05expanded_prompts/multi_level_prompts_20260130_113627.jsonl"
OUTPUT_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/06generated_html"
MAX_WORKERS = 40  # 并发工作线程数

# 可以选择生成哪些详细程度的版本
GENERATE_LEVELS = ["minimal", "simple", "medium", "detailed"]  # 可以根据需要调整


def read_prompts_from_jsonl(jsonl_file):
    """从JSONL文件读取所有多级别prompts
    
    Args:
        jsonl_file: JSONL文件路径
    
    Returns:
        list: 包含所有项目数据的列表
    """
    projects = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    projects.append({
                        "line_number": line_num,
                        "project_name": data.get("project_name", ""),
                        "category": data.get("category", ""),
                        "subcategory": data.get("subcategory", ""),
                        "detailed_category": data.get("detailed_category", ""),
                        "prompts": data.get("prompts", {}),
                        "metadata": data.get("metadata", {})
                    })
                except json.JSONDecodeError as e:
                    print(f"✗ 解析第 {line_num} 行时出错: {e}")
                    continue
    return projects


def generate_html(client, project_name, prompt_text, detail_level):
    """调用模型根据prompt生成HTML代码
    
    Args:
        client: OpenAI客户端
        project_name: 项目名称
        prompt_text: prompt文本
        detail_level: 详细程度级别
    
    Returns:
        str: 生成的HTML代码
    """
    # 根据详细程度级别设置不同的system message
    if detail_level == "detailed":
        system_message = """你是一个专业的Web前端开发专家。请将代码放在```html ```代码块中。"""
        user_message = f"""项目名称：{project_name}

需求描述：
{prompt_text}

如果需求描述中的某些需求、参数等不合理，可以适当修改。请将代码放在```html ```代码块中。"""
    elif detail_level == "medium":
        system_message = """你是一个专业的Web前端开发专家。请生成完整的单文件HTML页面代码，并将代码放在```html ```代码块中。"""
        user_message = f"""项目名称：{project_name}

需求描述：
{prompt_text}

如果需求描述中的某些需求、参数等不合理，可以适当修改。请生成HTML页面代码，并放在```html ```代码块中。"""
    else:
        system_message = """你是一个专业的Web前端开发专家。请生成完整的单文件HTML页面代码，并将代码放在```html ```代码块中。"""
        user_message = f"""项目名称：{project_name}

需求描述：
{prompt_text}

请生成HTML页面代码，并放在```html ```代码块中。"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            timeout=600.0,  # 设置600秒超时
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
                        # 结束代码块
                        break
                    else:
                        # 开始代码块
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


def process_single_project(client, project_data, idx, total):
    """处理单个项目，生成指定详细程度的HTML文件
    
    Args:
        client: OpenAI客户端
        project_data: 项目数据字典
        idx: 当前索引
        total: 总数量
    
    Returns:
        dict: 处理结果
    """
    project_name = project_data["project_name"]
    prompts = project_data["prompts"]
    
    print(f"[{idx}/{total}] 正在处理: {project_name}")
    
    results = {
        "project_name": project_name,
        "category": project_data["category"],
        "subcategory": project_data["subcategory"],
        "detailed_category": project_data["detailed_category"],
        "generated_files": {},
        "full_responses": {},
        "status": {}
    }
    
    # 为每个详细程度级别生成HTML
    for level in GENERATE_LEVELS:
        prompt_text = prompts.get(level)
        if not prompt_text:
            print(f"  - {level}: ✗ 缺少prompt")
            results["status"][level] = "missing_prompt"
            continue
        
        print(f"  - {level}: 生成中...", end=" ")
        result = generate_html(client, project_name, prompt_text, level)
        
        if result:
            results["generated_files"][level] = result["html_code"]
            results["full_responses"][level] = result["full_response"]
            results["status"][level] = "success"
            print(f"✓ ({len(result['html_code'])}字符)")
        else:
            results["status"][level] = "failed"
            print(f"✗ 失败")
    
    return results


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
        "saved_by_level": {level: 0 for level in GENERATE_LEVELS}
    }
    
    for result in results:
        project_name = result["project_name"]
        # 清理项目名称，用作文件夹名
        safe_project_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in project_name)
        
        project_dir = os.path.join(output_base_dir, safe_project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        for level, html_code in result["generated_files"].items():
            # 保存HTML文件
            filename = f"{safe_project_name}_{level}.html"
            filepath = os.path.join(project_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_code)
            
            # 保存完整响应
            if level in result.get("full_responses", {}):
                full_response_filename = f"{safe_project_name}_{level}_full_response.txt"
                full_response_filepath = os.path.join(project_dir, full_response_filename)
                
                with open(full_response_filepath, "w", encoding="utf-8") as f:
                    f.write(result["full_responses"][level])
            
            stats["total_files"] += 1
            stats["saved_by_level"][level] += 1
    
    return stats


def main():
    """主函数"""
    print(f"{'='*80}")
    print(f"多级别Prompt HTML生成工具")
    print(f"{'='*80}")
    print(f"输入文件: {INPUT_JSONL_FILE}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"并发线程数: {MAX_WORKERS}")
    print(f"生成级别: {', '.join(GENERATE_LEVELS)}")
    print(f"{'='*80}\n")
    
    # 读取prompts
    print("正在读取prompts...")
    projects = read_prompts_from_jsonl(INPUT_JSONL_FILE)
    print(f"✓ 读取了 {len(projects)} 个项目\n")
    
    if not projects:
        print("✗ 没有找到任何项目")
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
            executor.submit(process_single_project, client, project, idx, len(projects)): project
            for idx, project in enumerate(projects, 1)
        }
        
        for future in as_completed(futures):
            try:
                result = future.result()
                with results_lock:
                    all_results.append(result)
            except Exception as e:
                print(f"  ✗ 处理任务时出错: {e}")
    
    # 统计结果
    print(f"\n{'='*80}")
    print(f"生成完成！")
    print(f"{'='*80}")
    
    total_success = 0
    level_success = {level: 0 for level in GENERATE_LEVELS}
    
    for result in all_results:
        for level, status in result["status"].items():
            if status == "success":
                total_success += 1
                level_success[level] += 1
    
    print(f"总项目数: {len(all_results)}")
    print(f"总成功生成: {total_success} 个HTML文件")
    print(f"\n各级别成功数:")
    for level in GENERATE_LEVELS:
        print(f"  - {level}: {level_success[level]}")
    
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
            "total_files": save_stats['total_files'],
            "generate_levels": GENERATE_LEVELS,
            "max_workers": MAX_WORKERS
        },
        "statistics": {
            "success_by_level": level_success,
            "saved_by_level": save_stats['saved_by_level']
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
