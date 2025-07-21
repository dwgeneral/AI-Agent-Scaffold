"""LLM工厂类"""

from typing import Dict, Type, Optional, Any

from .base import BaseLLM
from .config import get_config, LLMConfig
from .exceptions import ProviderNotFoundError, ConfigError


class LLMFactory:
    """LLM工厂类，用于创建和管理LLM实例"""
    
    _providers: Dict[str, Type[BaseLLM]] = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseLLM]):
        """注册LLM提供商
        
        Args:
            name: 提供商名称
            provider_class: 提供商类
        """
        cls._providers[name] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """获取可用的提供商列表"""
        return list(cls._providers.keys())
    
    @classmethod
    def create(
        cls, 
        provider: str, 
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> BaseLLM:
        """创建LLM实例
        
        Args:
            provider: 提供商名称
            api_key: API密钥，如果不提供则从配置中获取
            base_url: 基础URL，如果不提供则从配置中获取
            model: 模型名称，如果不提供则从配置中获取
            **kwargs: 其他参数
            
        Returns:
            BaseLLM: LLM实例
            
        Raises:
            ProviderNotFoundError: 提供商不存在
            ConfigError: 配置错误
        """
        if provider not in cls._providers:
            raise ProviderNotFoundError(provider)
        
        # 获取配置
        config = get_config()
        llm_config = config.get_llm_config(provider)
        
        # 确定参数
        final_api_key = api_key
        final_base_url = base_url
        final_model = model
        
        if llm_config:
            final_api_key = final_api_key or llm_config.api_key
            final_base_url = final_base_url or llm_config.base_url
            final_model = final_model or llm_config.model
            
            # 合并配置参数
            config_kwargs = {
                "temperature": llm_config.temperature,
                "max_tokens": llm_config.max_tokens,
                "timeout": llm_config.timeout,
                "max_retries": llm_config.max_retries,
                **llm_config.extra_params
            }
            config_kwargs.update(kwargs)
            kwargs = config_kwargs
        
        if not final_api_key:
            raise ConfigError(f"API key not provided for provider '{provider}'")
        
        # 创建实例
        provider_class = cls._providers[provider]
        instance = provider_class(
            api_key=final_api_key,
            base_url=final_base_url,
            model=final_model,
            **kwargs
        )
        
        return instance
    
    @classmethod
    def create_from_config(cls, provider: str, config: LLMConfig) -> BaseLLM:
        """从配置创建LLM实例
        
        Args:
            provider: 提供商名称
            config: LLM配置
            
        Returns:
            BaseLLM: LLM实例
        """
        return cls.create(
            provider=provider,
            api_key=config.api_key,
            base_url=config.base_url,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout,
            max_retries=config.max_retries,
            **config.extra_params
        )
    
    @classmethod
    def auto_create(cls, provider: Optional[str] = None) -> BaseLLM:
        """自动创建LLM实例
        
        如果不指定provider，则使用配置中的默认provider
        
        Args:
            provider: 提供商名称，可选
            
        Returns:
            BaseLLM: LLM实例
        """
        config = get_config()
        
        if not provider:
            provider = config.global_config.default_provider
        
        return cls.create(provider)


# 自动注册提供商
def _auto_register_providers():
    """自动注册所有可用的提供商"""
    try:
        from ..adapters.zhipu import ZhipuLLM
        LLMFactory.register_provider("zhipu", ZhipuLLM)
    except ImportError:
        pass
    
    try:
        from ..adapters.moonshot import MoonshotLLM
        LLMFactory.register_provider("moonshot", MoonshotLLM)
    except ImportError:
        pass
    
    try:
        from ..adapters.tongyi import TongyiLLM
        LLMFactory.register_provider("tongyi", TongyiLLM)
    except ImportError:
        pass
    
    try:
        from ..adapters.volcano import VolcanoLLM
        LLMFactory.register_provider("volcano", VolcanoLLM)
    except ImportError:
        pass


# 在模块加载时自动注册
_auto_register_providers()