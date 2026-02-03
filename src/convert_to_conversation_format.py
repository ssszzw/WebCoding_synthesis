"""
将prompt和response转换为对话格式的JSONL

读取prompt文件和生成的HTML响应,转换成对话格式:
{"messages": [{"role": "user", "content": "prompt"}, {"role": "assistant", "content": "response"}]}
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime


# 配置变量
PROMPT_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/05expanded_prompts/multi_level_prompts_20260130_113627.jsonl"
GENERATION_REPORT_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/06generated_html/generation_report_20260201_195002.json"
OUTPUT_BASE_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/07conversation_format"
LEVELS = ["minimal", "simple", "medium", "detailed"]


def load_prompts(jsonl_file):
    """读取prompt文件
    
    Args:
        jsonl_file: JSONL文件路径
    
    Returns:
        dict: 以project_name为key的完整数据字典
    """
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
    """读取generation report文件
    
    Args:
        json_file: JSON文件路径
    
    Returns:
        dict: 以project_name为key的结果字典
    """
    print(f"正在读取generation report: {json_file}")
    results_dict = {}
    
    # 由于文件太大,我们需要流式读取
    with open(json_file, "r", encoding="utf-8") as f:
        # 读取整个JSON文件
        data = json.load(f)
        results = data.get("results", [])
        
        for result in results:
            project_name = result.get("project_name", "")
            if project_name:
                results_dict[project_name] = result
    
    print(f"✓ 加载了 {len(results_dict)} 个项目的生成结果")
    return results_dict


def clean_project_name(name):
    """清理项目名称,转换为文件夹名称
    
    Args:
        name: 原始项目名称
    
    Returns:
        str: 清理后的名称
    """
    return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)


def build_system_prompt(detail_level):
    """根据详细程度构建system prompt
    
    Args:
        detail_level: 详细程度级别
    
    Returns:
        str: system prompt内容
    """
    if detail_level == "detailed":
        return "你是一个专业的Web前端开发专家。请将代码放在```html ```代码块中。"
    elif detail_level == "medium":
        return "你是一个专业的Web前端开发专家。请生成完整的单文件HTML页面代码,并将代码放在```html ```代码块中。"
    else:
        return "你是一个专业的Web前端开发专家。请生成完整的单文件HTML页面代码,并将代码放在```html ```代码块中。"


def build_user_message(project_name, prompt_text, detail_level):
    """构建user message
    Generation Report: {GENERATION_REPORT_FILE}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*80}\n")
    
    # 加载prompts
    print("正在加载prompts...")
    prompts_dict = load_prompts(PROMPT_FILE)
    print(f"✓ 加载了 {len(prompts_dict)} 个项目的prompts\n")
    
    # 加载generation report
    results_dict = load_generation_report(GENERATION_REPORT_FILE)
    print(
    """
    if detail_level == "detailed":
        # detailed级别直接返回原始prompt
        return prompt_text
    else:
        # 其他级别添加"写到一个html中"的提示
        return f"写到一个html中。\n{prompt_text}"


def convert_to_conversation_format():
    """主函数:转换prompt和response为对话格式"""
    # 生成带时间戳的输出目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(OUTPUT_BASE_DIR, f"conversations_{timestamp}")
    
    print(f"{'='*80}")
    print(f"转换为对话格式工具")
    print(f"{'='*80}")
    print(f"Prompt文件: {PROMPT_FILE}")
    print(f"生成HTML目录: {GENERATED_HTML_DIR}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*80}\n")
    
    # 加载prompts
    print("正在加载prompts...")
    prompts_dict = load_prompts(PROMPT_FILE)
    print(f"✓ 加载了 {len(prompts_dict)} 个项目的prompts\n")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 复制输入的prompt文件到输出目录
    print("正在复制输入文件...")
    prompt_filename = os.path.basename(PROMPT_FILE)
    shutil.copy2(PROMPT_FILE, os.path.join(output_dir, prompt_filename))
    print(f"✓ 已复制: {prompt_filename}\n")
    
    # 统计信息
    stats = {
        "total_projects": 0,
        "total_conversations": 0,
        "by_level": {level: {"success": 0, "missing": 0} for level in LEVELS}
    }
    
    # 为每个级别创建单独的输出文件
    output_files = {}
    for level in LEVELS:
        output_file = os.path.join(output_dir, f"conversations_{level}.jsonl")
        output_files[level] = open(output_file, "w", encoding="utf-8")
    
    # 遍历所有项目
    prin
        # 提取项目元数据
        category = project_data.get("category", "")
        subcategory = project_data.get("subcategory", "")
        detailed_category = project_data.get("detailed_category", "")
        prompts = project_data.get("prompts", {})
        
        # 从generation report中获取结果
        result_data = results_dict.get(project_name)
        if not result_data:
            print(f"⚠ 跳过 {project_name}: 在generation report中未找到")
            for level in LEVELS:
                stats["by_level"][level]["missing"] += 1
            continue
        
        # 获取full_responses
        full_responses = result_data.get("full_responses", {})
        if not full_responses:
            print(f"⚠ 跳过 {project_name}: 没有full_responses数据")
            for level in LEVELS:
                stats["by_level"][level]["missing"] += 1
            continue
        
        print(f"处理: {project_name}")
        
        # 处理每个级别
        for level in LEVELS:
            prompt_text = prompts.get(level)
            if not prompt_text:
                print(f"  - {level}: ✗ 缺少prompt")
                stats["by_level"][level]["missing"] += 1
                continue
            
            # 从full_responses中获取response
            response_text = full_responses.get(level)
            if not response_text:
                print(f"  - {level}: ✗ 缺少response
                with open(response_file, "r", encoding="utf-8") as f:
                    response_text = f.read()
            except Exception as e:
                print(f"  - {level}: ✗ 读取response失败: {e}")
                stats["by_level"][level]["missing"] += 1
                continue
            
            # 构建对话格式
            user_content = build_user_message(project_name, prompt_text, level)
            
            conversation = {
                "project_name": project_name,
                "filename": f"{safe_name}_{level}.html",
                "category": category,
                "subcategory": subcategory,
                "detailed_category": detailed_category,
                "level": level,
                "messages": [
                    {
                        "role": "user",
                        "content": user_content
                    },
                    {
                        "role": "assistant",
                        "content": response_text
                    }
                ]
            }
            
            # 写入对应级别的文件
            output_files[level].write(json.dumps(conversation, ensure_ascii=False) + "\n")
            
            stats["total_conversations"] += 1
            stats["by_level"][level]["success"] += 1
            print(f"  - {level}: ✓ 转换成功")
    
    # 关闭所有输出文件
    for f in output_files.values():
        f.close()
    
    # 输出统计信息
    print(f"\n{'='*80}")
    print(f"转换完成!")
    print(f"{'='*80}")
    print(f"总项目数: {stats['total_projects']}")
    print(f"总对话数: {stats['total_conversations']}")
    print(f"\n各级别统计:")
    for level in LEVELS:
        success = stats['by_level'][level]['success']
        missing = stats['by_level'][level]['missing']
        print(f"  {level}:")
        print(f"    - 成功: {success}")
        print(f"    - 缺失: {missing}")
        print(f"    - 输出: {output_files[level].name if level in output_files else 'N/A'}")
    
    print(f"\n{'='*80}")
    print(f"✓ 任务完成!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    convert_to_conversation_format()
