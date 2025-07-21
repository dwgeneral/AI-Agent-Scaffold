快速开始
========

本指南将帮助您快速上手 AI Agent Scaffold，从安装到创建您的第一个AI Agent应用。

安装
----

基础安装
~~~~~~~~

.. code-block:: bash

   pip install ai-agent-scaffold

这将安装核心功能，但不包含任何LLM提供商或Agent框架的依赖。

完整安装
~~~~~~~~

如果您想要安装所有支持的LLM提供商和Agent框架：

.. code-block:: bash

   pip install ai-agent-scaffold[full]

选择性安装
~~~~~~~~~~

您也可以根据需要选择性安装特定的LLM提供商或框架：

.. code-block:: bash

   # 安装特定LLM提供商
   pip install ai-agent-scaffold[zhipu,moonshot]
   
   # 安装特定Agent框架
   pip install ai-agent-scaffold[langchain,crewai]
   
   # 安装开发依赖
   pip install ai-agent-scaffold[dev]

配置
----

环境变量配置
~~~~~~~~~~~~

首先，您需要配置API密钥。创建一个 ``.env`` 文件：

.. code-block:: bash

   # 复制环境变量模板
   cp .env.example .env

然后编辑 ``.env`` 文件，添加您的API密钥：

.. code-block:: bash

   # 智谱AI
   ZHIPU_API_KEY=your_zhipu_api_key_here
   
   # Moonshot AI
   MOONSHOT_API_KEY=your_moonshot_api_key_here
   
   # 通义千问
   TONGYI_API_KEY=your_tongyi_api_key_here
   
   # 火山引擎
   VOLCANO_API_KEY=your_volcano_api_key_here
   VOLCANO_SECRET_KEY=your_volcano_secret_key_here

配置文件
~~~~~~~~

您也可以使用YAML配置文件：

.. code-block:: yaml

   # config.yaml
   llm:
     default_provider: "zhipu"
     default_model: "glm-4"
     timeout: 30
     max_retries: 3
   
   logging:
     level: "INFO"
     format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

基础使用
--------

创建LLM实例
~~~~~~~~~~~~

.. code-block:: python

   from ai_agent_scaffold import LLMFactory
   
   # 使用默认配置创建LLM实例
   llm = LLMFactory.create_llm("zhipu")
   
   # 指定模型
   llm = LLMFactory.create_llm("zhipu", model="glm-4")
   
   # 使用配置创建
   config = {
       "api_key": "your_api_key",
       "model": "glm-4",
       "timeout": 30
   }
   llm = LLMFactory.create_llm("zhipu", **config)

发送消息
~~~~~~~~

.. code-block:: python

   # 简单聊天
   response = llm.chat("你好，世界！")
   print(response.content)
   
   # 多轮对话
   from ai_agent_scaffold import Message
   
   messages = [
       Message.system("你是一个有用的AI助手"),
       Message.user("请介绍一下Python"),
   ]
   
   response = llm.chat(messages)
   print(response.content)

流式响应
~~~~~~~~

.. code-block:: python

   # 流式聊天
   for chunk in llm.stream("讲一个关于AI的故事"):
       print(chunk.content, end="", flush=True)
   print()  # 换行

文本嵌入
~~~~~~~~

.. code-block:: python

   # 获取文本嵌入（如果提供商支持）
   try:
       embedding = llm.embedding("这是一段测试文本")
       print(f"嵌入维度: {len(embedding)}")
   except NotImplementedError:
       print("当前提供商不支持嵌入功能")

错误处理
~~~~~~~~

.. code-block:: python

   from ai_agent_scaffold import LLMError, APIError, RateLimitError
   
   try:
       response = llm.chat("Hello")
       print(response.content)
   except RateLimitError as e:
       print(f"请求频率过高: {e}")
       print(f"建议: {e.suggestion}")
   except APIError as e:
       print(f"API错误: {e}")
   except LLMError as e:
       print(f"LLM错误: {e}")

Agent框架集成
-------------

LangChain集成
~~~~~~~~~~~~~

.. code-block:: python

   from ai_agent_scaffold.frameworks import LangChainIntegration
   
   # 检查LangChain是否可用
   integration = LangChainIntegration()
   if not integration.is_available():
       print("请安装LangChain: pip install langchain")
       exit(1)
   
   # 创建LangChain适配器
   llm_adapter = integration.create_llm_adapter("zhipu", model="glm-4")
   
   # 创建简单Agent
   agent = integration.create_simple_agent(
       llm_adapter,
       tools=[],
       system_message="你是一个有用的AI助手"
   )
   
   # 运行Agent
   result = agent.invoke({"input": "你好！"})
   print(result["output"])

CrewAI集成
~~~~~~~~~~

.. code-block:: python

   from ai_agent_scaffold.frameworks import CrewAIIntegration
   
   integration = CrewAIIntegration()
   if not integration.is_available():
       print("请安装CrewAI: pip install crewai")
       exit(1)
   
   # 创建Agent
   agent = integration.create_agent(
       role="研究员",
       goal="研究AI技术发展趋势",
       backstory="你是一个专业的AI研究员",
       llm_provider="zhipu",
       model="glm-4"
   )
   
   # 创建任务
   task = integration.create_task(
       description="分析当前AI技术的发展趋势",
       agent=agent
   )
   
   # 创建团队
   crew = integration.create_crew(
       agents=[agent],
       tasks=[task]
   )
   
   # 执行任务
   result = crew.kickoff()
   print(result)

命令行工具
----------

AI Agent Scaffold 提供了便捷的命令行工具：

创建新项目
~~~~~~~~~~

.. code-block:: bash

   # 创建新项目
   ai-agent-scaffold init my-ai-project
   
   # 进入项目目录
   cd my-ai-project
   
   # 安装依赖
   pip install -r requirements.txt
   
   # 配置环境变量
   cp .env.example .env
   # 编辑 .env 文件添加API密钥

查看信息
~~~~~~~~

.. code-block:: bash

   # 查看可用的LLM提供商
   ai-agent-scaffold providers
   
   # 查看可用的Agent框架
   ai-agent-scaffold frameworks
   
   # 查看当前配置
   ai-agent-scaffold config
   
   # 查看版本信息
   ai-agent-scaffold version

测试连接
~~~~~~~~

.. code-block:: bash

   # 测试LLM连接
   ai-agent-scaffold test zhipu
   
   # 测试特定模型
   ai-agent-scaffold test zhipu --model glm-4

完整示例
--------

智能客服系统
~~~~~~~~~~~~

以下是一个完整的智能客服系统示例：

.. code-block:: python

   from ai_agent_scaffold import LLMFactory, Message
   from ai_agent_scaffold.frameworks import LangChainIntegration
   
   class IntelligentCustomerService:
       def __init__(self, llm_provider="zhipu", model="glm-4"):
           self.llm = LLMFactory.create_llm(llm_provider, model=model)
           self.conversation_history = []
       
       def analyze_sentiment(self, text):
           """分析客户情感。"""
           prompt = f"请分析以下文本的情感倾向（积极/中性/消极）：{text}"
           response = self.llm.chat(prompt)
           return response.content.strip()
       
       def classify_intent(self, text):
           """分类客户意图。"""
           prompt = f"""请分类以下客户咨询的意图类型：
           1. 产品咨询
           2. 技术支持
           3. 投诉建议
           4. 订单查询
           5. 其他
           
           客户消息：{text}
           请只返回类型编号和名称。
           """
           response = self.llm.chat(prompt)
           return response.content.strip()
       
       def generate_response(self, customer_message):
           """生成客服响应。"""
           # 分析情感和意图
           sentiment = self.analyze_sentiment(customer_message)
           intent = self.classify_intent(customer_message)
           
           # 构建上下文
           context = f"""你是一个专业的客服代表。
           客户情感：{sentiment}
           咨询类型：{intent}
           
           请根据客户的情感和咨询类型，提供专业、友好的回复。
           """
           
           # 构建对话历史
           messages = [Message.system(context)]
           messages.extend(self.conversation_history)
           messages.append(Message.user(customer_message))
           
           # 生成回复
           response = self.llm.chat(messages)
           
           # 更新对话历史
           self.conversation_history.append(Message.user(customer_message))
           self.conversation_history.append(Message.assistant(response.content))
           
           # 保持历史记录在合理长度
           if len(self.conversation_history) > 10:
               self.conversation_history = self.conversation_history[-10:]
           
           return {
               "response": response.content,
               "sentiment": sentiment,
               "intent": intent
           }
   
   # 使用示例
   def main():
       customer_service = IntelligentCustomerService()
       
       print("智能客服系统已启动！输入 'quit' 退出。")
       
       while True:
           customer_input = input("\n客户: ")
           if customer_input.lower() == 'quit':
               break
           
           result = customer_service.generate_response(customer_input)
           
           print(f"\n[情感: {result['sentiment']}, 意图: {result['intent']}]")
           print(f"客服: {result['response']}")
   
   if __name__ == "__main__":
       main()

下一步
------

现在您已经了解了基础用法，可以继续探索：

- :doc:`configuration` - 详细的配置选项
- :doc:`providers` - 各LLM提供商的详细说明
- :doc:`frameworks` - Agent框架集成指南
- :doc:`examples` - 更多示例和用例
- :doc:`api/core` - 完整的API参考

如果遇到问题，请查看 :doc:`support` 或在 `GitHub <https://github.com/ai-agent-scaffold/ai-agent-scaffold/issues>`_ 上提交issue。