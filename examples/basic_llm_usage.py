"""基础LLM使用示例

本示例展示如何使用AI Agent Scaffold SDK进行基础的LLM调用。
"""

import asyncio
import os
from ai_agent_scaffold import LLMFactory, UserMessage, SystemMessage


def basic_chat_example():
    """基础聊天示例"""
    print("=== 基础聊天示例 ===")
    
    # 创建LLM实例 - 智谱AI
    llm = LLMFactory.create(
        provider="zhipu",
        api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
        model="glm-4"
    )
    
    # 准备消息
    messages = [
        SystemMessage(content="你是一个有用的AI助手。"),
        UserMessage(content="请介绍一下人工智能的发展历史。")
    ]
    
    # 发送请求
    try:
        response = llm.chat(messages)
        print(f"回复: {response.content}")
        print(f"使用的模型: {response.model}")
        print(f"Token使用情况: {response.usage}")
    except Exception as e:
        print(f"请求失败: {e}")


async def streaming_chat_example():
    """流式聊天示例"""
    print("\n=== 流式聊天示例 ===")
    
    # 创建LLM实例 - Moonshot
    llm = LLMFactory.create(
        provider="moonshot",
        api_key=os.getenv("MOONSHOT_API_KEY", "your-api-key"),
        model="moonshot-v1-8k"
    )
    
    # 准备消息
    messages = [
        SystemMessage(content="你是一个创意写作助手。"),
        UserMessage(content="请写一首关于春天的短诗。")
    ]
    
    # 流式请求
    try:
        print("AI回复: ", end="", flush=True)
        async for chunk in llm.stream(messages):
            if chunk.content:
                print(chunk.content, end="", flush=True)
        print()  # 换行
    except Exception as e:
        print(f"流式请求失败: {e}")


def multi_provider_example():
    """多厂商对比示例"""
    print("\n=== 多厂商对比示例 ===")
    
    # 配置多个LLM提供商
    providers = [
        {
            "name": "智谱AI",
            "provider": "zhipu",
            "api_key": os.getenv("ZHIPU_API_KEY", "your-api-key"),
            "model": "glm-4"
        },
        {
            "name": "通义千问",
            "provider": "tongyi",
            "api_key": os.getenv("TONGYI_API_KEY", "your-api-key"),
            "model": "qwen-turbo"
        },
        {
            "name": "火山引擎",
            "provider": "volcano",
            "api_key": os.getenv("VOLCANO_API_KEY", "your-api-key"),
            "model": "doubao-lite-4k"
        }
    ]
    
    question = "什么是机器学习？请用一句话简单解释。"
    messages = [UserMessage(content=question)]
    
    for config in providers:
        try:
            llm = LLMFactory.create(
                provider=config["provider"],
                api_key=config["api_key"],
                model=config["model"]
            )
            
            response = llm.chat(messages)
            print(f"\n{config['name']} ({config['model']})的回答:")
            print(f"{response.content}")
            
        except Exception as e:
            print(f"\n{config['name']}请求失败: {e}")


def embedding_example():
    """文本嵌入示例"""
    print("\n=== 文本嵌入示例 ===")
    
    # 创建LLM实例
    llm = LLMFactory.create(
        provider="zhipu",
        api_key=os.getenv("ZHIPU_API_KEY", "your-api-key"),
        model="embedding-2"
    )
    
    # 文本列表
    texts = [
        "人工智能是计算机科学的一个分支",
        "机器学习是人工智能的核心技术",
        "深度学习是机器学习的一个子领域",
        "今天天气很好，适合出去散步"
    ]
    
    try:
        # 获取嵌入向量
        embeddings = llm.embedding(texts)
        
        print(f"成功获取 {len(embeddings)} 个文本的嵌入向量")
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            print(f"文本 {i+1}: {text}")
            print(f"嵌入维度: {len(embedding)}")
            print(f"前5个维度: {embedding[:5]}")
            print()
            
    except Exception as e:
        print(f"嵌入请求失败: {e}")


def factory_info_example():
    """工厂信息示例"""
    print("\n=== 可用提供商信息 ===")
    
    # 获取所有可用的提供商
    providers = LLMFactory.get_available_providers()
    
    print("当前支持的LLM提供商:")
    for provider in providers:
        print(f"- {provider}")
    
    # 获取特定提供商的信息
    for provider in providers:
        try:
            # 创建一个临时实例来获取支持的模型
            llm = LLMFactory.create(
                provider=provider,
                api_key="dummy",  # 临时密钥
                model="dummy"     # 临时模型
            )
            print(f"\n{provider} 支持的模型: {llm.supported_models}")
        except Exception:
            print(f"\n{provider} 信息获取失败")


def main():
    """主函数"""
    print("AI Agent Scaffold SDK - 基础LLM使用示例")
    print("=" * 50)
    
    # 检查环境变量
    required_keys = [
        "ZHIPU_API_KEY", "MOONSHOT_API_KEY", 
        "TONGYI_API_KEY", "VOLCANO_API_KEY"
    ]
    
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print("警告: 以下环境变量未设置，相关示例可能无法运行:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\n请设置相应的API密钥后重新运行示例。")
        print("示例: export ZHIPU_API_KEY='your-actual-api-key'")
        print()
    
    # 运行示例
    try:
        # 基础聊天
        basic_chat_example()
        
        # 流式聊天
        asyncio.run(streaming_chat_example())
        
        # 多厂商对比
        multi_provider_example()
        
        # 文本嵌入
        embedding_example()
        
        # 工厂信息
        factory_info_example()
        
    except KeyboardInterrupt:
        print("\n示例被用户中断")
    except Exception as e:
        print(f"\n示例运行出错: {e}")
    
    print("\n示例运行完成！")


if __name__ == "__main__":
    main()