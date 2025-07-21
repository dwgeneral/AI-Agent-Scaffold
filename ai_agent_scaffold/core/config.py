"""配置管理模块"""

import os
import json
import yaml
from typing import Dict, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field

from .exceptions import ConfigError


@dataclass
class LLMConfig:
    """LLM配置"""
    provider: str
    api_key: str
    base_url: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: float = 30.0
    max_retries: int = 3
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FrameworkConfig:
    """Agent框架配置"""
    framework: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GlobalConfig:
    """全局配置"""
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    async_timeout: float = 60.0
    default_provider: str = "zhipu"
    cache_enabled: bool = True
    cache_ttl: int = 3600


class Config:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        self.config_file = Path(config_file) if config_file else None
        self._llm_configs: Dict[str, LLMConfig] = {}
        self._framework_configs: Dict[str, FrameworkConfig] = {}
        self._global_config = GlobalConfig()
        
        # 加载配置
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        # 1. 从环境变量加载
        self._load_from_env()
        
        # 2. 从配置文件加载
        if self.config_file and self.config_file.exists():
            self._load_from_file()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        # 全局配置
        if os.getenv("AI_AGENT_LOG_LEVEL"):
            self._global_config.log_level = os.getenv("AI_AGENT_LOG_LEVEL")
        
        if os.getenv("AI_AGENT_DEFAULT_PROVIDER"):
            self._global_config.default_provider = os.getenv("AI_AGENT_DEFAULT_PROVIDER")
        
        # LLM配置
        providers = ["zhipu", "moonshot", "tongyi", "volcano"]
        for provider in providers:
            api_key_env = f"{provider.upper()}_API_KEY"
            base_url_env = f"{provider.upper()}_BASE_URL"
            model_env = f"{provider.upper()}_MODEL"
            
            if os.getenv(api_key_env):
                config = LLMConfig(
                    provider=provider,
                    api_key=os.getenv(api_key_env),
                    base_url=os.getenv(base_url_env),
                    model=os.getenv(model_env)
                )
                self._llm_configs[provider] = config
    
    def _load_from_file(self):
        """从配置文件加载"""
        try:
            if self.config_file.suffix.lower() in [".yaml", ".yml"]:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            elif self.config_file.suffix.lower() == ".json":
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                raise ConfigError(f"Unsupported config file format: {self.config_file.suffix}")
            
            # 解析配置
            self._parse_config_data(data)
            
        except Exception as e:
            raise ConfigError(f"Failed to load config file {self.config_file}: {str(e)}")
    
    def _parse_config_data(self, data: Dict[str, Any]):
        """解析配置数据"""
        # 全局配置
        if "global" in data:
            global_data = data["global"]
            for key, value in global_data.items():
                if hasattr(self._global_config, key):
                    setattr(self._global_config, key, value)
        
        # LLM配置
        if "llm" in data:
            for provider, config_data in data["llm"].items():
                if "api_key" in config_data:
                    config = LLMConfig(
                        provider=provider,
                        **config_data
                    )
                    self._llm_configs[provider] = config
        
        # 框架配置
        if "frameworks" in data:
            for framework, config_data in data["frameworks"].items():
                config = FrameworkConfig(
                    framework=framework,
                    **config_data
                )
                self._framework_configs[framework] = config
    
    def get_llm_config(self, provider: str) -> Optional[LLMConfig]:
        """获取LLM配置"""
        return self._llm_configs.get(provider)
    
    def set_llm_config(self, provider: str, config: LLMConfig):
        """设置LLM配置"""
        self._llm_configs[provider] = config
    
    def get_framework_config(self, framework: str) -> Optional[FrameworkConfig]:
        """获取框架配置"""
        return self._framework_configs.get(framework)
    
    def set_framework_config(self, framework: str, config: FrameworkConfig):
        """设置框架配置"""
        self._framework_configs[framework] = config
    
    @property
    def global_config(self) -> GlobalConfig:
        """获取全局配置"""
        return self._global_config
    
    def get_available_providers(self) -> list[str]:
        """获取可用的LLM提供商列表"""
        return list(self._llm_configs.keys())
    
    def get_available_frameworks(self) -> list[str]:
        """获取可用的框架列表"""
        return list(self._framework_configs.keys())
    
    def save_to_file(self, file_path: Union[str, Path]):
        """保存配置到文件"""
        file_path = Path(file_path)
        
        # 构建配置数据
        config_data = {
            "global": {
                "log_level": self._global_config.log_level,
                "log_format": self._global_config.log_format,
                "async_timeout": self._global_config.async_timeout,
                "default_provider": self._global_config.default_provider,
                "cache_enabled": self._global_config.cache_enabled,
                "cache_ttl": self._global_config.cache_ttl
            },
            "llm": {},
            "frameworks": {}
        }
        
        # LLM配置
        for provider, config in self._llm_configs.items():
            config_data["llm"][provider] = {
                "api_key": config.api_key,
                "base_url": config.base_url,
                "model": config.model,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "timeout": config.timeout,
                "max_retries": config.max_retries,
                "extra_params": config.extra_params
            }
        
        # 框架配置
        for framework, config in self._framework_configs.items():
            config_data["frameworks"][framework] = {
                "enabled": config.enabled,
                "config": config.config
            }
        
        # 保存文件
        try:
            if file_path.suffix.lower() in [".yaml", ".yml"]:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            elif file_path.suffix.lower() == ".json":
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
            else:
                raise ConfigError(f"Unsupported config file format: {file_path.suffix}")
        except Exception as e:
            raise ConfigError(f"Failed to save config file {file_path}: {str(e)}")


# 全局配置实例
_global_config = None


def get_config() -> Config:
    """获取全局配置实例"""
    global _global_config
    if _global_config is None:
        # 尝试从默认位置加载配置文件
        default_config_paths = [
            Path.cwd() / "ai_agent_config.yaml",
            Path.cwd() / "ai_agent_config.yml",
            Path.cwd() / "ai_agent_config.json",
            Path.home() / ".ai_agent_config.yaml",
            Path.home() / ".ai_agent_config.yml",
            Path.home() / ".ai_agent_config.json"
        ]
        
        config_file = None
        for path in default_config_paths:
            if path.exists():
                config_file = path
                break
        
        _global_config = Config(config_file)
    
    return _global_config


def set_config(config: Config):
    """设置全局配置实例"""
    global _global_config
    _global_config = config