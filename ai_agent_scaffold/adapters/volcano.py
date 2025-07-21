"""火山引擎适配器"""

import json
import httpx
from typing import List, Dict, Any, Optional, Union, AsyncGenerator

from ..core.base import BaseLLM, Message, LLMResponse, StreamChunk, MessageRole
from ..core.exceptions import APIError, AuthenticationError, RateLimitError, NetworkError, TimeoutError


class VolcanoLLM(BaseLLM):
    """火山引擎 LLM适配器"""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None, model: Optional[str] = None, **kwargs):
        super().__init__(api_key, base_url, **kwargs)
        self.base_url = base_url or "https://ark.cn-beijing.volces.com/api/v3"
        self.model = model or "doubao-lite-4k"
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
        return "volcano"
    
    @property
    def supported_models(self) -> List[str]:
        return [
            "doubao-lite-4k",
            "doubao-lite-32k",
            "doubao-lite-128k",
            "doubao-pro-4k",
            "doubao-pro-32k",
            "doubao-pro-128k"
        ]
    
    def _convert_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """转换消息格式为火山引擎格式"""
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
            "messages": converted_messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": False
        }
        
        if self.max_tokens:
            request_data["max_tokens"] = kwargs.get("max_tokens", self.max_tokens)
        
        # 发送请求
        try:
            response = await self._client.post(
                f"{self.base_url}/chat/completions",
                json=request_data
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 解析响应
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                content = choice["message"]["content"]
                
                # 构建使用信息
                usage = data.get("usage", {})
                
                return LLMResponse(
                    content=content,
                    role=MessageRole.ASSISTANT,
                    usage=usage,
                    metadata={
                        "model": data.get("model"),
                        "finish_reason": choice.get("finish_reason")
                    }
                )
            else:
                raise APIError("Invalid response format from Volcano API")
                
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
            "messages": converted_messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": True
        }
        
        if self.max_tokens:
            request_data["max_tokens"] = kwargs.get("max_tokens", self.max_tokens)
        
        try:
            async with self._client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=request_data
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # 移除 "data: " 前缀
                        
                        if data_str.strip() == "[DONE]":
                            yield StreamChunk(content="", is_complete=True)
                            break
                        
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                choice = data["choices"][0]
                                delta = choice.get("delta", {})
                                content = delta.get("content", "")
                                
                                if content:
                                    yield StreamChunk(
                                        content=content,
                                        metadata={
                                            "model": data.get("model"),
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
            "model": kwargs.get("model", "doubao-embedding"),
            "input": texts
        }
        
        try:
            response = await self._client.post(
                f"{self.base_url}/embeddings",
                json=request_data
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "data" in data:
                embeddings = []
                for item in data["data"]:
                    embeddings.append(item["embedding"])
                return embeddings
            else:
                raise APIError("Invalid response format from Volcano embedding API")
                
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
            error_message = error_data.get("error", {}).get("message", str(error))
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