# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 初始项目结构和核心架构
- 支持多个LLM提供商的统一接口
- 集成主流Agent框架的适配器
- 完整的开发工具链和CI/CD配置

## [0.1.0] - 2024-01-XX

### Added

#### 核心功能
- **统一LLM接口**: 提供`BaseLLM`抽象基类，统一不同LLM提供商的API调用方式
- **消息系统**: 实现`Message`类，支持文本、图片、音频等多模态消息类型
- **配置管理**: 提供灵活的配置系统，支持环境变量、YAML文件等多种配置方式
- **LLM工厂**: 实现`LLMFactory`类，支持动态创建和管理LLM实例
- **错误处理**: 定义完整的异常体系，提供详细的错误信息和处理建议

#### LLM提供商支持
- **智谱AI (GLM系列)**: 支持GLM-4、GLM-4V等模型的聊天、流式和嵌入功能
- **Moonshot AI (Kimi系列)**: 支持moonshot-v1-8k、moonshot-v1-32k等模型
- **通义千问**: 支持qwen-turbo、qwen-plus、qwen-max等阿里云模型
- **火山引擎**: 支持字节跳动的Doubao系列模型

#### Agent框架集成
- **LangChain**: 提供LangChain适配器，支持创建Agent、RAG链和对话链
- **LangGraph**: 支持创建复杂的工作流和多Agent协作
- **CrewAI**: 支持创建Agent团队和任务分配
- **LlamaIndex**: 支持文档索引和查询引擎
- **AutoGen**: 支持多Agent对话和群组聊天
- **MetaGPT**: 支持软件开发团队模拟
- **PocketFlow**: 提供工作流编排能力（示例实现）

#### 开发工具
- **代码质量**: 集成Black、isort、flake8、mypy等代码质量工具
- **测试框架**: 使用pytest进行单元测试和集成测试
- **文档生成**: 使用Sphinx生成API文档
- **CI/CD**: GitHub Actions自动化测试、构建和发布
- **安全检查**: 集成bandit和safety进行安全扫描

#### 示例和文档
- **基础使用示例**: 展示如何使用不同LLM提供商进行聊天和嵌入
- **框架集成示例**: 演示各种Agent框架的使用方法
- **智能客服示例**: 完整的客服系统实现，展示多组件协作
- **详细文档**: 包含安装、配置、使用指南和API参考

### Technical Details

#### 架构设计
- 采用插件化架构，支持动态加载LLM提供商和框架适配器
- 使用Pydantic进行数据验证和序列化
- 支持异步操作，提高并发性能
- 实现统一的错误处理和重试机制

#### 性能优化
- HTTP连接池复用，减少连接开销
- 支持流式响应，降低延迟
- 实现请求缓存，避免重复调用
- 支持并发限制，防止API限流

#### 安全特性
- API密钥安全存储和传输
- 请求签名验证
- 输入数据验证和清理
- 错误信息脱敏处理

### Dependencies

#### 核心依赖
- `pydantic>=2.0.0`: 数据验证和序列化
- `httpx>=0.24.0`: HTTP客户端
- `rich>=13.0.0`: 终端输出美化
- `pyyaml>=6.0`: YAML配置文件支持
- `typing-extensions>=4.0.0`: 类型注解扩展

#### 可选依赖
- LLM提供商SDK: zhipuai, openai, dashscope, volcengine
- Agent框架: langchain, langgraph, crewai, llama-index, pyautogen, metagpt
- 开发工具: pytest, black, flake8, mypy, sphinx等

### Breaking Changes
- 无（初始版本）

### Deprecated
- 无（初始版本）

### Removed
- 无（初始版本）

### Fixed
- 无（初始版本）

### Security
- 实现API密钥安全管理
- 添加输入验证防止注入攻击
- 集成安全扫描工具

---

## 版本说明

### 版本号规则
本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)规范：
- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 发布周期
- **主版本**: 根据重大架构变更决定
- **次版本**: 每月发布，包含新功能和改进
- **修订版本**: 根据需要发布，主要修复bug

### 支持政策
- **当前版本**: 提供完整支持和新功能开发
- **前一个主版本**: 提供安全更新和重要bug修复
- **更早版本**: 仅提供安全更新

### 迁移指南
每个主版本发布时，我们会提供详细的迁移指南，帮助用户平滑升级。

---

## 贡献指南

我们欢迎社区贡献！请查看[CONTRIBUTING.md](CONTRIBUTING.md)了解如何参与项目开发。

## 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。