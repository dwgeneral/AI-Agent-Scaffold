# AI Agent Scaffold SDK

一个高质量的Python AI Agent开发脚手架SDK，帮助开发者快速集成各大LLM厂商API和主流Agent框架。

## 🚀 特性

### 1. 统一的LLM接口
- 🔥 **火山引擎** - 字节跳动的大模型服务
- 🧠 **智谱AI** - GLM系列模型
- 🌙 **Moonshot** - Kimi大模型
- 💬 **通义千问** - 阿里云大模型
- 🔄 **易扩展** - 支持快速添加新的LLM厂商

### 2. 主流Agent框架集成
- 🦜 **LangChain** - 最流行的LLM应用开发框架
- 📊 **LangGraph** - 基于图的Agent工作流
- 👥 **CrewAI** - 多Agent协作框架
- 🦙 **LlamaIndex** - 数据索引和检索框架
- 🤖 **AutoGen** - 微软的多Agent对话框架
- 🎭 **MetaGPT** - 多角色Agent框架
- 🌊 **PocketFlow** - 轻量级工作流框架

### 3. 完整的开发体验
- 📚 **丰富示例** - 涵盖各种使用场景
- 📖 **详细文档** - 框架对比和最佳实践
- 🧪 **完整测试** - 保证代码质量
- 🎨 **现代化设计** - 异步支持、类型提示

## 🏗️ 架构设计

```
ai-agent-scaffold/
├── 核心层 (Core Layer)
│   ├── 统一LLM接口抽象
│   ├── 消息格式标准化
│   └── 配置管理系统
├── 适配层 (Adapter Layer)
│   ├── 各LLM厂商适配器
│   └── 统一工厂模式
├── 框架层 (Framework Layer)
│   ├── Agent框架集成
│   └── 最佳实践封装
└── 应用层 (Application Layer)
    ├── 示例代码
    └── 使用文档
```

## 📦 安装

```bash
pip install ai-agent-scaffold
```

## 🚀 快速开始

### 基础LLM调用

```python
from ai_agent_scaffold import LLMFactory

# 创建LLM实例
llm = LLMFactory.create('zhipu', api_key='your-api-key')

# 简单对话
response = await llm.chat("你好，请介绍一下自己")
print(response.content)

# 流式对话
async for chunk in llm.stream("写一首关于AI的诗"):
    print(chunk.content, end='')
```

### Agent框架集成

```python
from ai_agent_scaffold.frameworks import LangChainIntegration

# 快速创建LangChain Agent
agent = LangChainIntegration.create_agent(
    llm_provider='moonshot',
    tools=['search', 'calculator'],
    api_key='your-api-key'
)

# 运行Agent
result = await agent.run("帮我搜索今天的天气并计算温度差")
```

## 📁 项目结构

```
ai-agent-scaffold/
├── ai_agent_scaffold/          # 主包
│   ├── core/                   # 核心层
│   ├── adapters/              # 适配层
│   ├── frameworks/            # 框架层
│   └── utils/                 # 工具模块
├── examples/                  # 示例代码
├── docs/                      # 文档
├── tests/                     # 测试
└── requirements.txt           # 依赖
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License