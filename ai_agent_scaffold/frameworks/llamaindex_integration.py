"""LlamaIndex框架集成"""

from typing import List, Dict, Any, Optional, Union

from ..core.factory import LLMFactory
from ..core.exceptions import FrameworkError

try:
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
    from llama_index.core.llms import LLM
    from llama_index.core.query_engine import BaseQueryEngine
    LLAMAINDEX_AVAILABLE = True
except ImportError:
    LLAMAINDEX_AVAILABLE = False
    class VectorStoreIndex: pass
    class SimpleDirectoryReader: pass
    class Settings: pass
    class LLM: pass
    class BaseQueryEngine: pass


class LlamaIndexIntegration:
    """LlamaIndex框架集成类"""
    
    @staticmethod
    def check_availability() -> bool:
        """检查LlamaIndex是否可用"""
        return LLAMAINDEX_AVAILABLE
    
    @staticmethod
    def create_vector_index(
        documents_path: str,
        llm_provider: str,
        **llm_kwargs
    ) -> VectorStoreIndex:
        """创建向量索引
        
        Args:
            documents_path: 文档路径
            llm_provider: LLM提供商
            **llm_kwargs: LLM参数
            
        Returns:
            VectorStoreIndex实例
        """
        if not LLAMAINDEX_AVAILABLE:
            raise FrameworkError("LlamaIndex is not installed", "llamaindex")
        
        # 加载文档
        documents = SimpleDirectoryReader(documents_path).load_data()
        
        # 设置LLM（需要适配为LlamaIndex兼容格式）
        llm = LLMFactory.create(llm_provider, **llm_kwargs)
        
        # 创建索引
        index = VectorStoreIndex.from_documents(documents)
        
        return index
    
    @staticmethod
    def create_query_engine(
        index: VectorStoreIndex,
        llm_provider: str,
        **llm_kwargs
    ) -> BaseQueryEngine:
        """创建查询引擎
        
        Args:
            index: 向量索引
            llm_provider: LLM提供商
            **llm_kwargs: LLM参数
            
        Returns:
            查询引擎实例
        """
        if not LLAMAINDEX_AVAILABLE:
            raise FrameworkError("LlamaIndex is not installed", "llamaindex")
        
        # 创建查询引擎
        query_engine = index.as_query_engine()
        
        return query_engine
    
    @staticmethod
    def get_framework_info() -> Dict[str, Any]:
        """获取框架信息"""
        return {
            "name": "LlamaIndex",
            "description": "专注于数据索引和检索的框架，特别适合RAG应用",
            "available": LLAMAINDEX_AVAILABLE,
            "strengths": [
                "强大的数据索引能力",
                "丰富的数据连接器",
                "优秀的检索性能",
                "支持多种向量数据库"
            ],
            "weaknesses": [
                "主要专注于检索，Agent功能有限",
                "学习曲线较陡峭",
                "配置相对复杂"
            ],
            "use_cases": [
                "RAG应用开发",
                "文档问答系统",
                "知识库检索",
                "企业搜索"
            ],
            "installation": "pip install llama-index"
        }