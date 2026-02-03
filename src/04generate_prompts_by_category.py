import os
from openai import OpenAI
import json
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import random

# 配置模型参数
# gemini-3-pro
api_key = "ipyezule1b95gc953qf8dvd00p8ct6fz6yu5"
model = "app-wcy0kf-1764751667098941604"
url = "https://wanqing-api.corp.kuaishou.com/api/agent/v1/apps"

# claude-4.5
# api_key="w8hd39mwy1umpnp6s7dh49tn1uyy4hta0fj6"
# model="ep-5b9ezm-1768964270166908191"
# url="https://wanqing-api.corp.kuaishou.com/api/gateway/v1/endpoints"




def read_summaries(summaries_file):
    """从JSONL文件读取所有summaries
    
    Args:
        summaries_file: summaries JSONL文件路径
    
    Returns:
        dict: {project_name: summary}的字典
    """
    summaries = {}
    with open(summaries_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    project_name = data.get("project_name", "")
                    summary = data.get("summary", "")
                    if project_name and summary:
                        summaries[project_name] = summary
                except json.JSONDecodeError as e:
                    print(f"✗ 解析JSON行时出错: {e}")
                    continue
    return summaries


def read_classification(classification_file):
    """读取分类体系JSON文件
    
    Args:
        classification_file: 分类体系JSON文件路径
    
    Returns:
        tuple: (classification_system, projects_mapping)
    """
    with open(classification_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    classification_system = data.get("classification", {}).get("classification_system", {})
    projects_mapping = data.get("classification", {}).get("projects_mapping", {})
    
    return classification_system, projects_mapping


def group_projects_by_detailed_category(classification_system, projects_mapping, summaries):
    """按细类（第三级）对项目进行分组
    
    Args:
        classification_system: 分类体系
        projects_mapping: 项目映射关系
        summaries: 项目summary字典
    
    Returns:
        dict: 细类分组信息
    """
    # 构建细类的完整信息
    detailed_categories_info = {}
    
    for category_name, category_info in classification_system.items():
        for subcategory in category_info.get("subcategories", []):
            subcategory_name = subcategory.get("name", "")
            for detailed_cat in subcategory.get("detailed_categories", []):
                detailed_cat_name = detailed_cat.get("name", "")
                detailed_cat_key = f"{category_name}|{subcategory_name}|{detailed_cat_name}"
                
                detailed_categories_info[detailed_cat_key] = {
                    "category": category_name,
                    "category_desc": category_info.get("description", ""),
                    "subcategory": subcategory_name,
                    "subcategory_desc": subcategory.get("description", ""),
                    "detailed_category": detailed_cat_name,
                    "detailed_category_desc": detailed_cat.get("description", ""),
                    "projects": []
                }
    
    # 将项目分配到对应的细类
    for project_name, mapping in projects_mapping.items():
        category = mapping.get("category", "")
        subcategory = mapping.get("subcategory", "")
        detailed_category = mapping.get("detailed_category", "")
        
        detailed_cat_key = f"{category}|{subcategory}|{detailed_category}"
        
        if detailed_cat_key in detailed_categories_info:
            if project_name in summaries:
                detailed_categories_info[detailed_cat_key]["projects"].append({
                    "name": project_name,
                    "summary": summaries[project_name]
                })
    
    # 过滤掉没有项目的细类
    # detailed_categories_info = {
    #     k: v for k, v in detailed_categories_info.items() 
    #     if len(v["projects"]) > 0
    # }
    
    return detailed_categories_info


def format_classification_system_for_reference(classification_system):
    """格式化分类体系为文本，供模型参考
    
    Args:
        classification_system: 分类体系
    
    Returns:
        str: 格式化的分类体系文本
    """
    lines = []
    for category_name, category_info in classification_system.items():
        lines.append(f"【大类】{category_name}: {category_info.get('description', '')}")
        for subcategory in category_info.get("subcategories", []):
            subcategory_name = subcategory.get("name", "")
            lines.append(f"  【次类】{subcategory_name}: {subcategory.get('description', '')}")
            for detailed_cat in subcategory.get("detailed_categories", []):
                detailed_cat_name = detailed_cat.get("name", "")
                lines.append(f"    【细类】{detailed_cat_name}: {detailed_cat.get('description', '')}")
    
    return "\n".join(lines)


def generate_prompts_for_category(client, category_info, classification_system_text, num_prompts):
    """为指定的细类生成新的prompt案例
    
    Args:
        client: OpenAI客户端
        category_info: 细类信息
        classification_system_text: 完整分类体系文本
        num_prompts: 要生成的prompt数量
    
    Returns:
        list: 生成的prompt列表
    """
    # 构建已有项目的列表
    existing_projects = category_info["projects"]
    projects_text = "\n".join([
        f"{i+1}. {p['name']}: {p['summary']}" 
        for i, p in enumerate(existing_projects)
    ])
    
    system_message = f"""你是一个专业的Web前端项目需求生成专家。你的任务是为特定的技术类别生成符合该类别特征的新项目需求。

**当前目标类别**：
- 大类：{category_info['category']}
  描述：{category_info['category_desc']}
- 次类：{category_info['subcategory']}
  描述：{category_info['subcategory_desc']}
- 细类：{category_info['detailed_category']}
  描述：{category_info['detailed_category_desc']}

**生成数量要求**：
- 目标生成数量为 {num_prompts} 个项目
- 你可以根据该细类的任务丰富程度和可能性空间进行适当调整：
  * 如果该细类的应用场景和变化形式非常丰富，可以生成稍多一些（最多+10个）
  * 如果该细类的应用场景相对局限，可以生成稍少一些（最少-10个）
  * 总体范围建议在{num_prompts-10}到{num_prompts+10}个之间

**项目质量要求**：
1. 生成的每个项目需求必须**严格归属**于上述细类，在代码实现逻辑和所需理论知识上与该类别完全一致
2. 项目描述必须**详细且完整**，要清楚说明：
   - 项目的核心功能和交互方式
   - 需要实现的具体技术特性
   - 视觉效果或用户体验的关键点
   - 相关的参数、规则或约束条件
3. 描述长度应在50-150字之间，确保信息完整但不冗余
4. 必须避免跨越到其他类别（特别是同一次类下的其他细类）
5. 生成的项目应该具有多样性，但都符合该细类的技术特征和知识要求
6. **重要 - 浏览器兼容性要求**：
   - 所有功能和技术必须是**Chrome浏览器原生支持**的
   - 只能使用标准的Web技术：HTML5、CSS3、JavaScript (ES6+)、Canvas、WebGL、SVG等
   - 可以使用浏览器内置API，如：Web Audio API、WebRTC、IndexedDB、LocalStorage等
   - **禁止**使用需要外部依赖、后端服务、或浏览器不支持的功能
   - **禁止**使用需要安装插件、扩展、或额外软件的功能
   - 所有项目必须能够通过单个HTML文件（可包含内嵌CSS和JS）在Chrome浏览器中直接运行

**完整分类体系参考**（请确保生成的项目不越界到其他类别）：
{classification_system_text}

**输出格式**：
请直接输出JSON格式的项目列表：
```json
{{
  "prompts": [
    {{"name": "项目名称1", "description": "项目描述"}},
    {{"name": "项目名称2", "description": "项目描述"}}
  ]
}}
```

注意：
- 直接输出JSON格式，不要添加任何额外的文字说明
- 确保JSON格式正确，可以被直接解析
- 不要使用markdown代码块包裹"""

    user_message = f"""当前细类「{category_info['detailed_category']}」已有 {len(existing_projects)} 个项目：

{projects_text}

---

请根据上述已有项目的特点和该细类的定义，生成大约 {num_prompts} 个新的、严格归属于该细类的Web前端项目需求。

你可以根据该细类的任务丰富程度适当调整数量（在20-30之间），但要确保每个项目都有独特价值且严格符合该细类特征。

要求：
1. 新生成的项目必须与已有项目在技术实现和知识要求上保持一致
2. 项目名称要简洁有辨识度
3. 项目描述必须详细完整，包含功能、技术特性、交互方式、视觉效果等关键信息，长度50-150字
4. 确保不会越界到其他细类
5. 保持项目的多样性和创新性
6. **关键**：所有功能必须是Chrome浏览器原生支持的，可以通过单个HTML文件实现，不依赖外部服务或插件

请直接输出JSON格式的项目列表。"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    print(f"\n  正在为细类「{category_info['detailed_category']}」生成 {num_prompts} 个新项目...")
    print(f"  该类别当前有 {len(existing_projects)} 个已有项目")
    
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,  # 较高的温度以获得更多样化的结果
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # 解析JSON响应
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1] if len(lines) > 2 else lines)
            response_text = response_text.strip()
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()
        
        result = json.loads(response_text)
        prompts = result.get("prompts", [])
        
        print(f"  ✓ 成功生成 {len(prompts)} 个项目")
        return prompts
        
    except Exception as e:
        print(f"  ✗ 生成失败：{e}")
        return []


def main():
    """主函数"""

    # 配置变量
    SUMMARIES_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/summaried_prompt/summaries.jsonl"
    CLASSIFICATION_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/classification/classification_3level_taxonomy_20260129_155808.json"
    OUTPUT_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/generated_prompts_by_category"
    TARGET_PROMPTS_PER_CATEGORY = 25  # 每个细类的目标生成数量（模型可根据类别丰富程度调整20-30之间）
    MAX_WORKERS = 25  # 并发工作线程数


    print(f"{'='*80}")
    print(f"按细类生成新的项目需求")
    print(f"{'='*80}")
    print(f"输入文件:")
    print(f"  Summaries: {SUMMARIES_FILE}")
    print(f"  Classification: {CLASSIFICATION_FILE}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"每个细类目标数量: ~{TARGET_PROMPTS_PER_CATEGORY}个（模型可根据类别丰富程度调整20-30之间）")
    print(f"{'='*80}\n")
    
    # 读取数据
    print("正在读取数据...")
    summaries = read_summaries(SUMMARIES_FILE)
    print(f"✓ 读取了 {len(summaries)} 个项目的summary")
    
    classification_system, projects_mapping = read_classification(CLASSIFICATION_FILE)
    print(f"✓ 读取了分类体系，包含 {len(projects_mapping)} 个项目映射")
    
    # 按细类分组
    print("\n正在按细类分组项目...")
    detailed_categories = group_projects_by_detailed_category(
        classification_system, projects_mapping, summaries
    )
    print(f"✓ 共有 {len(detailed_categories)} 个细类包含项目\n")
    
    # 格式化分类体系供参考
    classification_system_text = format_classification_system_for_reference(classification_system)
    
    # 创建OpenAI客户端
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    
    # 并发为每个细类生成新项目
    all_results = {}
    results_lock = threading.Lock()
    successful_categories = 0
    total_prompts_generated = 0
    
    print(f"开始并发为每个细类生成新项目需求（{MAX_WORKERS}个工作线程）...\n")
    
    def process_category(idx, cat_key, cat_info):
        """处理单个细类的生成任务"""
        category = cat_info['category']
        subcategory = cat_info['subcategory']
        detailed_category = cat_info['detailed_category']
        
        print(f"[{idx}/{len(detailed_categories)}] {category} → {subcategory} → {detailed_category} (目标~{TARGET_PROMPTS_PER_CATEGORY}个)")
        
        # 生成新项目，让模型根据类别丰富程度自行调整
        new_prompts = generate_prompts_for_category(
            client, cat_info, classification_system_text, TARGET_PROMPTS_PER_CATEGORY
        )
        
        return (cat_key, cat_info, new_prompts)
    
    # 使用线程池并发执行
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_category, idx, cat_key, cat_info): (cat_key, cat_info)
            for idx, (cat_key, cat_info) in enumerate(detailed_categories.items(), 1)
        }
        
        for future in as_completed(futures):
            try:
                cat_key, cat_info, new_prompts = future.result()
                
                if new_prompts:
                    with results_lock:
                        all_results[cat_key] = {
                            "category_info": {
                                "category": cat_info['category'],
                                "subcategory": cat_info['subcategory'],
                                "detailed_category": cat_info['detailed_category'],
                                "category_desc": cat_info['category_desc'],
                                "subcategory_desc": cat_info['subcategory_desc'],
                                "detailed_category_desc": cat_info['detailed_category_desc']
                            },
                            "existing_projects_count": len(cat_info['projects']),
                            "existing_projects": cat_info['projects'],
                            "generated_prompts": new_prompts,
                            "generated_count": len(new_prompts)
                        }
                        successful_categories += 1
                        total_prompts_generated += len(new_prompts)
            except Exception as e:
                print(f"  ✗ 处理任务时出错: {e}")
    
    # 构建三层分类结构
    hierarchical_results = {}
    
    for cat_key, result in all_results.items():
        category = result['category_info']['category']
        subcategory = result['category_info']['subcategory']
        detailed_category = result['category_info']['detailed_category']
        
        # 初始化大类
        if category not in hierarchical_results:
            hierarchical_results[category] = {
                "description": result['category_info']['category_desc'],
                "subcategories": {}
            }
        
        # 初始化次类
        if subcategory not in hierarchical_results[category]["subcategories"]:
            hierarchical_results[category]["subcategories"][subcategory] = {
                "description": result['category_info']['subcategory_desc'],
                "detailed_categories": {}
            }
        
        # 添加细类数据
        hierarchical_results[category]["subcategories"][subcategory]["detailed_categories"][detailed_category] = {
            "description": result['category_info']['detailed_category_desc'],
            "existing_prompts": result['existing_projects'],
            "existing_count": result['existing_projects_count'],
            "generated_prompts": result['generated_prompts'],
            "generated_count": result['generated_count'],
            "total_count": result['existing_projects_count'] + result['generated_count']
        }
    
    # 保存结果
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"generated_prompts_by_category_{timestamp}.json")
    
    output_data = {
        "metadata": {
            "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "timestamp": timestamp,
            "summaries_file": SUMMARIES_FILE,
            "classification_file": CLASSIFICATION_FILE,
            "target_prompts_per_category": TARGET_PROMPTS_PER_CATEGORY,
            "prompts_adjustment_note": "Model can adjust count (20-30) based on category richness",
            "max_workers": MAX_WORKERS,
            "browser_requirement": "Chrome native support only",
            "total_detailed_categories": len(detailed_categories),
            "successful_categories": successful_categories,
            "total_existing_prompts": sum(r['existing_projects_count'] for r in all_results.values()),
            "total_generated_prompts": total_prompts_generated,
            "total_prompts": sum(r['existing_projects_count'] for r in all_results.values()) + total_prompts_generated
        },
        "classification_data": hierarchical_results
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"生成完成！")
    print(f"{'='*80}")
    print(f"输出文件: {output_file}")
    print(f"\n统计信息:")
    print(f"  处理的细类数量: {len(detailed_categories)}")
    print(f"  成功生成的细类: {successful_categories}")
    print(f"  已有项目总数: {sum(r['existing_projects_count'] for r in all_results.values())}")
    print(f"  新生成项目总数: {total_prompts_generated}")
    print(f"  总项目数: {sum(r['existing_projects_count'] for r in all_results.values()) + total_prompts_generated}")
    print(f"  平均每个细类生成: {total_prompts_generated / successful_categories:.1f} 个项目" if successful_categories > 0 else "")
    print(f"{'='*80}\n")
    
    # 显示三层结构的生成结果摘要
    print("各类别生成结果:")
    for category, cat_data in hierarchical_results.items():
        print(f"\n【{category}】")
        for subcategory, subcat_data in cat_data["subcategories"].items():
            print(f"  ├─ {subcategory}")
            for detailed_cat, det_data in subcat_data["detailed_categories"].items():
                print(f"      └─ {detailed_cat}")
                print(f"         已有: {det_data['existing_count']} 个 | 新增: {det_data['generated_count']} 个 | 总计: {det_data['total_count']} 个")
                # 显示前2个生成的项目
                for i, prompt in enumerate(det_data['generated_prompts'][:2], 1):
                    desc = prompt.get('description', '')[:60]
                    print(f"           {i}. {prompt.get('name', '')}: {desc}...")
                if det_data['generated_count'] > 2:
                    print(f"           ... 还有 {det_data['generated_count'] - 2} 个")
    
    print(f"\n✓ 任务完成！")


if __name__ == "__main__":
    main()
