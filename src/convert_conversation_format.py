"""
将prompt和response转换为对话格式的JSONL

读取prompt文件和generation report,转换成对话格式
"""

import os
import json
import shutil
from datetime import datetime


# 配置变量
PROMPT_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/05expanded_prompts/multi_level_prompts_20260130_113627.jsonl"
GENERATION_REPORT_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/06generated_html/generation_report_20260201_195002.json"
OUTPUT_BASE_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/07conversation_format"
LEVELS = ["minimal", "simple", "medium", "detailed"]


def load_prompts(jsonl_file):
    """读取prompt文件"""
    prompts_dict = {}
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                project_name = data.get("project_name", "")
                prompts_dict[project_name] = data
    return prompts_dict


def load_generation_report(json_file):
    """读取generation report文件"""
    print(f"正在读取generation report: {os.path.basename(json_file)}")
    results_dict = {}
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        results = data.get("results", [])
        
        for result in results:
            project_name = result.get("project_name", "")
            if project_name:
                results_dict[project_name] = result
    
    print(f"✓ 加载了 {len(results_dict)} 个项目的生成结果")
    return results_dict


def clean_project_name(name):
    """清理项目名称"""
    return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)


def build_user_message(prompt_text, detail_level):
    """构建user message"""
    if detail_level == "detailed":
        return prompt_text
    else:
        return f"写到一个html中。\n{prompt_text}"


def main():
    """主函数"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(OUTPUT_BASE_DIR, f"conversations_{timestamp}")
    
    print(f"{'='*80}")
    print(f"转换为对话格式工具")
    print(f"{'='*80}")
    print(f"Prompt文件: {PROMPT_FILE}")
    print(f"Generation Report: {GENERATION_REPORT_FILE}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*80}\n")
    
    # 加载数据
    print("正在加载prompts...")
    prompts_dict = load_prompts(PROMPT_FILE)
    print(f"✓ 加载了 {len(prompts_dict)} 个项目的prompts\n")
    
    results_dict = load_generation_report(GENERATION_REPORT_FILE)
    print()
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 复制输入文件
    print("正在复制输入文件...")
    shutil.copy2(PROMPT_FILE, os.path.join(output_dir, os.path.basename(PROMPT_FILE)))
    print(f"✓ 已复制: {os.path.basename(PROMPT_FILE)}")
    
    shutil.copy2(GENERATION_REPORT_FILE, os.path.join(output_dir, os.path.basename(GENERATION_REPORT_FILE)))
    print(f"✓ 已复制: {os.path.basename(GENERATION_REPORT_FILE)}\n")
    
    # 统计信息
    stats = {
        "total_projects": 0,
        "total_conversations": 0,
        "by_level": {level: {"success": 0, "missing": 0} for level in LEVELS}
    }
    
    # 打开输出文件
    output_files = {}
    for level in LEVELS:
        output_files[level] = open(os.path.join(output_dir, f"conversations_{level}.jsonl"), "w", encoding="utf-8")
    
    # 处理所有项目
    print("开始转换...\n")
    for project_name, project_data in prompts_dict.items():
        stats["total_projects"] += 1
        safe_name = clean_project_name(project_name)
        
        category = project_data.get("category", "")
        subcategory = project_data.get("subcategory", "")
        detailed_category = project_data.get("detailed_category", "")
        prompts = project_data.get("prompts", {})
        
        result_data = results_dict.get(project_name)
        if not result_data:
            print(f"⚠ 跳过 {project_name}: 在generation report中未找到")
            for level in LEVELS:
                stats["by_level"][level]["missing"] += 1
            continue
        
        full_responses = result_data.get("full_responses", {})
        if not full_responses:
            print(f"⚠ 跳过 {project_name}: 没有full_responses数据")
            for level in LEVELS:
                stats["by_level"][level]["missing"] += 1
            continue
        
        print(f"处理: {project_name}")
        
        for level in LEVELS:
            prompt_text = prompts.get(level)
            if not prompt_text:
                print(f"  - {level}: ✗ 缺少prompt")
                stats["by_level"][level]["missing"] += 1
                continue
            
            response_text = full_responses.get(level)
            if not response_text:
                print(f"  - {level}: ✗ 缺少response")
                stats["by_level"][level]["missing"] += 1
                continue
            
            user_content = build_user_message(prompt_text, level)
            
            conversation = {
                "project_name": project_name,
                "filename": f"{safe_name}_{level}.html",
                "category": category,
                "subcategory": subcategory,
                "detailed_category": detailed_category,
                "level": level,
                "messages": [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text}
                ]
            }
            
            output_files[level].write(json.dumps(conversation, ensure_ascii=False) + "\n")
            
            stats["total_conversations"] += 1
            stats["by_level"][level]["success"] += 1
            print(f"  - {level}: ✓ 转换成功")
    
    # 关闭文件
    for f in output_files.values():
        f.close()
    
    # 输出统计
    print(f"\n{'='*80}")
    print(f"转换完成!")
    print(f"{'='*80}")
    print(f"总项目数: {stats['total_projects']}")
    print(f"总对话数: {stats['total_conversations']}")
    print(f"\n各级别统计:")
    for level in LEVELS:
        success = stats['by_level'][level]['success']
        missing = stats['by_level'][level]['missing']
        print(f"  {level}: 成功={success}, 缺失={missing}")
    
    print(f"\n输出目录: {output_dir}")
    print(f"\n{'='*80}")
    print(f"✓ 任务完成!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
