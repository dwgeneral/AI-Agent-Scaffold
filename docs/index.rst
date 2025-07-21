AI Agent Scaffold 文档
======================

欢迎使用 AI Agent Scaffold！这是一个统一的Python SDK，用于快速集成各大LLM厂商API和主流Agent框架。

.. image:: https://img.shields.io/pypi/v/ai-agent-scaffold.svg
   :target: https://pypi.org/project/ai-agent-scaffold/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/ai-agent-scaffold.svg
   :target: https://pypi.org/project/ai-agent-scaffold/
   :alt: Python versions

.. image:: https://github.com/ai-agent-scaffold/ai-agent-scaffold/workflows/CI/badge.svg
   :target: https://github.com/ai-agent-scaffold/ai-agent-scaffold/actions
   :alt: CI status

.. image:: https://codecov.io/gh/ai-agent-scaffold/ai-agent-scaffold/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ai-agent-scaffold/ai-agent-scaffold
   :alt: Coverage

特性
----

🚀 **统一接口**
   - 支持多个主流LLM提供商（智谱AI、Moonshot、通义千问、火山引擎等）
   - 统一的API调用方式，轻松切换不同提供商
   - 支持同步和异步调用

🔧 **框架集成**
   - 无缝集成LangChain、LangGraph、CrewAI等主流Agent框架
   - 提供适配器模式，简化框架使用
   - 支持多Agent协作和工作流编排

⚡ **高性能**
   - HTTP连接池复用
   - 流式响应支持
   - 智能重试和错误处理
   - 并发控制和限流保护

🛡️ **安全可靠**
   - API密钥安全管理
   - 输入验证和清理
   - 完整的错误处理体系
   - 详细的日志记录

📦 **易于使用**
   - 简洁的API设计
   - 丰富的示例代码
   - 完整的类型注解
   - 详细的文档说明

快速开始
--------

安装
~~~~

.. code-block:: bash

   pip install ai-agent-scaffold

基础使用
~~~~~~~~

.. code-block:: python

   from ai_agent_scaffold import LLMFactory

   # 创建LLM实例
   llm = LLMFactory.create_llm("zhipu", model="glm-4")

   # 发送消息
   response = llm.chat("你好，世界！")
   print(response.content)

   # 流式响应
   for chunk in llm.stream("讲一个故事"):
       print(chunk.content, end="")

框架集成
~~~~~~~~

.. code-block:: python

   from ai_agent_scaffold.frameworks import LangChainIntegration

   # 创建LangChain集成
   integration = LangChainIntegration()
   
   # 创建LangChain适配器
   llm_adapter = integration.create_llm_adapter("zhipu", model="glm-4")
   
   # 创建简单Agent
   agent = integration.create_simple_agent(
       llm_adapter, 
       tools=[],
       system_message="你是一个有用的AI助手"
   )

目录
----

.. toctree::
   :maxdepth: 2
   :caption: 用户指南

   installation
   quickstart
   configuration
   providers
   frameworks
   examples

.. toctree::
   :maxdepth: 2
   :caption: API参考

   api/core
   api/adapters
   api/frameworks
   api/cli

.. toctree::
   :maxdepth: 2
   :caption: 开发者指南

   development/contributing
   development/architecture
   development/testing
   development/deployment

.. toctree::
   :maxdepth: 1
   :caption: 其他

   changelog
   license
   support

支持的LLM提供商
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - 提供商
     - 支持的模型
     - 功能
     - 状态
   * - 智谱AI
     - GLM-4, GLM-4V, GLM-3-Turbo
     - 聊天、流式、嵌入
     - ✅ 稳定
   * - Moonshot AI
     - moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k
     - 聊天、流式
     - ✅ 稳定
   * - 通义千问
     - qwen-turbo, qwen-plus, qwen-max
     - 聊天、流式、嵌入
     - ✅ 稳定
   * - 火山引擎
     - Doubao系列
     - 聊天、流式
     - ✅ 稳定

支持的Agent框架
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 20 20

   * - 框架
     - 描述
     - 集成状态
     - 文档
   * - LangChain
     - 构建LLM应用的框架
     - ✅ 完整
     - :doc:`frameworks/langchain`
   * - LangGraph
     - 构建有状态的多Actor应用
     - ✅ 完整
     - :doc:`frameworks/langgraph`
   * - CrewAI
     - 多Agent协作框架
     - ✅ 完整
     - :doc:`frameworks/crewai`
   * - LlamaIndex
     - 数据框架和RAG应用
     - ✅ 完整
     - :doc:`frameworks/llamaindex`
   * - AutoGen
     - 多Agent对话框架
     - ✅ 完整
     - :doc:`frameworks/autogen`
   * - MetaGPT
     - 多Agent软件开发框架
     - ✅ 完整
     - :doc:`frameworks/metagpt`

社区和支持
----------

- **GitHub**: https://github.com/ai-agent-scaffold/ai-agent-scaffold
- **文档**: https://ai-agent-scaffold.readthedocs.io/
- **PyPI**: https://pypi.org/project/ai-agent-scaffold/
- **问题反馈**: https://github.com/ai-agent-scaffold/ai-agent-scaffold/issues
- **讨论**: https://github.com/ai-agent-scaffold/ai-agent-scaffold/discussions

许可证
------

本项目采用 `MIT许可证 <https://github.com/ai-agent-scaffold/ai-agent-scaffold/blob/main/LICENSE>`_。

索引和表格
----------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`