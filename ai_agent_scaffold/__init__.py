"""AI Agent Scaffold SDK - 高质量的Python AI Agent开发脚手架

一个统一的SDK，用于快速集成各大LLM厂商API和主流Agent框架。
"""

__version__ = "0.1.0"
__author__ = "AI Agent Scaffold Team"
__email__ = "contact@ai-agent-scaffold.com"

from .core.factory import LLMFactory
from .core.base import BaseLLM, Message, SystemMessage, UserMessage, AssistantMessage
from .core.config import Config
from .core.exceptions import (
    AIAgentScaffoldError,
    LLMError,
    ConfigError,
    APIError,
    RateLimitError,
    AuthenticationError
)

__all__ = [
    "LLMFactory",
    "BaseLLM",
    "Message",
    "SystemMessage", 
    "UserMessage",
    "AssistantMessage",
    "Config",
    "AIAgentScaffoldError",
    "LLMError",
    "ConfigError",
    "APIError",
    "RateLimitError",
    "AuthenticationError"
]