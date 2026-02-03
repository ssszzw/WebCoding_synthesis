"""
多级别Prompt生成工具

功能说明：
为每个项目提供4种详细程度的版本：
- minimal: 最简单版本 (1-2句话，粗略描述，某些方面可含糊不清) - **需生成，参考simple**
- simple: 简单版本 (3-4句话描述主要需求) - **已存在，无需生成**（summary/description）
- medium: 中间版本 (包含主要细节，省略不那么关键的部分) - **需生成，参考simple+detailed**
- detailed: 详细版本 (尽可能详细地描述各种细节) - **需生成，参考simple+existing_prompts详细示例**

数据来源说明：
1. REFRESH_JSONL_FILE (48条): 
   - 包含部分existing_prompts的详细描述
   - 用作detailed版本的参考示例
   - 对于这48个existing项目，直接使用作为detailed版本

2. CATEGORY_JSON_FILE:
   - existing_prompts (48个): 每个有name和summary
     * summary本身就是simple版本，无需生成
     * 需要生成: minimal, medium
     * detailed: 直接使用refresh中的版本
   - generated_prompts (600个): 每个有name和description
     * description本身就是simple版本，无需生成
     * 需要生成: minimal, medium, detailed

处理逻辑总结：
- 总共处理: 48 (existing) + 600 (generated) = 648个项目
- existing_prompts: simple已有（summary），detailed已有（refresh），按顺序生成minimal和medium
- generated_prompts: simple已有（description），按顺序生成minimal、detailed和medium
- 生成顺序: minimal（参考simple） → detailed（参考simple+existing_prompts） → medium（参考simple+detailed）
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
REFRESH_JSONL_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/01generated_prompt/prompts_20260129_141125_refresh.jsonl"
CATEGORY_JSON_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/04generated_prompts_by_category/generated_prompts_by_category_20260129_165049.json"
OUTPUT_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/05expanded_prompts"
MAX_WORKERS = 50  # 并发工作线程数

# 定义4种详细程度
DETAIL_LEVELS = {
    "minimal": {
        "name": "最简单版本",
        "description": "1-2句话粗略描述，某些方面可以含糊不清"
    },
    "simple": {
        "name": "简单版本",
        "description": "3-4句话描述主要需求"
    },
    "medium": {
        "name": "中间版本",
        "description": "包含主要细节，省略不那么关键的部分"
    },
    "detailed": {
        "name": "详细版本",
        "description": "尽可能详细地描述各种细节"
    }
}


def read_refresh_prompts(jsonl_file):
    """读取清理后的prompts作为例子
    
    Returns:
        dict: {project_name: prompt_text}
    """
    prompts_dict = {}
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    project_name = data.get("project_name", "")
                    prompt = data.get("prompt", "")
                    if project_name and prompt:
                        prompts_dict[project_name] = prompt
                except json.JSONDecodeError as e:
                    print(f"✗ 解析JSONL行时出错: {e}")
                    continue
    return prompts_dict


def read_category_data(json_file):
    """读取分类数据
    
    Returns:
        dict: 完整的分类数据
    """
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def expand_prompt(client, project_name, short_description, example_prompts, category_info, detail_level, generated_prompts=None):
    """调用模型生成指定详细程度的prompt
    
    Args:
        client: OpenAI客户端
        project_name: 项目名称
        short_description: 简短描述（simple版本）
        example_prompts: 同类别的existing_prompts列表（含summary和详细描述）
        category_info: 类别信息
        detail_level: 详细程度 (minimal/medium/detailed)
        generated_prompts: 已生成的其他版本prompt（用于medium版本）
    
    Returns:
        str: 生成的prompt
    """
    level_info = DETAIL_LEVELS[detail_level]
    
    # 构建示例文本
    examples_text = ""
    
    if detail_level == "minimal":
        # 最简单版本：使用当前项目的simple版本作为示例
        examples_text = f"参考的简单版本描述:\n{short_description}"
        
    elif detail_level == "detailed":
        # 详细版本：使用simple版本 + existing_prompts的详细描述作为示例
        examples = []
        
        # 1. 当前项目的simple版本
        examples.append(f"当前项目的简单版本:\n{short_description}")
        
        # 2. 同类别existing_prompts的详细描述（最多4个）
        detailed_examples = []
        for ex in example_prompts[:4]:
            if 'prompt' in ex and ex['prompt']:
                detailed_examples.append(f"同类别示例 {len(detailed_examples)+1} - {ex['name']}:\n{ex['prompt']}")
        
        if detailed_examples:
            examples.append("\n同类别的详细版本示例:\n" + "\n\n".join(detailed_examples))
        else:
            examples.append("\n（同类别暂无详细示例，请根据简单版本尽可能详细地扩展）")
        
        examples_text = "\n\n".join(examples)
        
    elif detail_level == "medium":
        # 中间版本：使用simple版本 + 已生成的detailed版本作为示例
        examples = []
        
        # 1. 当前项目的simple版本
        examples.append(f"简单版本:\n{short_description}")
        
        # 2. 当前项目的detailed版本（如果已生成）
        if generated_prompts and 'detailed' in generated_prompts and generated_prompts['detailed']:
            examples.append(f"\n详细版本:\n{generated_prompts['detailed']}")
        else:
            examples.append("\n（详细版本尚未生成，请根据简单版本适度扩展）")
        
        examples_text = "\n\n".join(examples)
    
    # 构建四个详细程度的说明
    all_levels_desc = "\n".join([
        f"- {DETAIL_LEVELS[k]['name']} ({k}): {DETAIL_LEVELS[k]['description']}"
        for k in ['minimal', 'simple', 'medium', 'detailed']
    ])
    
    system_message = f"""你是一个专业的Web前端项目提示信息撰写专家。你的任务是根据项目描述生成提示信息。

**当前项目所属类别**：
- 大类：{category_info['category']}
- 次类：{category_info['subcategory']}
- 细类：{category_info['detailed_category']}
  描述：{category_info['detailed_category_desc']}

**技术约束范围**（仅作为任务边界参考，不需要在输出中显式说明，不要在输出中提及这里的技术约束，只是给你作为参考来生成合理范围内的prompt）：
- 所有功能使用标准Web技术实现（HTML5、CSS3、JavaScript ES6+、Canvas、WebGL、SVG等）
- 不依赖外部服务或后端

**四个详细程度级别说明**：
{all_levels_desc}

**本次生成的详细程度要求：{level_info['name']}**
{level_info['description']}

**输出要求**：
- 只输出提示信息本身，不要输出代码或HTML文件
- 不要包含"添加注释"等代码注释要求
- 格式不限，用你认为最合适的方式组织内容
- **重要**：不要在生成的prompt中包含类似"编写一个包含 HTML、CSS 和 JavaScript 的单文件 Web 项目（index.html）"这种元信息或技术实现说明，只描述项目的功能需求、交互设计、视觉效果等

**参考信息**：
{examples_text}"""

    # 根据detail_level调整user_message
    if detail_level == "minimal":
        user_message = f"""项目名称：{project_name}

---

请生成{level_info['name']}的提示信息：{level_info['description']}。
基于上面的简单版本描述，用1-2句话粗略概括项目核心功能，某些细节可以含糊不清。
只输出提示信息，不要输出代码。"""
        
    elif detail_level == "medium":
        user_message = f"""项目名称：{project_name}

---

请生成{level_info['name']}的提示信息：{level_info['description']}。
参考上面的简单版本和详细版本，生成一个介于两者之间的中间版本。
包含核心功能、主要交互逻辑、基本UI设计，但省略次要细节。

**特别注意（仅针对中间版本）**：
- 绝对不要包含"编写一个包含 HTML、CSS 和 JavaScript 的单文件 Web 项目（index.html）"等技术实现说明
- 不要包含文件结构说明（如"创建index.html文件"）
- 不要包含具体技术栈指令（如"使用Canvas"、"使用WebGL"、"使用SVG"等）
- 只描述功能需求、用户交互方式、视觉效果、界面布局等产品层面的内容
- 专注于"做什么"而不是"用什么技术做"

只输出提示信息，不要输出代码。"""
        
    else:  # detailed
        user_message = f"""项目名称：{project_name}

---

请生成{level_info['name']}的提示信息：{level_info['description']}。
参考上面的简单版本描述和同类别的详细示例，生成完整详细的提示信息。
包含完整的功能说明、技术实现细节、UI/UX设计、交互流程、视觉效果等。
只输出提示信息，不要输出代码。"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        
        expanded_prompt = completion.choices[0].message.content.strip()
        return expanded_prompt
        
    except Exception as e:
        print(f"  ✗ 扩展失败：{e}")
        return None


def process_single_project(client, project_data, refresh_prompts, idx, total):
    """处理单个项目，按顺序生成3种详细程度的prompt（simple已存在）
    
    生成顺序：
    1. minimal: 使用simple作为参考示例
    2. detailed: 使用simple + 同类别existing_prompts的详细描述作为示例（如已在refresh中则直接使用）
    3. medium: 使用simple + 刚生成的detailed作为示例
    
    Args:
        client: OpenAI客户端
        project_data: 项目数据字典
        refresh_prompts: 清理后的prompts字典（existing_prompts的detailed版本）
        idx: 当前索引
        total: 总数量
    
    Returns:
        dict: 处理结果（包含4个版本的prompt）
    """
    project_name = project_data["name"]
    short_description = project_data["description"]  # 这就是simple版本
    category_info = project_data["category_info"]
    existing_prompts = project_data["existing_prompts"]
    
    # 准备示例prompts（包含existing_prompts的详细描述）
    example_prompts = []
    for ep in existing_prompts:
        ep_name = ep.get("name", "")
        ep_data = {
            "name": ep_name,
            "summary": ep.get("summary", "")
        }
        # 添加详细版本（如果在refresh中存在）
        if ep_name in refresh_prompts:
            ep_data["prompt"] = refresh_prompts[ep_name]
        example_prompts.append(ep_data)
    
    detailed_example_count = len([e for e in example_prompts if 'prompt' in e and e['prompt']])
    
    # 检查当前项目是否在refresh中已有详细描述
    has_existing_detailed = project_name in refresh_prompts
    
    # 初始化结果，simple版本直接使用现有描述
    results = {
        "simple": short_description  # simple版本不需要生成
    }
    
    all_success = True
    
    # 步骤1: 生成minimal版本（使用simple作为示例）
    minimal_prompt = expand_prompt(
        client, project_name, short_description, example_prompts, 
        category_info, "minimal", generated_prompts=None
    )
    if minimal_prompt:
        results["minimal"] = minimal_prompt
    else:
        all_success = False
        results["minimal"] = None
    
    # 步骤2: 生成或使用detailed版本
    if has_existing_detailed:
        # 直接使用现有的detailed版本
        results["detailed"] = refresh_prompts[project_name]
    else:
        # 生成detailed版本（使用simple + existing_prompts作为示例）
        detailed_prompt = expand_prompt(
            client, project_name, short_description, example_prompts, 
            category_info, "detailed", generated_prompts=None
        )
        if detailed_prompt:
            results["detailed"] = detailed_prompt
        else:
            all_success = False
            results["detailed"] = None
    
    # 步骤3: 生成medium版本（使用simple + detailed作为示例）
    medium_prompt = expand_prompt(
        client, project_name, short_description, example_prompts, 
        category_info, "medium", generated_prompts=results
    )
    if medium_prompt:
        results["medium"] = medium_prompt
    else:
        all_success = False
        results["medium"] = None
    
    # 确保4个版本都存在（即使某些是None）
    for level_key in DETAIL_LEVELS.keys():
        if level_key not in results:
            results[level_key] = None
    
    # 构建一次性输出（避免并发时打印混乱）
    status = "✓" if (all_success and all(results.values())) else "✗"
    lengths = " | ".join([
        f"{DETAIL_LEVELS[k]['name'][:2]}:{len(results[k]) if results[k] else 0:4d}字"
        for k in ['minimal', 'simple', 'medium', 'detailed']
    ])
    output = f"[{idx}/{total}] {status} {project_name} ({category_info['detailed_category']}) | {lengths} | 示例:{detailed_example_count}"
    print(output)
    
    if all_success and all(results.values()):
        return {
            "status": "success",
            "project_name": project_name,
            "category_info": category_info,
            "prompts": results,
            "lengths": {k: len(v) if v else 0 for k, v in results.items()},
            "example_count": len(example_prompts),
            "detailed_example_count": detailed_example_count,
            "used_existing_detailed": has_existing_detailed,
            "is_existing": project_data.get("is_existing", False)
        }
    else:
        return {
            "status": "partial" if any(results.values()) else "failed",
            "project_name": project_name,
            "category_info": category_info,
            "prompts": results,
            "used_existing_detailed": has_existing_detailed,
            "is_existing": project_data.get("is_existing", False),
            "error": "Some or all prompts failed to generate"
        }


def collect_all_projects(category_data):
    """从分类数据中收集所有需要处理的项目
    
    包括：
    1. existing_prompts（48个）：simple已有（summary），detailed已有（refresh），需生成minimal和medium
    2. generated_prompts（600个）：simple已有（description），需生成minimal、detailed和medium
    
    Returns:
        list: 所有项目数据列表
    """
    all_projects = []
    
    classification_data = category_data.get("classification_data", {})
    
    for category_name, category_info in classification_data.items():
        for subcategory_name, subcategory_info in category_info.get("subcategories", {}).items():
            for detailed_cat_name, detailed_cat_info in subcategory_info.get("detailed_categories", {}).items():
                
                category_meta = {
                    "category": category_name,
                    "subcategory": subcategory_name,
                    "detailed_category": detailed_cat_name,
                    "category_desc": category_info.get("description", ""),
                    "subcategory_desc": subcategory_info.get("description", ""),
                    "detailed_category_desc": detailed_cat_info.get("description", "")
                }
                
                # 获取该细类的existing_prompts（用作示例）
                existing_prompts = detailed_cat_info.get("existing_prompts", [])
                
                # 1. 添加existing_prompts自身（它们也需要生成其他版本）
                for ep in existing_prompts:
                    all_projects.append({
                        "name": ep.get("name", ""),
                        "description": ep.get("summary", ""),  # 使用summary作为参考描述
                        "category_info": category_meta,
                        "existing_prompts": existing_prompts,
                        "is_existing": True
                    })
                
                # 2. 添加所有generated_prompts
                for prompt_obj in detailed_cat_info.get("generated_prompts", []):
                    all_projects.append({
                        "name": prompt_obj.get("name", ""),
                        "description": prompt_obj.get("description", ""),
                        "category_info": category_meta,
                        "existing_prompts": existing_prompts,
                        "is_existing": False
                    })
    
    return all_projects


def main():
    """主函数"""
    print(f"{'='*80}")
    print(f"多级别Prompt生成工具")
    print(f"{'='*80}")
    print(f"输入文件:")
    print(f"  Refresh JSONL: {REFRESH_JSONL_FILE}")
    print(f"  Category JSON: {CATEGORY_JSON_FILE}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"并发线程数: {MAX_WORKERS}")
    print(f"\n生成详细程度:")
    for level_key, level_info in DETAIL_LEVELS.items():
        print(f"  - {level_info['name']} ({level_key}): {level_info['description']}")
    print(f"{'='*80}\n")
    
    # 读取数据
    print("正在读取数据...")
    refresh_prompts = read_refresh_prompts(REFRESH_JSONL_FILE)
    print(f"✓ 读取了 {len(refresh_prompts)} 个详细描述（用于existing_prompts的detailed版本）")
    
    category_data = read_category_data(CATEGORY_JSON_FILE)
    print(f"✓ 读取了分类数据")
    print(f"  - existing_prompts总数: {category_data.get('metadata', {}).get('total_existing_prompts', 0)} 个（summary即simple版本）")
    print(f"  - generated_prompts总数: {category_data.get('metadata', {}).get('total_generated_prompts', 0)} 个（description即simple版本）")
    
    # 收集所有需要扩展的项目
    print("\n正在收集所有需要处理的项目...")
    all_projects = collect_all_projects(category_data)
    existing_count = len([p for p in all_projects if p.get("is_existing", False)])
    generated_count = len([p for p in all_projects if not p.get("is_existing", False)])
    print(f"✓ 共收集到 {len(all_projects)} 个项目")
    print(f"  - existing_prompts: {existing_count} 个（simple已有，detailed已有，生成minimal和medium）")
    print(f"  - generated_prompts: {generated_count} 个（simple已有，生成minimal、medium和detailed）\n")
    
    if not all_projects:
        print("✗ 没有找到任何需要处理的项目")
        return
    
    # 创建OpenAI客户端
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    
    # 并发处理所有项目
    all_results = []
    results_lock = threading.Lock()
    
    print(f"开始并发生成prompts（生成顺序：minimal→detailed→medium，{MAX_WORKERS}个工作线程）...\n")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_single_project, client, project, refresh_prompts, idx, len(all_projects)): project
            for idx, project in enumerate(all_projects, 1)
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
    partial = [r for r in all_results if r["status"] == "partial"]
    failed = [r for r in all_results if r["status"] == "failed"]
    
    print(f"\n{'='*80}")
    print(f"生成完成！")
    print(f"{'='*80}")
    print(f"总数: {len(all_results)}")
    print(f"全部成功: {len(successful)}")
    print(f"部分成功: {len(partial)}")
    print(f"全部失败: {len(failed)}")
    
    # 统计使用现有详细描述的项目数
    used_existing_detailed_count = len([r for r in successful + partial if r.get("used_existing_detailed", False)])
    print(f"\n其中直接使用现有detailed描述: {used_existing_detailed_count} 个")
    
    # 保存结果
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存生成的prompts（JSONL格式，每个项目包含4个版本）
    output_jsonl_file = os.path.join(OUTPUT_DIR, f"multi_level_prompts_{timestamp}.jsonl")
    with open(output_jsonl_file, "w", encoding="utf-8") as f:
        for result in successful + partial:
            output_data = {
                "project_name": result["project_name"],
                "category": result["category_info"]["category"],
                "subcategory": result["category_info"]["subcategory"],
                "detailed_category": result["category_info"]["detailed_category"],
                "is_existing": result.get("is_existing", False),
                "prompts": {
                    "minimal": result["prompts"].get("minimal"),
                    "simple": result["prompts"].get("simple"),  # 来自原始数据，无需生成
                    "medium": result["prompts"].get("medium"),
                    "detailed": result["prompts"].get("detailed")
                },
                "metadata": {
                    "lengths": result.get("lengths", {}),
                    "example_count": result.get("example_count", 0),
                    "status": result["status"],
                    "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            f.write(json.dumps(output_data, ensure_ascii=False) + "\n")
    
    print(f"\n生成的prompts已保存到: {output_jsonl_file}")
    
    # 保存详细报告（JSON格式）
    report_file = os.path.join(OUTPUT_DIR, f"generation_report_{timestamp}.json")
    report_data = {
        "metadata": {
            "refresh_file": REFRESH_JSONL_FILE,
            "category_file": CATEGORY_JSON_FILE,
            "output_file": output_jsonl_file,
            "processing_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "timestamp": timestamp,
            "total_projects": len(all_projects),
            "successful": len(successful),
            "partial": len(partial),
            "failed": len(failed),
            "max_workers": MAX_WORKERS,
            "detail_levels": list(DETAIL_LEVELS.keys())
        },
        "statistics": {
            "total_prompts_generated": sum(len([v for v in r["prompts"].values() if v]) for r in successful + partial),
            "average_example_count": sum(r.get("example_count", 0) for r in successful) / len(successful) if successful else 0
        },
        "results": all_results
    }
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"详细报告已保存到: {report_file}")
    
    # 显示部分生成示例
    if successful:
        print(f"\n{'='*80}")
        print(f"生成示例（前2个项目）：")
        print(f"{'='*80}")
        for i, result in enumerate(successful[:2], 1):
            print(f"\n{i}. [{result['project_name']}]")
            print(f"   类别: {result['category_info']['detailed_category']}")
            simple_desc = result["prompts"].get("simple", "")
            if simple_desc:
                print(f"   简短描述: {simple_desc[:60]}...")
            for level_key, level_info in DETAIL_LEVELS.items():
                prompt = result["prompts"].get(level_key)
                if prompt:
                    print(f"   {level_info['name']} ({len(prompt)}字): {prompt[:50]}...")
    
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
