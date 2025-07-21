"""Agent框架集成示例

本示例展示如何使用AI Agent Scaffold SDK集成各种Agent框架。
"""

import os
import asyncio
from ai_agent_scaffold import LLMFactory
from ai_agent_scaffold.frameworks import (
    LangChainIntegration,
    LangGraphIntegration,
    CrewAIIntegration,
    LlamaIndexIntegration,
    AutoGenIntegration,
    MetaGPTIntegration,
    PocketFlowIntegration
)


def print_framework_info():
    """打印所有框架信息"""
    print("=== 支持的Agent框架信息 ===")
    
    frameworks = [
        LangChainIntegration,
        LangGraphIntegration,
        CrewAIIntegration,
        LlamaIndexIntegration,
        AutoGenIntegration,
        MetaGPTIntegration,
        PocketFlowIntegration
    ]
    
    for framework_class in frameworks:
        info = framework_class.get_framework_info()
        print(f"\n📚 {info['name']}")
        print(f"   描述: {info['description']}")
        print(f"   可用: {'✅' if info['available'] else '❌'}")
        print(f"   安装: {info['installation']}")
        
        if info['available']:
            print(f"   优势: {', '.join(info['strengths'][:2])}...")
            print(f"   用例: {', '.join(info['use_cases'][:2])}...")


def langchain_example():
    """LangChain集成示例"""
    print("\n=== LangChain集成示例 ===")
    
    if not LangChainIntegration.check_availability():
        print("❌ LangChain未安装，跳过示例")
        return
    
    try:
        # 创建LLM实例
        llm = LLMFactory.create(
            provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        
        # 创建LangChain适配器
        langchain_llm = LangChainIntegration.create_llm_adapter(llm)
        print("✅ LangChain LLM适配器创建成功")
        
        # 创建简单Agent
        agent = LangChainIntegration.create_simple_agent(
            llm=langchain_llm,
            tools=[],  # 暂时不添加工具
            system_message="你是一个有用的AI助手。"
        )
        print("✅ LangChain Agent创建成功")
        
        # 创建对话链
        conversation_chain = LangChainIntegration.create_conversation_chain(langchain_llm)
        print("✅ LangChain对话链创建成功")
        
        # 测试对话
        response = conversation_chain.predict(input="什么是LangChain？")
        print(f"🤖 Agent回复: {response[:100]}...")
        
    except Exception as e:
        print(f"❌ LangChain示例失败: {e}")


async def langgraph_example():
    """LangGraph集成示例"""
    print("\n=== LangGraph集成示例 ===")
    
    if not LangGraphIntegration.check_availability():
        print("❌ LangGraph未安装，跳过示例")
        return
    
    try:
        # 创建LLM实例
        llm = LLMFactory.create(
            provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        
        # 创建简单工作流
        workflow = LangGraphIntegration.create_simple_workflow(
            llm=llm,
            system_message="你是一个数学助手。"
        )
        print("✅ LangGraph简单工作流创建成功")
        
        # 创建Agent工作流
        agent_workflow = LangGraphIntegration.create_agent_workflow(
            llm=llm,
            tools=[],  # 暂时不添加工具
            system_message="你是一个问题解决专家。"
        )
        print("✅ LangGraph Agent工作流创建成功")
        
        # 测试工作流
        result = await workflow.ainvoke({
            "messages": ["计算 15 + 27 = ?"]
        })
        print(f"🤖 工作流结果: {str(result)[:100]}...")
        
    except Exception as e:
        print(f"❌ LangGraph示例失败: {e}")


def crewai_example():
    """CrewAI集成示例"""
    print("\n=== CrewAI集成示例 ===")
    
    if not CrewAIIntegration.check_availability():
        print("❌ CrewAI未安装，跳过示例")
        return
    
    try:
        # 创建研究员Agent
        researcher = CrewAIIntegration.create_agent(
            role="研究员",
            goal="收集和分析信息",
            backstory="你是一个经验丰富的研究员，擅长收集和分析各种信息。",
            llm_provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ CrewAI研究员Agent创建成功")
        
        # 创建写作员Agent
        writer = CrewAIIntegration.create_agent(
            role="写作员",
            goal="撰写高质量的内容",
            backstory="你是一个专业的写作员，能够将复杂的信息转化为易懂的内容。",
            llm_provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ CrewAI写作员Agent创建成功")
        
        # 创建任务
        research_task = CrewAIIntegration.create_task(
            description="研究人工智能的最新发展趋势",
            agent=researcher,
            expected_output="一份详细的研究报告"
        )
        
        writing_task = CrewAIIntegration.create_task(
            description="基于研究结果撰写一篇科普文章",
            agent=writer,
            expected_output="一篇1000字的科普文章"
        )
        
        # 创建团队
        crew = CrewAIIntegration.create_crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process="sequential"
        )
        print("✅ CrewAI团队创建成功")
        
        print("🚀 CrewAI团队配置完成，可以开始执行任务")
        
    except Exception as e:
        print(f"❌ CrewAI示例失败: {e}")


def llamaindex_example():
    """LlamaIndex集成示例"""
    print("\n=== LlamaIndex集成示例 ===")
    
    if not LlamaIndexIntegration.check_availability():
        print("❌ LlamaIndex未安装，跳过示例")
        return
    
    try:
        # 注意：这个示例需要实际的文档目录
        print("✅ LlamaIndex可用")
        print("📝 LlamaIndex主要用于文档索引和检索")
        print("💡 使用示例:")
        print("   1. 准备文档目录")
        print("   2. 调用 create_vector_index() 创建索引")
        print("   3. 调用 create_query_engine() 创建查询引擎")
        print("   4. 使用查询引擎进行问答")
        
        # 获取框架信息
        info = LlamaIndexIntegration.get_framework_info()
        print(f"🎯 适用场景: {', '.join(info['use_cases'])}")
        
    except Exception as e:
        print(f"❌ LlamaIndex示例失败: {e}")


def autogen_example():
    """AutoGen集成示例"""
    print("\n=== AutoGen集成示例 ===")
    
    if not AutoGenIntegration.check_availability():
        print("❌ AutoGen未安装，跳过示例")
        return
    
    try:
        # 创建用户代理
        user_proxy = AutoGenIntegration.create_agent(
            name="用户代理",
            system_message="你代表用户提出问题和需求。",
            llm_provider="zhipu",
            human_input_mode="NEVER",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ AutoGen用户代理创建成功")
        
        # 创建助手代理
        assistant = AutoGenIntegration.create_agent(
            name="AI助手",
            system_message="你是一个有用的AI助手，能够回答各种问题。",
            llm_provider="zhipu",
            human_input_mode="NEVER",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ AutoGen助手代理创建成功")
        
        # 创建群组聊天
        group_chat = AutoGenIntegration.create_group_chat(
            agents=[user_proxy, assistant],
            max_round=3
        )
        print("✅ AutoGen群组聊天创建成功")
        
        # 创建群组聊天管理器
        manager = AutoGenIntegration.create_group_chat_manager(
            group_chat=group_chat,
            llm_provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ AutoGen群组聊天管理器创建成功")
        
        print("🚀 AutoGen多Agent对话系统配置完成")
        
    except Exception as e:
        print(f"❌ AutoGen示例失败: {e}")


def metagpt_example():
    """MetaGPT集成示例"""
    print("\n=== MetaGPT集成示例 ===")
    
    if not MetaGPTIntegration.check_availability():
        print("❌ MetaGPT未安装，跳过示例")
        return
    
    try:
        # 创建产品经理角色
        pm = MetaGPTIntegration.create_role(
            name="产品经理",
            profile="负责产品规划和需求分析",
            goal="设计出用户喜爱的产品",
            constraints="必须考虑技术可行性和商业价值",
            llm_provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ MetaGPT产品经理角色创建成功")
        
        # 创建软件公司团队
        try:
            company = MetaGPTIntegration.create_software_company(
                idea="开发一个AI驱动的任务管理应用",
                investment=5.0,
                n_round=3
            )
            print("✅ MetaGPT软件公司团队创建成功")
        except Exception as e:
            print(f"⚠️ 软件公司团队创建失败: {e}")
            print("💡 可能需要安装完整的MetaGPT依赖")
        
        # 获取框架信息
        info = MetaGPTIntegration.get_framework_info()
        print(f"🎯 MetaGPT适用于: {', '.join(info['use_cases'])}")
        
    except Exception as e:
        print(f"❌ MetaGPT示例失败: {e}")


def pocketflow_example():
    """PocketFlow集成示例"""
    print("\n=== PocketFlow集成示例 ===")
    
    try:
        # 创建简单流程
        flow = PocketFlowIntegration.create_simple_flow(
            name="文本处理流程",
            llm_provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ PocketFlow简单流程创建成功")
        
        # 创建Agent节点
        analyzer_node = PocketFlowIntegration.create_agent_node(
            node_id="analyzer",
            role="文本分析师",
            instructions="分析输入文本的情感和主题",
            llm_provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        
        summarizer_node = PocketFlowIntegration.create_agent_node(
            node_id="summarizer",
            role="文本摘要师",
            instructions="为输入文本生成简洁的摘要",
            llm_provider="zhipu",
            api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
            model="glm-4"
        )
        print("✅ PocketFlow Agent节点创建成功")
        
        # 创建工作流
        workflow = PocketFlowIntegration.create_workflow(
            nodes=[analyzer_node, summarizer_node],
            connections=[
                {"from": "analyzer", "to": "summarizer"}
            ]
        )
        print("✅ PocketFlow工作流创建成功")
        
        # 执行工作流（模拟）
        result = PocketFlowIntegration.execute_workflow(
            workflow=workflow,
            input_data={"text": "这是一段需要处理的示例文本。"}
        )
        print(f"🚀 工作流执行结果: {result['status']}")
        
        # 获取框架信息
        info = PocketFlowIntegration.get_framework_info()
        if 'note' in info:
            print(f"📝 注意: {info['note']}")
        
    except Exception as e:
        print(f"❌ PocketFlow示例失败: {e}")


def main():
    """主函数"""
    print("AI Agent Scaffold SDK - Agent框架集成示例")
    print("=" * 60)
    
    # 检查环境变量
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        print("⚠️ 警告: ZHIPU_API_KEY环境变量未设置")
        print("某些示例可能无法正常运行")
        print("请设置: export ZHIPU_API_KEY='your-actual-api-key'")
        print()
    
    try:
        # 打印框架信息
        print_framework_info()
        
        # 运行各框架示例
        langchain_example()
        asyncio.run(langgraph_example())
        crewai_example()
        llamaindex_example()
        autogen_example()
        metagpt_example()
        pocketflow_example()
        
    except KeyboardInterrupt:
        print("\n示例被用户中断")
    except Exception as e:
        print(f"\n示例运行出错: {e}")
    
    print("\n🎉 Agent框架集成示例运行完成！")
    print("\n💡 提示:")
    print("- 安装相应的框架依赖以启用完整功能")
    print("- 查看各框架的详细文档了解更多用法")
    print("- 根据具体需求选择合适的框架")


if __name__ == "__main__":
    main()