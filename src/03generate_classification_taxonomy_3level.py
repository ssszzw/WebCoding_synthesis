import os
from openai import OpenAI
import json
from datetime import datetime

# 配置模型参数
# gemini-3-pro
api_key = "ipyezule1b95gc953qf8dvd00p8ct6fz6yu5"
model = "app-wcy0kf-1764751667098941604"
url = "https://wanqing-api.corp.kuaishou.com/api/agent/v1/apps"

# claude-4.5
# api_key="w8hd39mwy1umpnp6s7dh49tn1uyy4hta0fj6"
# model="ep-5b9ezm-1768964270166908191"
# url="https://wanqing-api.corp.kuaishou.com/api/gateway/v1/endpoints"

# 配置变量：输入输出路径
# 是否对项目进行分类（True: 模型会将每个项目分配到具体类别；False: 只生成分类体系）
CLASSIFY_PROJECTS = True



def read_summaries_from_report(report_file):
    """从report JSON文件中提取所有的summary
    
    Args:
        report_file: report JSON文件路径
    
    Returns:
        list: 包含所有summary的列表
    """
    if not os.path.exists(report_file):
        print(f"✗ 错误：输入文件不存在: {report_file}")
        return []
    
    with open(report_file, "r", encoding="utf-8") as f:
        report_data = json.load(f)
    
    summaries = []
    
    # 从results中提取summary
    if "results" in report_data:
        for result in report_data["results"]:
            if result.get("status") == "success" and "summary" in result:
                summaries.append({
                    "project": result.get("project", "unknown"),
                    "summary": result["summary"]
                })
    
    return summaries


def read_summaries_from_jsonl(jsonl_file):
    """从JSONL文件中提取所有的summary（备用方法）
    
    Args:
        jsonl_file: JSONL文件路径
    
    Returns:
        list: 包含所有summary的列表
    """
    if not os.path.exists(jsonl_file):
        print(f"✗ 错误：输入文件不存在: {jsonl_file}")
        return []
    
    summaries = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    if "summary" in data:
                        summaries.append({
                            "project": data.get("project_name", "unknown"),
                            "summary": data["summary"]
                        })
                except json.JSONDecodeError as e:
                    print(f"✗ 解析JSON行时出错: {e}")
                    continue
    
    return summaries


def generate_classification_taxonomy(client, summaries, classify_projects=False):
    """调用模型生成三级分类体系
    
    Args:
        client: OpenAI客户端
        summaries: 所有summary的列表
        classify_projects: 是否对每个项目进行分类
    
    Returns:
        str: 模型生成的分类体系
    """
    # 拼接所有的summary
    if classify_projects:
        # 包含project_name，方便模型进行分类
        summaries_text = "\n".join([f"{i+1}. [项目名: {s['project']}] {s['summary']}" for i, s in enumerate(summaries)])
    else:
        summaries_text = "\n".join([f"{i+1}. {s['summary']}" for i, s in enumerate(summaries)])
    
    system_message = """你是一个专业的分类专家。你的任务是根据提供的一系列Web前端项目的功能描述，设计一个合理的三级分类体系。

**核心分类依据**：
分类应基于以下两个维度进行：
1. **代码实现逻辑**：技术栈、算法复杂度、架构模式、渲染方式、交互机制等
2. **所需理论知识**：模型需要掌握和理解的世界知识，如物理学原理、数学理论、游戏设计理论、视觉艺术原理、业务领域知识等

分类层级要求：
1. 分类需要分为三个层级：
   - **大类（一级分类）**：按照项目的主要应用领域和技术方向进行宏观分类
     * 例如：游戏类、模拟类、工具类、可视化类等
   
   - **次类（二级分类）**：基于代码实现逻辑和核心技术栈进行细分
     * 例如：对于游戏类 → 按渲染方式分为2D Canvas游戏、3D WebGL游戏等
     * 例如：对于模拟类 → 按实现技术分为粒子系统模拟、物理引擎模拟、数学公式驱动等
     * 每个大类下应有2-20个次类，确保充分细分
   
   - **细类（三级分类）**：基于所需的理论知识和具体实现细节进行最精细划分
     * 例如：物理引擎模拟 → 细分为刚体力学（碰撞检测）、流体动力学（SPH算法）、软体物理（弹簧质点系统）等
     * 例如：2D Canvas游戏 → 细分为射击类（弹道计算）、平台跳跃类（重力与碰撞）、解谜类（逻辑推理）等
     * 例如：3D场景渲染 → 细分为自然景观（地形生成、植被系统）、建筑场景（几何建模）、抽象特效（着色器编程）等
     * 每个次类下可以有2-15个细类
   
2. **重要 - 二级分类要求**：
   - 次类必须明确反映代码实现的核心技术和架构特点
   - 同一次类下的项目应该使用相似的技术栈和实现模式
   - 如果某个大类技术跨度大，应该创建更多次类来区分不同的实现路径
   
3. **重要 - 三级分类要求**：
   - 细类必须明确反映项目所需的理论知识类型
   - 同一细类下的项目应该需要相似的世界知识和理论基础
   - 细类名称要能够清晰指出具体的知识领域，例如：
     * 物理学：经典力学、流体力学、热力学、光学、电磁学等
     * 数学：几何变换、三角函数、微积分、线性代数、概率统计等
     * 游戏设计：关卡设计、平衡性设计、交互反馈、难度曲线等
     * 图形学：光线追踪、体素渲染、粒子系统、程序化生成等
     * 领域知识：音乐理论、色彩理论、UI/UX设计、业务流程等
   
4. **分类原则**：
   - 分类要覆盖所有提供的项目描述
   - 同一类别下的项目在代码实现和知识要求上应该有明显的相似性
   - 不同类别之间的项目在技术栈或理论知识上应该有清晰的区分
   - 分类名称要简洁、准确、专业，能够体现技术特点和知识领域
   - 建议的大类数量：5-12个，但优先保证次类和细类的细致划分

输出格式：
请使用以下JSON格式输出分类体系：
```json
{
  "classification_system": {
    "大类名称1": {
      "description": "大类的简短描述",
      "subcategories": [
        {
          "name": "次类名称1",
          "description": "次类的简短描述",
          "detailed_categories": [
            {"name": "细类名称1", "description": "细类的简短描述"},
            {"name": "细类名称2", "description": "细类的简短描述"}
          ]
        },
        {
          "name": "次类名称2",
          "description": "次类的简短描述",
          "detailed_categories": [
            {"name": "细类名称1", "description": "细类的简短描述"},
            {"name": "细类名称2", "description": "细类的简短描述"}
          ]
        }
      ]
    },
    "大类名称2": {
      "description": "大类的简短描述",
      "subcategories": [
        {
          "name": "次类名称1",
          "description": "次类的简短描述",
          "detailed_categories": [
            {"name": "细类名称1", "description": "细类的简短描述"}
          ]
        }
      ]
    }
  },
  "total_categories": "总大类数量",
  "total_subcategories": "总次类数量",
  "total_detailed_categories": "总细类数量",
  "classification_rationale": "分类设计的理由说明"PROJECTS_MAPPING_PLACEHOLDER
}
```

注意：
- 直接输出JSON格式的分类体系，不要添加任何额外的文字说明
- 确保JSON格式正确，可以被直接解析
- 不要使用markdown代码块包裹"""
    
    # 根据是否需要对项目分类，调整输出格式说明
    if classify_projects:
        projects_mapping_format = ''',
  "projects_mapping": {
    "项目名1": {"category": "大类名称", "subcategory": "次类名称", "detailed_category": "细类名称"},
    "项目名2": {"category": "大类名称", "subcategory": "次类名称", "detailed_category": "细类名称"}
  }'''
        system_message = system_message.replace('PROJECTS_MAPPING_PLACEHOLDER', projects_mapping_format)
    else:
        system_message = system_message.replace('PROJECTS_MAPPING_PLACEHOLDER', '')

    if classify_projects:
        user_message = f"""以下是 {len(summaries)} 个Web前端项目的功能描述：

{summaries_text}

---

请根据上述所有项目的功能描述，设计一个合理的三级分类体系，并将每个项目分配到对应的大类、次类和细类中。

要求：
1. 在 projects_mapping 中，使用项目名作为key，指定每个项目所属的大类（category）、次类（subcategory）和细类（detailed_category）
2. 确保每个项目都被分配到一个类别中
3. 项目名要与输入中 [项目名: xxx] 的名称完全一致

请直接输出JSON格式的分类体系和项目映射。"""
    else:
        user_message = f"""以下是 {len(summaries)} 个Web前端项目的功能描述：

{summaries_text}

---

请根据上述所有项目的功能描述，设计一个合理的三级分类体系。注意：不需要指定每个项目属于哪个类别，只需要设计出分类体系本身。

请直接输出JSON格式的分类体系。"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    print(f"\n正在调用模型生成三级分类体系...")
    print(f"共提供 {len(summaries)} 个项目描述")
    
    # 调用API
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.5,  # 适中的温度，保证创意和稳定性
        )
        
        classification = completion.choices[0].message.content.strip()
        return classification
        
    except Exception as e:
        print(f"✗ 调用API时出错：{e}")
        return None


def parse_and_validate_classification(classification_text):
    """解析并验证分类体系JSON
    
    Args:
        classification_text: 模型返回的分类体系文本
    
    Returns:
        dict: 解析后的分类体系字典
    """
    # 移除可能的markdown代码块标记
    if classification_text.startswith("```"):
        lines = classification_text.split("\n")
        classification_text = "\n".join(lines[1:-1] if len(lines) > 2 else lines)
        classification_text = classification_text.strip()
        if classification_text.startswith("json"):
            classification_text = classification_text[4:].strip()
    
    try:
        classification_dict = json.loads(classification_text)
        return classification_dict
    except json.JSONDecodeError as e:
        print(f"✗ JSON解析失败：{e}")
        print(f"原始响应内容:\n{classification_text[:500]}...")
        return None


def generate_classification_from_summaries(summaries_file, output_dir, classify_projects=False):
    """从summaries JSONL文件生成三级分类体系的主函数
    
    Args:
        summaries_file: summaries JSONL文件路径
        output_dir: 输出目录路径
        classify_projects: 是否对每个项目进行分类
    """
    print(f"{'='*80}")
    print(f"从summaries生成三级分类体系")
    print(f"{'='*80}")
    print(f"输入文件: {summaries_file}")
    print(f"输出目录: {output_dir}")
    print(f"项目分类: {'是' if classify_projects else '否'}")
    print(f"{'='*80}\n")
    
    # 读取summaries
    summaries = read_summaries_from_jsonl(summaries_file)
    
    if not summaries:
        print("✗ 错误：未能从summaries文件中提取到任何summary")
        return
    
    print(f"✓ 成功提取 {len(summaries)} 个项目的summary\n")
    
    # 显示前5个summary作为预览
    print("前5个summary预览:")
    for i, s in enumerate(summaries[:5]):
        print(f"  {i+1}. [{s['project']}] {s['summary'][:60]}...")
    if len(summaries) > 5:
        print(f"  ... 还有 {len(summaries) - 5} 个\n")
    
    # 创建OpenAI客户端
    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    
    # 生成分类体系
    classification_text = generate_classification_taxonomy(client, summaries, classify_projects)
    
    if not classification_text:
        print("✗ 生成分类体系失败")
        return
    
    print(f"✓ 模型已返回分类体系\n")
    
    # 解析和验证分类体系
    classification_dict = parse_and_validate_classification(classification_text)
    
    if not classification_dict:
        print("✗ 分类体系解析失败")
        # 仍然保存原始文本
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_output_file = os.path.join(output_dir, f"classification_3level_raw_{timestamp}.txt")
        with open(raw_output_file, "w", encoding="utf-8") as f:
            f.write(classification_text)
        print(f"原始输出已保存到: {raw_output_file}")
        return
    
    # 保存分类体系
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"classification_3level_taxonomy_{timestamp}.json")
    
    # 计算三级分类的统计
    total_detailed_categories = 0
    if "classification_system" in classification_dict:
        for cat_info in classification_dict["classification_system"].values():
            if "subcategories" in cat_info:
                for subcat in cat_info["subcategories"]:
                    if "detailed_categories" in subcat:
                        total_detailed_categories += len(subcat["detailed_categories"])
    
    # 添加元数据和详细信息
    output_data = {
        "metadata": {
            "source_file": summaries_file,
            "timestamp": timestamp,
            "total_projects": len(summaries),
            "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "classify_projects": classify_projects,
            "classification_levels": 3
        },
        "classification": classification_dict,
        "statistics": {
            "total_categories": len(classification_dict.get("classification_system", {})),
            "total_subcategories": sum(
                len(cat.get("subcategories", [])) 
                for cat in classification_dict.get("classification_system", {}).values()
            ),
            "total_detailed_categories": total_detailed_categories
        }
    }
    
    # 如果包含项目映射，添加映射统计
    if classify_projects and "projects_mapping" in classification_dict:
        output_data["statistics"]["total_mapped_projects"] = len(classification_dict["projects_mapping"])
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"三级分类体系生成完成！")
    print(f"{'='*80}")
    print(f"输出文件: {output_file}")
    
    # 显示分类统计
    if "classification_system" in classification_dict:
        cat_system = classification_dict["classification_system"]
        print(f"\n分类统计:")
        print(f"  大类数量: {len(cat_system)}")
        total_subcats = sum(len(cat["subcategories"]) for cat in cat_system.values() if "subcategories" in cat)
        print(f"  次类总数: {total_subcats}")
        print(f"  细类总数: {total_detailed_categories}")
        
        print(f"\n分类结构:")
        for main_cat, cat_info in cat_system.items():
            desc = cat_info.get("description", "")
            subcats = cat_info.get("subcategories", [])
            print(f"  [{main_cat}] - {desc}")
            for subcat in subcats:
                subcat_name = subcat.get('name', '')
                subcat_desc = subcat.get('description', '')
                print(f"    - {subcat_name}: {subcat_desc}")
                # 显示细类
                detailed_cats = subcat.get("detailed_categories", [])
                if detailed_cats:
                    for det_cat in detailed_cats:
                        print(f"      · {det_cat.get('name', '')}: {det_cat.get('description', '')}")
    
    # 如果包含项目映射，显示映射统计
    if classify_projects and "projects_mapping" in classification_dict:
        projects_mapping = classification_dict["projects_mapping"]
        print(f"\n项目分类统计:")
        print(f"  已分类项目数: {len(projects_mapping)}")
        print(f"  未分类项目数: {len(summaries) - len(projects_mapping)}")
        
        # 统计每个大类下的项目数量
        category_counts = {}
        for project, mapping in projects_mapping.items():
            category = mapping.get("category", "未知")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\n各大类项目分布:")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}个项目")
    
    print(f"{'='*80}\n")
    
    return output_data


if __name__ == "__main__":

    INPUT_JSONL_FILE = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/summaried_prompt/summaries.jsonl"
    OUTPUT_DIR = "/Users/shenzhiwei/intern-content/code/WebCoding_synthesis/data/classification"

    # 使用配置变量
    print(f"\n配置信息:")
    print(f"  输入文件: {INPUT_JSONL_FILE}")
    print(f"  输出目录: {OUTPUT_DIR}")
    print(f"  项目分类: {'启用' if CLASSIFY_PROJECTS else '禁用'}")
    print(f"  分类层级: 三级（大类 → 次类 → 细类）")
    print()
    
    # 生成分类体系
    result = generate_classification_from_summaries(INPUT_JSONL_FILE, OUTPUT_DIR, CLASSIFY_PROJECTS)
    
    if result:
        print("✓ 任务完成！")
    else:
        print("✗ 任务失败")
