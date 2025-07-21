"""LangChain框架集成"""

from typing import List, Dict, Any, Optional, Union
import asyncio
from abc import ABC, abstractmethod

from ..core.base import BaseLLM, Message
from ..core.factory import LLMFactory
from ..core.exceptions import FrameworkError

try:
    from langchain.llms.base import LLM
    from langchain.chat_models.base import BaseChatModel
    from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain.tools import Tool
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.memory import ConversationBufferMemory
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    # 创建占位符类
    class LLM: pass
    class BaseChatModel: pass
    class BaseMessage: pass
    class HumanMessage: pass
    class AIMessage: pass
    class SystemMessage: pass
    class AgentExecutor: pass
    class Tool: pass
    class ChatPromptTemplate: pass
    class MessagesPlaceholder: pass
    class ConversationBufferMemory: pass


class LangChainLLMAdapter(BaseChatModel):
    """将我们的LLM适配为LangChain的ChatModel"""
    
    def __init__(self, llm: BaseLLM):
        super().__init__()
        self.llm = llm
    
    def _generate(self, messages: List[BaseMessage], **kwargs) -> Any:
        """同步生成方法"""
        # 转换消息格式
        converted_messages = self._convert_messages(messages)
        
        # 使用asyncio运行异步方法
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(self.llm.chat(converted_messages, **kwargs))
            return self._create_chat_result(response.content)
        finally:
            loop.close()
    
    async def _agenerate(self, messages: List[BaseMessage], **kwargs) -> Any:
        """异步生成方法"""
        # 转换消息格式
        converted_messages = self._convert_messages(messages)
        
        response = await self.llm.chat(converted_messages, **kwargs)
        return self._create_chat_result(response.content)
    
    def _convert_messages(self, messages: List[BaseMessage]) -> List[Message]:
        """转换LangChain消息为我们的消息格式"""
        converted = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                converted.append(Message("user", msg.content))
            elif isinstance(msg, AIMessage):
                converted.append(Message("assistant", msg.content))
            elif isinstance(msg, SystemMessage):
                converted.append(Message("system", msg.content))
        return converted
    
    def _create_chat_result(self, content: str):
        """创建LangChain ChatResult"""
        if not LANGCHAIN_AVAILABLE:
            return {"content": content}
        
        from langchain.schema import ChatResult, ChatGeneration
        return ChatResult(
            generations=[
                ChatGeneration(message=AIMessage(content=content))
            ]
        )
    
    @property
    def _llm_type(self) -> str:
        return f"ai_agent_scaffold_{self.llm.provider_name}"


class LangChainIntegration:
    """LangChain框架集成类"""
    
    @staticmethod
    def check_availability() -> bool:
        """检查LangChain是否可用"""
        return LANGCHAIN_AVAILABLE
    
    @staticmethod
    def create_llm_adapter(llm_provider: str, **kwargs) -> BaseChatModel:
        """创建LangChain LLM适配器
        
        Args:
            llm_provider: LLM提供商名称
            **kwargs: LLM参数
            
        Returns:
            BaseChatModel: LangChain兼容的ChatModel
        """
        if not LANGCHAIN_AVAILABLE:
            raise FrameworkError("LangChain is not installed", "langchain")
        
        llm = LLMFactory.create(llm_provider, **kwargs)
        return LangChainLLMAdapter(llm)
    
    @staticmethod
    def create_simple_agent(
        llm_provider: str,
        tools: Optional[List[Tool]] = None,
        system_message: str = "You are a helpful assistant.",
        **llm_kwargs
    ) -> AgentExecutor:
        """创建简单的LangChain Agent
        
        Args:
            llm_provider: LLM提供商名称
            tools: 工具列表
            system_message: 系统消息
            **llm_kwargs: LLM参数
            
        Returns:
            AgentExecutor: LangChain Agent执行器
        """
        if not LANGCHAIN_AVAILABLE:
            raise FrameworkError("LangChain is not installed", "langchain")
        
        # 创建LLM适配器
        llm = LangChainIntegration.create_llm_adapter(llm_provider, **llm_kwargs)
        
        # 创建提示模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # 创建Agent
        tools = tools or []
        agent = create_openai_functions_agent(llm, tools, prompt)
        
        # 创建内存
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建Agent执行器
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True
        )
        
        return agent_executor
    
    @staticmethod
    def create_rag_chain(
        llm_provider: str,
        retriever,
        system_template: str = "Use the following context to answer the question:\n{context}",
        **llm_kwargs
    ):
        """创建RAG链
        
        Args:
            llm_provider: LLM提供商名称
            retriever: 检索器
            system_template: 系统模板
            **llm_kwargs: LLM参数
            
        Returns:
            RAG链
        """
        if not LANGCHAIN_AVAILABLE:
            raise FrameworkError("LangChain is not installed", "langchain")
        
        from langchain.chains import RetrievalQA
        from langchain.prompts import PromptTemplate
        
        # 创建LLM适配器
        llm = LangChainIntegration.create_llm_adapter(llm_provider, **llm_kwargs)
        
        # 创建提示模板
        prompt_template = PromptTemplate(
            template=system_template + "\n\nQuestion: {question}\nAnswer:",
            input_variables=["context", "question"]
        )
        
        # 创建RAG链
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt_template}
        )
        
        return qa_chain
    
    @staticmethod
    def create_conversation_chain(
        llm_provider: str,
        system_message: str = "You are a helpful assistant.",
        **llm_kwargs
    ):
        """创建对话链
        
        Args:
            llm_provider: LLM提供商名称
            system_message: 系统消息
            **llm_kwargs: LLM参数
            
        Returns:
            对话链
        """
        if not LANGCHAIN_AVAILABLE:
            raise FrameworkError("LangChain is not installed", "langchain")
        
        from langchain.chains import ConversationChain
        from langchain.prompts import PromptTemplate
        
        # 创建LLM适配器
        llm = LangChainIntegration.create_llm_adapter(llm_provider, **llm_kwargs)
        
        # 创建内存
        memory = ConversationBufferMemory()
        
        # 创建提示模板
        template = f"""{system_message}

Current conversation:
{{history}}
Human: {{input}}
AI:"""
        
        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )
        
        # 创建对话链
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        )
        
        return conversation
    
    @staticmethod
    def get_framework_info() -> Dict[str, Any]:
        """获取框架信息"""
        return {
            "name": "LangChain",
            "description": "最流行的LLM应用开发框架，提供丰富的组件和工具",
            "available": LANGCHAIN_AVAILABLE,
            "strengths": [
                "生态系统丰富，组件齐全",
                "社区活跃，文档完善",
                "支持多种LLM和工具集成",
                "RAG和Agent开发便捷"
            ],
            "weaknesses": [
                "学习曲线较陡峭",
                "抽象层次较高，定制化困难",
                "性能开销相对较大"
            ],
            "use_cases": [
                "快速原型开发",
                "RAG应用",
                "多工具Agent",
                "对话系统"
            ],
            "installation": "pip install langchain"
        }