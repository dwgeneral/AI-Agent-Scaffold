"""LangGraph框架集成"""

from typing import List, Dict, Any, Optional, Union, Callable
import asyncio

from ..core.base import BaseLLM, Message
from ..core.factory import LLMFactory
from ..core.exceptions import FrameworkError

try:
    from langgraph.graph import StateGraph, END
    from langgraph.prebuilt import ToolExecutor, ToolInvocation
    from langgraph.checkpoint.sqlite import SqliteSaver
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    # 创建占位符类
    class StateGraph: pass
    class ToolExecutor: pass
    class ToolInvocation: pass
    class SqliteSaver: pass
    END = "__end__"


class LangGraphIntegration:
    """LangGraph框架集成类"""
    
    @staticmethod
    def check_availability() -> bool:
        """检查LangGraph是否可用"""
        return LANGGRAPH_AVAILABLE
    
    @staticmethod
    def create_simple_workflow(
        llm_provider: str,
        nodes: Dict[str, Callable],
        edges: List[tuple],
        entry_point: str = "start",
        **llm_kwargs
    ):
        """创建简单的工作流
        
        Args:
            llm_provider: LLM提供商名称
            nodes: 节点字典 {节点名: 处理函数}
            edges: 边列表 [(from_node, to_node)]
            entry_point: 入口节点
            **llm_kwargs: LLM参数
            
        Returns:
            编译后的工作流
        """
        if not LANGGRAPH_AVAILABLE:
            raise FrameworkError("LangGraph is not installed", "langgraph")
        
        # 创建LLM实例
        llm = LLMFactory.create(llm_provider, **llm_kwargs)
        
        # 创建状态图
        workflow = StateGraph(dict)
        
        # 添加节点
        for node_name, node_func in nodes.items():
            # 包装节点函数以注入LLM
            def wrapped_func(state, func=node_func, llm_instance=llm):
                return func(state, llm_instance)
            workflow.add_node(node_name, wrapped_func)
        
        # 添加边
        for from_node, to_node in edges:
            if to_node == "END":
                workflow.add_edge(from_node, END)
            else:
                workflow.add_edge(from_node, to_node)
        
        # 设置入口点
        workflow.set_entry_point(entry_point)
        
        # 编译工作流
        app = workflow.compile()
        
        return app
    
    @staticmethod
    def create_agent_workflow(
        llm_provider: str,
        tools: Optional[List] = None,
        system_message: str = "You are a helpful assistant.",
        **llm_kwargs
    ):
        """创建Agent工作流
        
        Args:
            llm_provider: LLM提供商名称
            tools: 工具列表
            system_message: 系统消息
            **llm_kwargs: LLM参数
            
        Returns:
            Agent工作流
        """
        if not LANGGRAPH_AVAILABLE:
            raise FrameworkError("LangGraph is not installed", "langgraph")
        
        # 创建LLM实例
        llm = LLMFactory.create(llm_provider, **llm_kwargs)
        tools = tools or []
        
        # 定义状态
        class AgentState(dict):
            messages: List[Dict[str, str]]
            next_action: Optional[str] = None
        
        # 定义节点函数
        async def agent_node(state: AgentState, llm_instance: BaseLLM):
            """Agent推理节点"""
            messages = state.get("messages", [])
            
            # 添加系统消息
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, {"role": "system", "content": system_message})
            
            # 转换消息格式
            llm_messages = []
            for msg in messages:
                llm_messages.append(Message(msg["role"], msg["content"]))
            
            # 调用LLM
            response = await llm_instance.chat(llm_messages)
            
            # 更新状态
            new_messages = messages + [{"role": "assistant", "content": response.content}]
            
            return {
                "messages": new_messages,
                "next_action": "end" if not tools else "tool_check"
            }
        
        def tool_check_node(state: AgentState):
            """工具检查节点"""
            last_message = state["messages"][-1]
            
            # 简单的工具调用检测（实际应用中需要更复杂的逻辑）
            if "tool:" in last_message["content"].lower():
                return {**state, "next_action": "tool_execution"}
            else:
                return {**state, "next_action": "end"}
        
        def tool_execution_node(state: AgentState):
            """工具执行节点"""
            # 这里应该实现实际的工具执行逻辑
            # 为了简化，我们只是添加一个模拟的工具执行结果
            tool_result = "Tool execution completed."
            
            new_messages = state["messages"] + [
                {"role": "system", "content": f"Tool result: {tool_result}"}
            ]
            
            return {
                "messages": new_messages,
                "next_action": "agent"
            }
        
        # 创建工作流
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("agent", lambda state: asyncio.run(agent_node(state, llm)))
        
        if tools:
            workflow.add_node("tool_check", tool_check_node)
            workflow.add_node("tool_execution", tool_execution_node)
        
        # 设置入口点
        workflow.set_entry_point("agent")
        
        # 添加条件边
        if tools:
            workflow.add_conditional_edges(
                "agent",
                lambda state: state["next_action"],
                {
                    "tool_check": "tool_check",
                    "end": END
                }
            )
            
            workflow.add_conditional_edges(
                "tool_check",
                lambda state: state["next_action"],
                {
                    "tool_execution": "tool_execution",
                    "end": END
                }
            )
            
            workflow.add_edge("tool_execution", "agent")
        else:
            workflow.add_edge("agent", END)
        
        # 编译工作流
        app = workflow.compile()
        
        return app
    
    @staticmethod
    def create_multi_agent_workflow(
        agents_config: List[Dict[str, Any]],
        coordination_strategy: str = "sequential"
    ):
        """创建多Agent工作流
        
        Args:
            agents_config: Agent配置列表
            coordination_strategy: 协调策略 (sequential, parallel, conditional)
            
        Returns:
            多Agent工作流
        """
        if not LANGGRAPH_AVAILABLE:
            raise FrameworkError("LangGraph is not installed", "langgraph")
        
        # 定义多Agent状态
        class MultiAgentState(dict):
            messages: List[Dict[str, str]]
            current_agent: int = 0
            agent_results: List[str] = []
        
        # 创建工作流
        workflow = StateGraph(MultiAgentState)
        
        # 为每个Agent创建节点
        for i, agent_config in enumerate(agents_config):
            llm = LLMFactory.create(
                agent_config["llm_provider"],
                **agent_config.get("llm_kwargs", {})
            )
            
            def create_agent_node(agent_llm, agent_name, agent_prompt):
                async def agent_node(state: MultiAgentState):
                    messages = state.get("messages", [])
                    
                    # 添加Agent特定的系统消息
                    agent_messages = [
                        Message("system", agent_prompt)
                    ]
                    
                    for msg in messages:
                        agent_messages.append(Message(msg["role"], msg["content"]))
                    
                    # 调用LLM
                    response = await agent_llm.chat(agent_messages)
                    
                    # 更新状态
                    new_results = state.get("agent_results", []) + [response.content]
                    
                    return {
                        **state,
                        "agent_results": new_results,
                        "current_agent": state.get("current_agent", 0) + 1
                    }
                
                return agent_node
            
            node_func = create_agent_node(
                llm,
                agent_config["name"],
                agent_config.get("prompt", "You are a helpful assistant.")
            )
            
            workflow.add_node(f"agent_{i}", lambda state, func=node_func: asyncio.run(func(state)))
        
        # 根据协调策略添加边
        if coordination_strategy == "sequential":
            workflow.set_entry_point("agent_0")
            for i in range(len(agents_config) - 1):
                workflow.add_edge(f"agent_{i}", f"agent_{i+1}")
            workflow.add_edge(f"agent_{len(agents_config)-1}", END)
        
        # 编译工作流
        app = workflow.compile()
        
        return app
    
    @staticmethod
    def get_framework_info() -> Dict[str, Any]:
        """获取框架信息"""
        return {
            "name": "LangGraph",
            "description": "基于图的Agent工作流框架，支持复杂的状态管理和条件分支",
            "available": LANGGRAPH_AVAILABLE,
            "strengths": [
                "强大的状态管理能力",
                "支持复杂的工作流设计",
                "可视化图结构",
                "内置检查点和持久化"
            ],
            "weaknesses": [
                "学习曲线较陡峭",
                "相对较新，生态系统不够成熟",
                "调试复杂工作流较困难"
            ],
            "use_cases": [
                "复杂的多步骤工作流",
                "多Agent协作",
                "需要状态管理的应用",
                "条件分支逻辑"
            ],
            "installation": "pip install langgraph"
        }