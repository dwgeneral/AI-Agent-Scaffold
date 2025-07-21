"""AutoGen框架集成"""

from typing import List, Dict, Any, Optional, Union

from ..core.factory import LLMFactory
from ..core.exceptions import FrameworkError

try:
    from autogen import ConversableAgent, GroupChat, GroupChatManager
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    class ConversableAgent: pass
    class GroupChat: pass
    class GroupChatManager: pass


class AutoGenIntegration:
    """AutoGen框架集成类"""
    
    @staticmethod
    def check_availability() -> bool:
        """检查AutoGen是否可用"""
        return AUTOGEN_AVAILABLE
    
    @staticmethod
    def create_agent(
        name: str,
        system_message: str,
        llm_provider: str,
        human_input_mode: str = "NEVER",
        **llm_kwargs
    ) -> ConversableAgent:
        """创建AutoGen Agent
        
        Args:
            name: Agent名称
            system_message: 系统消息
            llm_provider: LLM提供商
            human_input_mode: 人工输入模式
            **llm_kwargs: LLM参数
            
        Returns:
            ConversableAgent实例
        """
        if not AUTOGEN_AVAILABLE:
            raise FrameworkError("AutoGen is not installed", "autogen")
        
        # 创建LLM配置（需要适配为AutoGen兼容格式）
        llm_config = {
            "model": llm_kwargs.get("model", "gpt-3.5-turbo"),
            "api_key": llm_kwargs.get("api_key"),
            "base_url": llm_kwargs.get("base_url"),
            "temperature": llm_kwargs.get("temperature", 0.7)
        }
        
        agent = ConversableAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode=human_input_mode
        )
        
        return agent
    
    @staticmethod
    def create_group_chat(
        agents: List[ConversableAgent],
        messages: Optional[List[Dict]] = None,
        max_round: int = 10
    ) -> GroupChat:
        """创建群组聊天
        
        Args:
            agents: Agent列表
            messages: 初始消息
            max_round: 最大轮次
            
        Returns:
            GroupChat实例
        """
        if not AUTOGEN_AVAILABLE:
            raise FrameworkError("AutoGen is not installed", "autogen")
        
        group_chat = GroupChat(
            agents=agents,
            messages=messages or [],
            max_round=max_round
        )
        
        return group_chat
    
    @staticmethod
    def create_group_chat_manager(
        group_chat: GroupChat,
        llm_provider: str,
        **llm_kwargs
    ) -> GroupChatManager:
        """创建群组聊天管理器
        
        Args:
            group_chat: 群组聊天
            llm_provider: LLM提供商
            **llm_kwargs: LLM参数
            
        Returns:
            GroupChatManager实例
        """
        if not AUTOGEN_AVAILABLE:
            raise FrameworkError("AutoGen is not installed", "autogen")
        
        # 创建LLM配置
        llm_config = {
            "model": llm_kwargs.get("model", "gpt-3.5-turbo"),
            "api_key": llm_kwargs.get("api_key"),
            "base_url": llm_kwargs.get("base_url"),
            "temperature": llm_kwargs.get("temperature", 0.7)
        }
        
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=llm_config
        )
        
        return manager
    
    @staticmethod
    def get_framework_info() -> Dict[str, Any]:
        """获取框架信息"""
        return {
            "name": "AutoGen",
            "description": "微软开发的多Agent对话框架，支持复杂的多轮对话",
            "available": AUTOGEN_AVAILABLE,
            "strengths": [
                "强大的多Agent对话能力",
                "支持人机交互",
                "灵活的对话流程控制",
                "丰富的Agent角色定义"
            ],
            "weaknesses": [
                "主要专注于对话场景",
                "配置相对复杂",
                "资源消耗较大"
            ],
            "use_cases": [
                "多Agent协作对话",
                "代码生成和审查",
                "问题解决和决策",
                "教育和培训场景"
            ],
            "installation": "pip install pyautogen"
        }