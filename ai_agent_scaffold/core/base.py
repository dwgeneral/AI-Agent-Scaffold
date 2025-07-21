"""核心基础类定义"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
from dataclasses import dataclass
from enum import Enum


class MessageRole(str, Enum):
    """消息角色枚举"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


@dataclass
class Message:
    """统一的消息格式"""
    role: MessageRole
    content: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "role": self.role.value,
            "content": self.content
        }
        if self.metadata:
            result["metadata"] = self.metadata
        return result


class SystemMessage(Message):
    """系统消息"""
    def __init__(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(MessageRole.SYSTEM, content, metadata)


class UserMessage(Message):
    """用户消息"""
    def __init__(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(MessageRole.USER, content, metadata)


class AssistantMessage(Message):
    """助手消息"""
    def __init__(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(MessageRole.ASSISTANT, content, metadata)


class FunctionMessage(Message):
    """函数调用消息"""
    def __init__(self, content: str, function_name: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(MessageRole.FUNCTION, content, metadata)
        self.function_name = function_name


@dataclass
class LLMResponse:
    """LLM响应格式"""
    content: str
    role: MessageRole = MessageRole.ASSISTANT
    metadata: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, Any]] = None
    
    def to_message(self) -> Message:
        """转换为消息格式"""
        return Message(self.role, self.content, self.metadata)


@dataclass
class StreamChunk:
    """流式响应块"""
    content: str
    is_complete: bool = False
    metadata: Optional[Dict[str, Any]] = None


class BaseLLM(ABC):
    """LLM基础抽象类"""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.base_url = base_url
        self.config = kwargs
    
    @abstractmethod
    async def chat(
        self, 
        messages: Union[str, List[Message]], 
        **kwargs
    ) -> LLMResponse:
        """异步聊天接口
        
        Args:
            messages: 消息内容，可以是字符串或消息列表
            **kwargs: 其他参数如temperature, max_tokens等
            
        Returns:
            LLMResponse: 响应结果
        """
        pass
    
    @abstractmethod
    async def stream(
        self, 
        messages: Union[str, List[Message]], 
        **kwargs
    ) -> AsyncGenerator[StreamChunk, None]:
        """异步流式聊天接口
        
        Args:
            messages: 消息内容，可以是字符串或消息列表
            **kwargs: 其他参数
            
        Yields:
            StreamChunk: 流式响应块
        """
        pass
    
    @abstractmethod
    async def embedding(
        self, 
        texts: Union[str, List[str]], 
        **kwargs
    ) -> List[List[float]]:
        """文本嵌入接口
        
        Args:
            texts: 文本内容
            **kwargs: 其他参数
            
        Returns:
            List[List[float]]: 嵌入向量列表
        """
        pass
    
    def _normalize_messages(self, messages: Union[str, List[Message]]) -> List[Message]:
        """标准化消息格式"""
        if isinstance(messages, str):
            return [UserMessage(messages)]
        return messages
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """LLM提供商名称"""
        pass
    
    @property
    @abstractmethod
    def supported_models(self) -> List[str]:
        """支持的模型列表"""
        pass