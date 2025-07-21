"""MetaGPT框架集成"""

from typing import List, Dict, Any, Optional, Union

from ..core.factory import LLMFactory
from ..core.exceptions import FrameworkError

try:
    from metagpt.roles import Role
    from metagpt.team import Team
    from metagpt.actions import Action
    METAGPT_AVAILABLE = True
except ImportError:
    METAGPT_AVAILABLE = False
    class Role: pass
    class Team: pass
    class Action: pass


class MetaGPTIntegration:
    """MetaGPT框架集成类"""
    
    @staticmethod
    def check_availability() -> bool:
        """检查MetaGPT是否可用"""
        return METAGPT_AVAILABLE
    
    @staticmethod
    def create_role(
        name: str,
        profile: str,
        goal: str,
        constraints: str,
        llm_provider: str,
        **llm_kwargs
    ) -> Role:
        """创建MetaGPT Role
        
        Args:
            name: 角色名称
            profile: 角色简介
            goal: 角色目标
            constraints: 约束条件
            llm_provider: LLM提供商
            **llm_kwargs: LLM参数
            
        Returns:
            Role实例
        """
        if not METAGPT_AVAILABLE:
            raise FrameworkError("MetaGPT is not installed", "metagpt")
        
        # 创建LLM实例（需要适配为MetaGPT兼容格式）
        llm = LLMFactory.create(llm_provider, **llm_kwargs)
        
        role = Role(
            name=name,
            profile=profile,
            goal=goal,
            constraints=constraints
        )
        
        return role
    
    @staticmethod
    def create_team(
        roles: List[Role],
        investment: float = 10.0,
        n_round: int = 5
    ) -> Team:
        """创建MetaGPT Team
        
        Args:
            roles: 角色列表
            investment: 投资预算
            n_round: 执行轮次
            
        Returns:
            Team实例
        """
        if not METAGPT_AVAILABLE:
            raise FrameworkError("MetaGPT is not installed", "metagpt")
        
        team = Team()
        for role in roles:
            team.hire(role)
        
        team.invest(investment)
        team.n_round = n_round
        
        return team
    
    @staticmethod
    def create_software_company(
        idea: str,
        investment: float = 3.0,
        n_round: int = 5
    ) -> Team:
        """创建软件公司团队
        
        Args:
            idea: 产品想法
            investment: 投资预算
            n_round: 执行轮次
            
        Returns:
            配置好的软件公司Team
        """
        if not METAGPT_AVAILABLE:
            raise FrameworkError("MetaGPT is not installed", "metagpt")
        
        # 这里需要导入具体的角色类
        try:
            from metagpt.roles import ProductManager, Architect, ProjectManager, Engineer, QaEngineer
            
            team = Team()
            team.hire([
                ProductManager(),
                Architect(),
                ProjectManager(),
                Engineer(),
                QaEngineer()
            ])
            
            team.invest(investment)
            team.n_round = n_round
            
            return team
        except ImportError:
            raise FrameworkError("MetaGPT roles not available", "metagpt")
    
    @staticmethod
    def get_framework_info() -> Dict[str, Any]:
        """获取框架信息"""
        return {
            "name": "MetaGPT",
            "description": "多Agent软件开发框架，模拟软件公司的开发流程",
            "available": METAGPT_AVAILABLE,
            "strengths": [
                "完整的软件开发流程",
                "角色分工明确",
                "自动化程度高",
                "支持复杂项目开发"
            ],
            "weaknesses": [
                "主要专注于软件开发",
                "定制化难度较大",
                "资源消耗较高",
                "学习成本较高"
            ],
            "use_cases": [
                "自动化软件开发",
                "原型快速开发",
                "需求分析和设计",
                "代码生成和测试"
            ],
            "installation": "pip install metagpt"
        }