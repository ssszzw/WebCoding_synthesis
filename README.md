# Code Comprehension Trajectory

用于构建代码理解相关训练数据的工具集。

## 核心流程

```
爬取 GitHub 仓库列表 -> 筛选仓库 -> 爬取仓库 DeepWiki -> 构建 Docker 镜像 -> 合成代码理解 Query -> 合成轨迹并转换
```

## 项目结构

```
code-comprehension-traj/
├── README.md                              # 项目说明
├── configs/                               # 配置文件
│   └── example_config.json               # 示例配置
├── data/                                  # 数据目录
│   ├── sample_repos.jsonl                # 示例仓库数据
│   └── .gitkeep
├── src/                                   # 源代码
│   ├── __init__.py
│   ├── crawl/                            # 爬取相关
│   │   ├── __init__.py
│   │   ├── github_repo_crawler.py        # GitHub 仓库爬取
│   │   ├── repo_filter.py                # 仓库筛选
│   │   └── deepwiki_crawler.py           # DeepWiki 文档爬取
│   ├── docker/                           # Docker 相关
│   │   ├── templates/
│   │   │   └── Dockerfile.template       # Dockerfile 模板
│   │   ├── build_image.sh                # 单个仓库构建脚本
│   │   └── batch_build.py                # 批量构建脚本
│   ├── query/                            # Query 合成相关
│   │   ├── __init__.py
│   │   ├── query_synthesizer.py          # 基于 DeepWiki 生成 Query
│   │   └── tasks_generator.py            # 生成 tasks.jsonl
│   ├── trajectory/                       # 轨迹相关
│   │   ├── __init__.py
│   │   ├── synthesize.py                 # 轨迹合成
│   │   └── convert.py                    # 轨迹转换
│   └── utils/                            # 工具函数
│       └── __init__.py
└── scripts/                              # 运行脚本（可选）
```

## 安装依赖

```bash
pip install requests tqdm fastmcp
```

## 使用方法

### 1. 爬取 GitHub 高星仓库

支持多 token 轮换使用，自动验证 token 有效性并过滤无效 token。

**准备 Token 文件：**

创建 `data/github_tokens.txt`，每行一个 token：
```
# GitHub Personal Access Tokens（# 开头为注释）
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ghp_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
ghp_zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
```

**运行爬取：**

```bash
# 使用 token 文件爬取（推荐）
python -m src.crawl.github_repo_crawler \
    --language ALL \
    --count 50000 \
    --tokens data/github_tokens.txt \
    --output data/repos/ALL_top_50000_repos.jsonl

# 使用单个 token（兼容旧接口）
python -m src.crawl.github_repo_crawler \
    --language Python \
    --count 1000 \
    --token YOUR_GITHUB_TOKEN \
    --output data/repos/Python_top_1000_repos.jsonl
```

**参数说明：**
- `--language`, `-l`: 目标语言（如 `Python`），或 `ALL` 表示所有语言（默认: ALL）
- `--count`, `-c`: 需要获取的仓库数量（默认: 1000）
- `--tokens`: GitHub tokens 文件路径（推荐，支持多 token 轮换）
- `--token`, `-t`: 单个 GitHub API token（兼容旧接口）
- `--output`, `-o`: 输出文件路径（JSONL 格式）
- `--require-full-permission`: 要求 token 具有完整权限（repo + admin:org）

**Token 权限说明：**
- 爬取公开仓库列表**不需要任何特殊权限**，只要 token 有效即可
- Token 的主要作用是提高 API 速率限制（无 token: 60次/小时，有 token: 5000次/小时）
- 程序会自动验证所有 token，过滤掉无效或过期的 token

**验证输出示例：**
```
开始验证 19 个 GitHub tokens...
==================================================
验证 tokens: 100%|████████████████| 19/19
==================================================
验证完成:
  - 总 token 数: 19
  - 有效 token 数: 15
  - 完整权限 token 数: 3
将使用 15 个有效 token 进行爬取
```

### 2. 筛选仓库

过滤掉非代码仓库（如 awesome 列表、学习资料等）：

```bash
python -m src.crawl.repo_filter \
    --input data/repos/ALL_top_5865_repos.jsonl \
    --output data/filtered_repos \
    --tokens data/github_tokens.txt \
    --workers 4
```

**参数说明：**
- `--input`: 输入的仓库列表文件
- `--output`: 输出目录
- `--tokens`: GitHub tokens 文件（每行一个 token）
- `--workers`: 并发数

**输出文件：**
- `filtered_code_repos.jsonl`: 通过筛选的仓库
- `filter_analysis_detail.jsonl`: 详细分析结果
- `filtered_repos_{language}.jsonl`: 按语言分类的仓库

### 3. 爬取 DeepWiki 文档

```bash
python -m src.crawl.deepwiki_crawler \
    --input data/filtered_repos/filtered_code_repos.jsonl \
    --output data/wiki \
    --proxies data/proxies.txt //代码里默认的proxies已够用
```

**参数说明：**
- `--input`: 输入的仓库列表文件
- `--output`: 输出目录
- `--proxies`: 代理列表文件（可选）

### 4. 构建 Docker 镜像

#### 单个仓库构建

```bash
./src/docker/build_image.sh <repo_owner> <repo_name> <commit_id> [output_dir]

# 示例
./src/docker/build_image.sh Acly krita-ai-diffusion 4cf869ec ./tar
```

#### 批量构建

从 DeepWiki 数据目录读取仓库信息，批量构建 Docker 镜像并保存为 tar 包：

```bash
# 构建全部仓库
python -m src.docker.batch_build \
    --wiki-dir data/wiki \
    --output ./tar \
    --count -1

# 随机构建 100 个仓库
python -m src.docker.batch_build \
    --wiki-dir data/wiki \
    --output ./tar \
    --count 100

# 使用多线程并行构建（通常不建议，Docker 构建本身较重）
python -m src.docker.batch_build \
    --wiki-dir data/wiki \
    --output ./tar \
    --count 50 \
    --workers 2
```

**参数说明：**
- `--wiki-dir`, `-w`: DeepWiki 数据目录（默认: data/wiki）
- `--output`, `-o`: tar 包输出目录（默认: ./tar）
- `--count`, `-c`: 构建数量，-1 表示全部，正数表示随机选择该数量（默认: -1）
- `--workers`, `-j`: 并行工作线程数（默认: 1）
- `--no-skip`: 不跳过已完成的仓库（重新构建）
- `--build-script`: 自定义构建脚本路径

**输出文件：**
- `{owner}_{repo}_latest.tar`: Docker 镜像 tar 包
- `build_failed.txt`: 构建失败的仓库日志

### 5. 合成代码理解 Query

基于 DeepWiki 文档，使用 LLM 生成代码理解相关的问题。

#### 步骤 1: 生成 Query

```bash
# 处理全部 wiki 文件
python -m src.query.query_synthesizer \
    --wiki-dir ./data/wiki \
    --output ./data/queries \
    --num-queries 8 \
    --workers 2 \
    --api-url "http://wanqing.internal/api/gateway/v1/endpoints/chat/completions" \
    --api-key "w8hd39mwy1umpnp6s7dh49tn1uyy4hta0fj6" \
    --model "ep-nsitap-1768964384995638827"

# 随机处理 10 个仓库（测试用）
python -m src.query.query_synthesizer \
    --wiki-dir ./data/wiki \
    --output ./data/queries \
    --count 10 \
    --num-queries 8
```

**参数说明：**
- `--wiki-dir`, `-w`: DeepWiki 数据目录
- `--output`, `-o`: Query 输出目录（默认: ./data/queries）
- `--count`, `-c`: 处理数量，-1 表示全部（默认: -1）
- `--num-queries`, `-n`: 每个仓库生成的 query 数量（默认: 8）
- `--workers`, `-j`: 并行工作线程数（默认: 1）

**Query 类型分布：**
- 25% 新手视角：项目介绍、核心功能、快速上手
- 25% 初学者视角：功能实现、模块作用、数据流
- 25% 进阶用户视角：文件定位、调用链、设计决策
- 25% 专家视角：重构建议、功能扩展、Bug 修复

**输出格式（JSONL）：**
```json
{"instance_id": "owner_repo_001", "repo": "owner/repo", "level": "beginner", "type": "understanding", "language": "zh", "query": "这个项目是干什么的？"}
```

#### 步骤 2: 生成 tasks.jsonl

将 Query 与 Docker 镜像信息合并，生成轨迹合成所需的 tasks.jsonl。只有同时具有 Query 和 Docker 镜像（tar 包）的仓库才会被包含在 tasks.jsonl 中。

```bash
# 首次生成 tasks.jsonl
python -m src.query.tasks_generator \
    --queries-dir ./data/queries \
    --wiki-dir ./data/wiki \
    --tar-dir ./tar \
    --output ./data/tasks.jsonl
```

**增量合成（跳过已完成的轨迹）：**

当部分轨迹已经合成完成后，可以使用 `--trajectory-dir` 参数跳过已完成的任务，只生成剩余待处理的 tasks：

```bash
# 增量生成 tasks.jsonl（跳过已完成的轨迹）
python -m src.query.tasks_generator \
    --queries-dir ./data/queries \
    --wiki-dir ./data/wiki \
    --tar-dir ./tar \
    --trajectory-dir ./output/trajectory \
    --output ./data/tasks2.jsonl
```

这在以下场景非常有用：
- 镜像分批构建，需要分批合成轨迹
- 轨迹合成中断后需要续跑
- 新增镜像后需要增量合成

**参数说明：**
- `--queries-dir`, `-q`: Query 文件目录
- `--wiki-dir`, `-w`: DeepWiki 数据目录
- `--tar-dir`, `-t`: Docker tar 包目录
- `--trajectory-dir`: 轨迹输出目录（用于跳过已完成的任务，可选）
- `--output`, `-o`: 输出文件路径（默认: ./data/tasks.jsonl）

**tasks.jsonl 格式：**
```json
{"instance_id": "owner_repo_001", "repo": "owner/repo", "images_name": "owner_repo_latest", "base_commit": "abc123", "problem_statement": "这个项目是干什么的？"}
```

### 6. 轨迹合成

#### 步骤 1: 加载 Docker 镜像

在运行轨迹合成之前，需要先将 tar 包加载为 Docker 镜像：

```bash
# 批量加载所有镜像
ls ./tar/*.tar | xargs -P 8 -I {} sh -c 'echo "Loading {}..." && docker load -i "{}"'

# 或者加载单个镜像
docker load -i ./tar/owner_repo_latest.tar
```

#### 步骤 2: 运行轨迹合成

```bash
python -m src.trajectory.synthesize --config configs/example_config.json
```

**配置文件格式：**
```json
{
    "tasks_file": "data/tasks.jsonl",
    "output_dir": "./output/trajectory",
    "proxy_server_file": "server.py",
    "agent_dir": "agent/claude_code",
    "anthropic_auth_token": "YOUR_TOKEN",
    "anthropic_base_url": "https://api.anthropic.com",
    "num_tasks": -1,
    "num_processes": 4,
    "retry_count": 3
}
```

**说明：**
- 轨迹合成会自动跳过已完成的任务（检查 `output_dir` 下是否存在 `model.patch` 或 `messages.log`）
- 如果需要增量合成新的镜像，先用步骤 5.2 重新生成 tasks.jsonl（带 `--trajectory-dir` 参数），然后再运行合成

### 7. 轨迹转换

将 Claude Code 轨迹转换为 OpenAI 格式的训练数据：

```bash
python -m src.trajectory.convert \
    --input /path/to/trajectory_dir \
    --output train_data.jsonl \
    --workers 8
```

**参数说明：**
- `--input`: 输入目录（可以指定多个）
- `--output`: 输出文件路径（JSONL 格式）
- `--workers`: 并行处理的进程数

## 数据格式

### 仓库列表格式（JSONL）

```json
{"repo": "owner/repo", "language": "Python", "stars": 12345}
```

### 筛选后的仓库格式（JSONL）

```json
{
    "repo": "owner/repo",
    "language": "Python",
    "stars": 12345,
    "forks": 1000,
    "pr_count": 500,
    "issue_count": 200,
    "contributors": 50,
    "default_branch": "main",
    "language_stats": {"Python": 85.5, "JavaScript": 10.2, "CSS": 4.3}
}
```

### DeepWiki 数据格式（JSON）

```json
{
    "repo_name": "owner/repo",
    "commit_id": "abc123",
    "github_url": "https://github.com/owner/repo",
    "commit_url": "https://github.com/owner/repo/commit/abc123",
    "toc": "目录结构...",
    "documents": ["文档1内容...", "文档2内容..."],
    "crawl_time": "2024-01-01T00:00:00",
    "proxy_used": "10.0.0.1:8080"
}
```

### 训练数据格式（JSONL）

```json
{
    "uid": "unique_id",
    "model": "claude-3-opus",
    "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "...", "tool_calls": [...]}
    ],
    "tools": [...],
    "start_index": 0,
    "source_file": "/path/to/messages.log"
}
```

## 原始数据位置

- 原始仓库列表：`/wl_intelligent/zhuangwenhao/deepwikinew/swe-bench-pro/repo_env_construct/crawl/data/ALL_top_50000_repos.jsonl`
- 筛选结果目录：`/wl_intelligent/zhuangwenhao/deepwikinew/swe-bench-pro/repo_env_construct/crawl/output2`
- DeepWiki 数据目录：`/wl_intelligent/zhuangwenhao/deepwikinew/swe-bench-pro/repo_env_construct/crawl/repo_wiki2`
- 轨迹示例目录：`/wl_intelligent/zhuangwenhao/deepwikinew/trajectory/0112test/Acly/krita-ai-diffusion`
- 转换后的训练数据：`/wl_intelligent/zhuangwenhao/deepwikinew/trajectory/deepwiki_trajectory_train_data.jsonl`

## 筛选规则

仓库筛选器会过滤掉以下类型的仓库：

1. **名称匹配**：awesome-*, *-list, *-resources, *-books, *-tutorials 等
2. **描述匹配**：curated list, collection of, list of 等
3. **语言过滤**：主语言为 Markdown, HTML, CSS 等非编程语言
4. **代码占比**：主语言代码占比低于 50%
5. **活跃度**：Fork 数、PR 数、Issue 数、贡献者数低于阈值
6. **代码文件**：仓库中没有实际的代码文件

## 注意事项

1. GitHub API 有速率限制，建议使用多个 token 轮换
2. DeepWiki 爬取建议使用代理池，避免 IP 被封
3. Docker 构建需要网络访问 GitHub，建议配置代理
4. 轨迹合成需要较长时间，建议使用多进程并行

## License

MIT
