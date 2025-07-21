"""CrewAI框架集成"""

from typing import List, Dict, Any, Optional

from ..core.factory import LLMFactory
from ..core.exceptions import FrameworkError

try:
    from crewai import Agent, Task, Crew
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    class Agent: pass
    class Task: pass
    class Crew: pass


class CrewAIIntegration:
    """CrewAI框架集成类"""
    
    @staticmethod
    def check_availability() -> bool:
        """检查CrewAI是否可用"""
        return CREWAI_AVAILABLE
    
    @staticmethod
    def create_agent(
        role: str,
        goal: str,
        backstory: str,
        llm_provider: str,
        tools: Optional[List] = None,
        **llm_kwargs
    ) -> Agent:
        """创建CrewAI Agent
        
        Args:
            role: Agent角色
            goal: Agent目标
            backstory: Agent背景故事
            llm_provider: LLM提供商
            tools: 工具列表
            **llm_kwargs: LLM参数
            
        Returns:
            CrewAI Agent实例
        """
        if not CREWAI_AVAILABLE:
            raise FrameworkError("CrewAI is not installed", "crewai")
        
        # 创建LLM实例（这里需要适配为CrewAI兼容的格式）
        llm = LLMFactory.create(llm_provider, **llm_kwargs)
        
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=True,
            allow_delegation=False
        )
        
        return agent
    
    @staticmethod
    def create_task(
        description: str,
        agent: Agent,
        expected_output: Optional[str] = None
    ) -> Task:
        """创建CrewAI Task
        
        Args:
            description: 任务描述
            agent: 执行任务的Agent
            expected_output: 期望输出
            
        Returns:
            CrewAI Task实例
        """
        if not CREWAI_AVAILABLE:
            raise FrameworkError("CrewAI is not installed", "crewai")
        
        task = Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )
        
        return task
    
    @staticmethod
    def create_crew(
        agents: List[Agent],
        tasks: List[Task],
        process: str = "sequential"
    ) -> Crew:
        """创建CrewAI Crew
        
        Args:
            agents: Agent列表
            tasks: Task列表
            process: 执行流程 (sequential, hierarchical)
            
        Returns:
            CrewAI Crew实例
        """
        if not CREWAI_AVAILABLE:
            raise FrameworkError("CrewAI is not installed", "crewai")
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=process,
            verbose=2
        )
        
        return crew
    
    @staticmethod
    def get_framework_info() -> Dict[str, Any]:
        """获取框架信息"""
        return {
            "name": "CrewAI",
            "description": "多Agent协作框架，专注于团队合作和任务分配",
            "available": CREWAI_AVAILABLE,
            "strengths": [
                "专注多Agent协作",
                "简单易用的API",
                "内置角色和任务管理",
                "支持不同的执行流程"
            ],
            "weaknesses": [
                "相对较新，功能有限",
                "定制化能力较弱",
                "生态系统不够丰富"
            ],
            "use_cases": [
                "多Agent团队协作",
                "复杂任务分解",
                "角色扮演场景",
                "工作流自动化"
            ],
            "installation": "pip install crewai"
        }