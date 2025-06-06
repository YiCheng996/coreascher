# Coreascher - 基于 CrewAI 的文献综述助手

欢迎使用 Coreascher 项目！这是一个基于 [CrewAI](https://crewai.com) 框架构建的多智能体文献综述系统。该项目旨在通过多个AI代理的协作，自动化完成高质量的学术文献综述任务。

## 项目简介

Coreascher 是一个智能文献综述助手，利用多智能体协作和大语言模型（GLM系列）完成文献检索、分析和综述撰写。系统通过四个专业化的AI代理协同工作，能够生成2000-3000字的高质量学术综述。

### 核心特性

- 🤖 **多智能体协作**：基于CrewAI框架的四个专业化代理
- 📚 **智能文献检索**：支持arXiv等学术数据库的自动检索
- 📝 **自动综述生成**：生成符合学术规范的高质量综述
- 🔍 **可追溯引用**：确保所有引用的准确性和可追溯性
- 🌐 **中英文支持**：支持中英文研究主题输入

## 系统架构

### AI代理团队

1. **教授代理 (Professor Agent)**
   - 角色：研究教授
   - 职责：制定研究框架、指导研究方向、评审论文质量
   - 专长：学术指导和质量控制

2. **博士后代理 (Postdoc Agent)**
   - 角色：计算机科学博士后研究员
   - 职责：将研究计划转化为具体任务、整合研究成果
   - 专长：研究计划细化和成果整合

3. **博士生代理 (PhD Agent)**
   - 角色：计算机科学博士生
   - 职责：执行文献检索、撰写综述内容
   - 专长：文献搜索和内容撰写
   - 工具：文献搜索工具 (LiteratureSearch)

4. **评审代理 (Reviewer Agent)**
   - 角色：严苛但公正的评审人
   - 职责：评估综述质量、提供改进建议
   - 专长：学术质量评估

### 工作流程

1. **研究框架创建** - 教授代理根据主题制定研究框架
2. **框架分析完善** - 博士后代理分析并完善研究框架
3. **关键词任务分配** - 博士后代理生成搜索关键词和具体任务
4. **文献搜索** - 博士生代理使用工具搜索相关文献
5. **综述撰写** - 博士生代理基于检索文献撰写综述
6. **论文整合** - 博士后代理整合各部分内容形成完整论文

## 安装要求

确保您的系统已安装 Python >=3.10 <3.13。本项目使用现代化的依赖管理工具。

### 依赖项

主要依赖包括：
- `crewai>=0.95.0` - 多智能体协作框架
- `langchain>=0.1.0` - 语言模型链
- `pydantic>=2.0.0` - 数据验证
- `python-dotenv>=1.0.0` - 环境变量管理
- `requests>=2.31.0` - HTTP请求
- `loguru>=0.7.2` - 日志记录
- `PyYAML>=6.0.1` - YAML配置文件解析
- `arxiv` - arXiv API客户端

### 安装步骤

1. 克隆项目到本地：
```bash
git clone <repository-url>
cd coreascher
```

2. 安装依赖：
```bash
pip install -r requirements.txt
# 或者如果使用uv
pip install uv
uv sync
```

3. 配置环境变量：
```bash
# 复制环境变量模板
cp .env.example .env
# 编辑 .env 文件，添加您的 OPENAI_API_KEY
```

## 配置说明

### 环境变量配置

在 `.env` 文件中添加必要的API密钥：

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 代理配置

代理配置文件位于 `src/coreascher/config/agents.yaml`，您可以根据需要调整：
- 代理角色和目标
- 代理的详细背景描述
- 执行参数（如最大迭代次数）

### 任务配置

任务配置文件位于 `src/coreascher/config/tasks.yaml`，定义了各个任务的：
- 任务描述
- 预期输出
- 任务依赖关系

## 运行项目

### 基本运行

```bash
# 使用 CrewAI 命令行工具
crewai run

# 或者直接运行 Python 脚本
python run.py

# 或者运行主模块
python -m src.coreascher.main
```

### 高级功能

```bash
# 训练模式（需要指定迭代次数和文件名）
crewai train <n_iterations> <filename>

# 重放特定任务
crewai replay <task_id>

# 测试模式
crewai test <n_iterations> <model_name>
```

## 项目结构

```
coreascher/
├── src/
│   └── coreascher/
│       ├── main.py              # 主程序入口
│       ├── crew.py              # CrewAI团队配置
│       ├── config/
│       │   ├── agents.yaml      # 代理配置
│       │   └── tasks.yaml       # 任务配置
│       ├── tools/
│       │   └── custom_tool.py   # 自定义工具（文献搜索）
│       └── output/              # 输出目录
├── data/                        # 数据目录
├── logs/                        # 日志目录
├── output/                      # 输出结果
├── run.py                       # 启动脚本
├── pyproject.toml              # 项目配置
├── .env                        # 环境变量
└── README.md                   # 项目说明
```

## 使用示例

系统默认会处理 "AI LLMs" 主题的文献综述。您可以通过修改 `main.py` 中的输入参数来更改研究主题：

```python
inputs = {
    'topic': '您的研究主题'  # 支持中英文
}
```

## 输出说明

系统会生成包含以下内容的综述：

1. **摘要** - 研究主题的概述
2. **综述正文** - 详细的文献分析和讨论
3. **研究现状总结** - 主要结论和指标对比
4. **未来趋势展望** - 发展方向预测

所有引用都采用可追溯的格式：`<sup>number</sup>` 和 `【标题+会议/期刊+年份+chunk序号】`

## 自定义开发

### 添加新的代理

1. 在 `config/agents.yaml` 中定义新代理
2. 在 `crew.py` 中添加代理创建方法
3. 更新任务配置以包含新代理

### 添加新的工具

1. 在 `tools/` 目录下创建新的工具文件
2. 继承 `BaseTool` 类并实现必要方法
3. 在相应代理中注册新工具

### 修改工作流程

1. 更新 `config/tasks.yaml` 中的任务定义
2. 调整任务依赖关系
3. 在 `crew.py` 中更新任务创建方法

## 故障排除

### 常见问题

1. **API密钥错误**：确保 `.env` 文件中的 `OPENAI_API_KEY` 正确设置
2. **依赖冲突**：使用虚拟环境隔离项目依赖
3. **网络连接问题**：检查网络连接，确保能访问外部API

### 日志查看

系统日志保存在 `logs/` 目录下，可以通过查看日志文件来诊断问题：

```bash
tail -f logs/crew_execution.log
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 支持与反馈

如需支持、提问或反馈，请通过以下方式联系：

- 📧 邮箱：lth2010lth@outlook.com
- 🐛 问题报告：[GitHub Issues](https://github.com/your-repo/coreascher/issues)
- 📖 CrewAI 文档：[https://docs.crewai.com](https://docs.crewai.com)
- 💬 CrewAI Discord：[https://discord.com/invite/X4JWnZnxPb](https://discord.com/invite/X4JWnZnxPb)

---

让我们一起利用 CrewAI 的强大功能和简洁性，创造学术研究的奇迹！
