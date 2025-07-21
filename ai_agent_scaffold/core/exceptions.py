"""统一异常处理模块"""

from typing import Optional, Dict, Any


class AIAgentScaffoldError(Exception):
    """AI Agent Scaffold基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class LLMError(AIAgentScaffoldError):
    """LLM相关异常"""
    pass


class ConfigError(AIAgentScaffoldError):
    """配置相关异常"""
    pass


class APIError(LLMError):
    """API调用异常"""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message, f"API_ERROR_{status_code}" if status_code else "API_ERROR")
        self.status_code = status_code
        self.response_data = response_data or {}


class RateLimitError(APIError):
    """API限流异常"""
    
    def __init__(self, message: str = "API rate limit exceeded", retry_after: Optional[int] = None):
        super().__init__(message, 429)
        self.retry_after = retry_after


class AuthenticationError(APIError):
    """认证异常"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class ModelNotFoundError(LLMError):
    """模型不存在异常"""
    
    def __init__(self, model_name: str, provider: str):
        message = f"Model '{model_name}' not found for provider '{provider}'"
        super().__init__(message, "MODEL_NOT_FOUND")
        self.model_name = model_name
        self.provider = provider


class ProviderNotFoundError(LLMError):
    """提供商不存在异常"""
    
    def __init__(self, provider_name: str):
        message = f"LLM provider '{provider_name}' not found"
        super().__init__(message, "PROVIDER_NOT_FOUND")
        self.provider_name = provider_name


class ValidationError(AIAgentScaffoldError):
    """数据验证异常"""
    pass


class TimeoutError(APIError):
    """请求超时异常"""
    
    def __init__(self, message: str = "Request timeout", timeout_seconds: Optional[float] = None):
        super().__init__(message, "TIMEOUT")
        self.timeout_seconds = timeout_seconds


class NetworkError(APIError):
    """网络异常"""
    
    def __init__(self, message: str = "Network error occurred"):
        super().__init__(message, "NETWORK_ERROR")


class FrameworkError(AIAgentScaffoldError):
    """Agent框架相关异常"""
    
    def __init__(self, message: str, framework_name: str):
        super().__init__(message, f"FRAMEWORK_ERROR_{framework_name.upper()}")
        self.framework_name = framework_name