"""核心模块测试"""

import pytest
from unittest.mock import Mock, patch
from ai_agent_scaffold.core.base import (
    MessageRole, Message, SystemMessage, UserMessage, 
    AssistantMessage, FunctionMessage, LLMResponse, BaseLLM
)
from ai_agent_scaffold.core.config import Config, LLMConfig, GlobalConfig
from ai_agent_scaffold.core.factory import LLMFactory
from ai_agent_scaffold.core.exceptions import (
    LLMError, ConfigError, ProviderNotFoundError
)


class TestMessage:
    """消息类测试"""
    
    def test_system_message_creation(self):
        """测试系统消息创建"""
        msg = SystemMessage(content="You are a helpful assistant.")
        assert msg.role == MessageRole.SYSTEM
        assert msg.content == "You are a helpful assistant."
        assert msg.timestamp is not None
    
    def test_user_message_creation(self):
        """测试用户消息创建"""
        msg = UserMessage(content="Hello, world!")
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello, world!"
    
    def test_assistant_message_creation(self):
        """测试助手消息创建"""
        msg = AssistantMessage(content="Hello! How can I help you?")
        assert msg.role == MessageRole.ASSISTANT
        assert msg.content == "Hello! How can I help you?"
    
    def test_function_message_creation(self):
        """测试函数消息创建"""
        msg = FunctionMessage(
            content="Function result",
            function_name="test_function"
        )
        assert msg.role == MessageRole.FUNCTION
        assert msg.function_name == "test_function"
    
    def test_message_to_dict(self):
        """测试消息转字典"""
        msg = UserMessage(content="Test message")
        msg_dict = msg.to_dict()
        
        assert msg_dict["role"] == "user"
        assert msg_dict["content"] == "Test message"
        assert "timestamp" in msg_dict
    
    def test_message_from_dict(self):
        """测试从字典创建消息"""
        msg_dict = {
            "role": "user",
            "content": "Test message"
        }
        
        msg = Message.from_dict(msg_dict)
        assert isinstance(msg, UserMessage)
        assert msg.content == "Test message"


class TestLLMResponse:
    """LLM响应测试"""
    
    def test_llm_response_creation(self):
        """测试LLM响应创建"""
        response = LLMResponse(
            content="Test response",
            model="test-model",
            usage={"prompt_tokens": 10, "completion_tokens": 5}
        )
        
        assert response.content == "Test response"
        assert response.model == "test-model"
        assert response.usage["prompt_tokens"] == 10
        assert response.finish_reason is None


class MockLLM(BaseLLM):
    """测试用的Mock LLM"""
    
    @property
    def provider_name(self) -> str:
        return "mock"
    
    @property
    def supported_models(self) -> list:
        return ["mock-model-1", "mock-model-2"]
    
    def chat(self, messages, **kwargs):
        return LLMResponse(
            content="Mock response",
            model=self.model,
            usage={"prompt_tokens": 10, "completion_tokens": 5}
        )
    
    async def astream(self, messages, **kwargs):
        from ai_agent_scaffold.core.base import StreamChunk
        yield StreamChunk(content="Mock ", delta="Mock ")
        yield StreamChunk(content="response", delta="response")
    
    def embedding(self, texts, **kwargs):
        return [[0.1, 0.2, 0.3] for _ in texts]


class TestBaseLLM:
    """BaseLLM测试"""
    
    def test_mock_llm_creation(self):
        """测试Mock LLM创建"""
        llm = MockLLM(api_key="test-key", model="mock-model-1")
        assert llm.provider_name == "mock"
        assert llm.model == "mock-model-1"
        assert "mock-model-1" in llm.supported_models
    
    def test_mock_llm_chat(self):
        """测试Mock LLM聊天"""
        llm = MockLLM(api_key="test-key", model="mock-model-1")
        messages = [UserMessage(content="Hello")]
        
        response = llm.chat(messages)
        assert isinstance(response, LLMResponse)
        assert response.content == "Mock response"
        assert response.model == "mock-model-1"
    
    @pytest.mark.asyncio
    async def test_mock_llm_stream(self):
        """测试Mock LLM流式响应"""
        llm = MockLLM(api_key="test-key", model="mock-model-1")
        messages = [UserMessage(content="Hello")]
        
        chunks = []
        async for chunk in llm.astream(messages):
            chunks.append(chunk)
        
        assert len(chunks) == 2
        assert chunks[0].delta == "Mock "
        assert chunks[1].delta == "response"
    
    def test_mock_llm_embedding(self):
        """测试Mock LLM嵌入"""
        llm = MockLLM(api_key="test-key", model="mock-model-1")
        texts = ["Hello", "World"]
        
        embeddings = llm.embedding(texts)
        assert len(embeddings) == 2
        assert len(embeddings[0]) == 3
        assert embeddings[0] == [0.1, 0.2, 0.3]


class TestConfig:
    """配置测试"""
    
    def test_llm_config_creation(self):
        """测试LLM配置创建"""
        config = LLMConfig(
            provider="test",
            api_key="test-key",
            model="test-model"
        )
        
        assert config.provider == "test"
        assert config.api_key == "test-key"
        assert config.model == "test-model"
        assert config.temperature == 0.7  # 默认值
    
    def test_global_config_creation(self):
        """测试全局配置创建"""
        llm_config = LLMConfig(
            provider="test",
            api_key="test-key",
            model="test-model"
        )
        
        global_config = GlobalConfig(
            default_llm=llm_config,
            log_level="INFO"
        )
        
        assert global_config.default_llm == llm_config
        assert global_config.log_level == "INFO"
        assert global_config.timeout == 30  # 默认值
    
    @patch.dict('os.environ', {'TEST_API_KEY': 'env-test-key'})
    def test_config_from_env(self):
        """测试从环境变量加载配置"""
        config = Config()
        
        # 测试环境变量读取
        api_key = config._get_env_var('TEST_API_KEY')
        assert api_key == 'env-test-key'
    
    def test_config_validation(self):
        """测试配置验证"""
        with pytest.raises(ValueError):
            # 无效的温度值
            LLMConfig(
                provider="test",
                api_key="test-key",
                model="test-model",
                temperature=2.0  # 超出范围
            )


class TestLLMFactory:
    """LLM工厂测试"""
    
    def setup_method(self):
        """测试前设置"""
        # 清理工厂状态
        LLMFactory._providers.clear()
        # 注册Mock提供商
        LLMFactory.register_provider("mock", MockLLM)
    
    def test_register_provider(self):
        """测试注册提供商"""
        assert "mock" in LLMFactory._providers
        assert LLMFactory._providers["mock"] == MockLLM
    
    def test_get_available_providers(self):
        """测试获取可用提供商"""
        providers = LLMFactory.get_available_providers()
        assert "mock" in providers
    
    def test_create_llm(self):
        """测试创建LLM实例"""
        llm = LLMFactory.create(
            provider="mock",
            api_key="test-key",
            model="mock-model-1"
        )
        
        assert isinstance(llm, MockLLM)
        assert llm.provider_name == "mock"
        assert llm.model == "mock-model-1"
    
    def test_create_llm_with_config(self):
        """测试使用配置创建LLM"""
        config = LLMConfig(
            provider="mock",
            api_key="test-key",
            model="mock-model-1"
        )
        
        llm = LLMFactory.create_from_config(config)
        assert isinstance(llm, MockLLM)
        assert llm.model == "mock-model-1"
    
    def test_create_unknown_provider(self):
        """测试创建未知提供商"""
        with pytest.raises(ProviderNotFoundError):
            LLMFactory.create(
                provider="unknown",
                api_key="test-key",
                model="test-model"
            )
    
    def test_auto_create_llm(self):
        """测试自动创建LLM"""
        # 设置默认配置
        config = Config()
        config._config = GlobalConfig(
            default_llm=LLMConfig(
                provider="mock",
                api_key="test-key",
                model="mock-model-1"
            )
        )
        
        with patch('ai_agent_scaffold.core.factory.get_config', return_value=config):
            llm = LLMFactory.auto_create()
            assert isinstance(llm, MockLLM)


class TestExceptions:
    """异常测试"""
    
    def test_llm_error(self):
        """测试LLM错误"""
        error = LLMError("Test error", "test-provider")
        assert str(error) == "Test error"
        assert error.provider == "test-provider"
    
    def test_config_error(self):
        """测试配置错误"""
        error = ConfigError("Invalid config")
        assert str(error) == "Invalid config"
    
    def test_provider_not_found_error(self):
        """测试提供商未找到错误"""
        error = ProviderNotFoundError("unknown-provider")
        assert "unknown-provider" in str(error)
        assert error.provider == "unknown-provider"


if __name__ == "__main__":
    pytest.main([__file__])