"""通义千问适配器"""

import json
import httpx
from typing import List, Dict, Any, Optional, Union, AsyncGenerator

from ..core.base import BaseLLM, Message, LLMResponse, StreamChunk, MessageRole
from ..core.exceptions import APIError, AuthenticationError, RateLimitError, NetworkError, TimeoutError


class TongyiLLM(BaseLLM):
    """通义千问 LLM适配器"""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None, model: Optional[str] = None, **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self.base_url = base_url or "https://dashscope.aliyuncs.com/api/v1"
        self.model = model or "qwen-turbo"
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", None)
        self.timeout = kwargs.get("timeout", 30.0)
        self.max_retries = kwargs.get("max_retries", 3)
        
        # 创建HTTP客户端
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
    
    @property
    def provider_name(self) -> str:
        return "tongyi"
    
    @property
    def supported_models(self) -> List[str]:
        return [
            "qwen-turbo",
            "qwen-plus",
            "qwen-max",
            "qwen-max-1201",
            "qwen-max-longcontext",
            "qwen1.5-72b-chat",
            "qwen1.5-14b-chat",
            "qwen1.5-7b-chat"
        ]
    
    def _convert_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """转换消息格式为通义千问格式"""
        converted = []
        for msg in messages:
            converted.append({
                "role": msg.role.value,
                "content": msg.content
            })
        return converted
    
    async def chat(
        self, 
        messages: Union[str, List[Message]], 
        **kwargs
    ) -> LLMResponse:
        """聊天接口"""
        normalized_messages = self._normalize_messages(messages)
        converted_messages = self._convert_messages(normalized_messages)
        
        # 构建请求参数
        request_data = {
            "model": kwargs.get("model", self.model),
            "input": {
                "messages": converted_messages
            },
            "parameters": {
                "temperature": kwargs.get("temperature", self.temperature),
                "result_format": "message"
            }
        }
        
        if self.max_tokens:
            request_data["parameters"]["max_tokens"] = kwargs.get("max_tokens", self.max_tokens)
        
        # 发送请求
        try:
            response = await self._client.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                json=request_data
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 解析响应
            if "output" in data and "choices" in data["output"]:
                choices = data["output"]["choices"]
                if len(choices) > 0:
                    choice = choices[0]
                    content = choice["message"]["content"]
                    
                    # 构建使用信息
                    usage = data["output"].get("usage", {})
                    
                    return LLMResponse(
                        content=content,
                        role=MessageRole.ASSISTANT,
                        usage=usage,
                        metadata={
                            "model": self.model,
                            "finish_reason": choice.get("finish_reason")
                        }
                    )
            
            raise APIError("Invalid response format from Tongyi API")
                
        except httpx.HTTPStatusError as e:
            await self._handle_http_error(e)
        except httpx.TimeoutException:
            raise TimeoutError(f"Request timeout after {self.timeout} seconds")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    async def stream(
        self, 
        messages: Union[str, List[Message]], 
        **kwargs
    ) -> AsyncGenerator[StreamChunk, None]:
        """流式聊天接口"""
        normalized_messages = self._normalize_messages(messages)
        converted_messages = self._convert_messages(normalized_messages)
        
        # 构建请求参数
        request_data = {
            "model": kwargs.get("model", self.model),
            "input": {
                "messages": converted_messages
            },
            "parameters": {
                "temperature": kwargs.get("temperature", self.temperature),
                "result_format": "message",
                "incremental_output": True
            }
        }
        
        if self.max_tokens:
            request_data["parameters"]["max_tokens"] = kwargs.get("max_tokens", self.max_tokens)
        
        try:
            # 通义千问使用SSE格式
            headers = self._client.headers.copy()
            headers["Accept"] = "text/event-stream"
            headers["X-DashScope-SSE"] = "enable"
            
            async with httpx.AsyncClient(headers=headers, timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/services/aigc/text-generation/generation",
                    json=request_data
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            data_str = line[5:].strip()  # 移除 "data:" 前缀
                            
                            if data_str == "[DONE]":
                                yield StreamChunk(content="", is_complete=True)
                                break
                            
                            try:
                                data = json.loads(data_str)
                                if "output" in data and "choices" in data["output"]:
                                    choices = data["output"]["choices"]
                                    if len(choices) > 0:
                                        choice = choices[0]
                                        content = choice["message"]["content"]
                                        
                                        if content:
                                            yield StreamChunk(
                                                content=content,
                                                metadata={
                                                    "model": self.model,
                                                    "finish_reason": choice.get("finish_reason")
                                                }
                                            )
                            except json.JSONDecodeError:
                                continue
                            
        except httpx.HTTPStatusError as e:
            await self._handle_http_error(e)
        except httpx.TimeoutException:
            raise TimeoutError(f"Request timeout after {self.timeout} seconds")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    async def embedding(
        self, 
        texts: Union[str, List[str]], 
        **kwargs
    ) -> List[List[float]]:
        """文本嵌入接口"""
        if isinstance(texts, str):
            texts = [texts]
        
        request_data = {
            "model": kwargs.get("model", "text-embedding-v1"),
            "input": {
                "texts": texts
            }
        }
        
        try:
            response = await self._client.post(
                f"{self.base_url}/services/embeddings/text-embedding/text-embedding",
                json=request_data
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "output" in data and "embeddings" in data["output"]:
                embeddings = []
                for item in data["output"]["embeddings"]:
                    embeddings.append(item["embedding"])
                return embeddings
            else:
                raise APIError("Invalid response format from Tongyi embedding API")
                
        except httpx.HTTPStatusError as e:
            await self._handle_http_error(e)
        except httpx.TimeoutException:
            raise TimeoutError(f"Request timeout after {self.timeout} seconds")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    async def _handle_http_error(self, error: httpx.HTTPStatusError):
        """处理HTTP错误"""
        status_code = error.response.status_code
        
        try:
            error_data = error.response.json()
            error_message = error_data.get("message", str(error))
        except:
            error_message = str(error)
        
        if status_code == 401:
            raise AuthenticationError(f"Authentication failed: {error_message}")
        elif status_code == 429:
            raise RateLimitError(f"Rate limit exceeded: {error_message}")
        else:
            raise APIError(f"API error: {error_message}", status_code)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()