"""智能客服系统示例

本示例展示如何使用AI Agent Scaffold SDK构建一个完整的智能客服系统，
集成多个LLM提供商和Agent框架，实现智能问答、情感分析、工单处理等功能。
"""

import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from ai_agent_scaffold import (
    LLMFactory, 
    UserMessage, 
    SystemMessage, 
    AssistantMessage
)
from ai_agent_scaffold.frameworks import (
    LangChainIntegration,
    CrewAIIntegration
)


class TicketPriority(Enum):
    """工单优先级"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    URGENT = "紧急"


class TicketStatus(Enum):
    """工单状态"""
    OPEN = "待处理"
    IN_PROGRESS = "处理中"
    RESOLVED = "已解决"
    CLOSED = "已关闭"


@dataclass
class CustomerTicket:
    """客服工单"""
    id: str
    customer_id: str
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    category: str
    created_at: datetime
    updated_at: datetime
    assigned_agent: Optional[str] = None
    resolution: Optional[str] = None


class SentimentAnalyzer:
    """情感分析器"""
    
    def __init__(self, llm_provider: str = "zhipu", **llm_kwargs):
        self.llm = LLMFactory.create(provider=llm_provider, **llm_kwargs)
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """分析文本情感"""
        messages = [
            SystemMessage(content="""
你是一个专业的情感分析专家。请分析用户输入文本的情感倾向。

请返回JSON格式的结果，包含以下字段：
- sentiment: 情感倾向（positive/negative/neutral）
- confidence: 置信度（0-1之间的浮点数）
- emotions: 具体情感列表（如：愤怒、满意、困惑等）
- urgency: 紧急程度（low/medium/high/urgent）

只返回JSON，不要其他内容。
            """),
            UserMessage(content=f"请分析以下文本的情感：\n\n{text}")
        ]
        
        try:
            response = await self.llm.astream(messages).__anext__()
            # 这里简化处理，实际应该累积所有流式响应
            result = json.loads(response.content)
            return result
        except Exception as e:
            # 降级处理
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "emotions": ["未知"],
                "urgency": "medium"
            }


class IntentClassifier:
    """意图分类器"""
    
    def __init__(self, llm_provider: str = "zhipu", **llm_kwargs):
        self.llm = LLMFactory.create(provider=llm_provider, **llm_kwargs)
    
    async def classify_intent(self, text: str) -> Dict[str, Any]:
        """分类用户意图"""
        messages = [
            SystemMessage(content="""
你是一个客服意图分类专家。请分析用户输入的意图类别。

支持的意图类别：
- product_inquiry: 产品咨询
- technical_support: 技术支持
- billing_issue: 账单问题
- complaint: 投诉
- refund_request: 退款申请
- account_issue: 账户问题
- general_question: 一般问题
- praise: 表扬

请返回JSON格式：
{
  "intent": "意图类别",
  "confidence": 置信度,
  "keywords": ["关键词列表"],
  "suggested_category": "建议的工单分类"
}

只返回JSON，不要其他内容。
            """),
            UserMessage(content=f"请分析以下用户输入的意图：\n\n{text}")
        ]
        
        try:
            response = await self.llm.astream(messages).__anext__()
            result = json.loads(response.content)
            return result
        except Exception as e:
            return {
                "intent": "general_question",
                "confidence": 0.5,
                "keywords": [],
                "suggested_category": "一般咨询"
            }


class KnowledgeBase:
    """知识库"""
    
    def __init__(self):
        # 简化的知识库，实际应该连接真实的知识库系统
        self.knowledge = {
            "product_inquiry": {
                "常见问题": "我们的产品支持多种功能，包括...",
                "价格信息": "产品价格根据套餐不同，基础版...",
                "功能特性": "主要功能包括数据分析、报表生成..."
            },
            "technical_support": {
                "登录问题": "如果无法登录，请检查用户名密码...",
                "系统错误": "遇到系统错误时，请尝试刷新页面...",
                "性能问题": "系统运行缓慢可能是由于..."
            },
            "billing_issue": {
                "账单查询": "您可以在账户设置中查看详细账单...",
                "付款问题": "支持多种付款方式，包括...",
                "发票申请": "发票申请请联系财务部门..."
            }
        }
    
    def search(self, intent: str, keywords: List[str]) -> List[str]:
        """搜索相关知识"""
        if intent in self.knowledge:
            relevant_info = []
            for key, value in self.knowledge[intent].items():
                if any(keyword in key or keyword in value for keyword in keywords):
                    relevant_info.append(f"{key}: {value}")
            return relevant_info
        return []


class CustomerServiceAgent:
    """客服Agent"""
    
    def __init__(self, llm_provider: str = "zhipu", **llm_kwargs):
        self.llm = LLMFactory.create(provider=llm_provider, **llm_kwargs)
        self.sentiment_analyzer = SentimentAnalyzer(llm_provider, **llm_kwargs)
        self.intent_classifier = IntentClassifier(llm_provider, **llm_kwargs)
        self.knowledge_base = KnowledgeBase()
        self.conversation_history = []
    
    async def process_customer_message(self, message: str, customer_id: str) -> Dict[str, Any]:
        """处理客户消息"""
        # 1. 情感分析
        sentiment = await self.sentiment_analyzer.analyze_sentiment(message)
        
        # 2. 意图分类
        intent = await self.intent_classifier.classify_intent(message)
        
        # 3. 知识库搜索
        knowledge = self.knowledge_base.search(
            intent["intent"], 
            intent["keywords"]
        )
        
        # 4. 生成回复
        response = await self._generate_response(
            message, sentiment, intent, knowledge
        )
        
        # 5. 判断是否需要创建工单
        needs_ticket = self._should_create_ticket(sentiment, intent)
        
        result = {
            "customer_id": customer_id,
            "message": message,
            "sentiment": sentiment,
            "intent": intent,
            "knowledge": knowledge,
            "response": response,
            "needs_ticket": needs_ticket,
            "timestamp": datetime.now().isoformat()
        }
        
        # 更新对话历史
        self.conversation_history.append(result)
        
        return result
    
    async def _generate_response(self, message: str, sentiment: Dict, intent: Dict, knowledge: List[str]) -> str:
        """生成回复"""
        # 构建上下文
        context = f"""
用户情感：{sentiment['sentiment']} (置信度: {sentiment['confidence']})
用户意图：{intent['intent']}
相关知识：{'; '.join(knowledge) if knowledge else '无相关知识'}
        """
        
        # 根据情感调整回复风格
        if sentiment['sentiment'] == 'negative':
            style_instruction = "请用同理心和耐心的语气回复，优先解决用户的问题和担忧。"
        elif sentiment['sentiment'] == 'positive':
            style_instruction = "请用友好和积极的语气回复，保持用户的良好体验。"
        else:
            style_instruction = "请用专业和友好的语气回复。"
        
        messages = [
            SystemMessage(content=f"""
你是一个专业的客服代表。请根据以下信息为用户提供帮助：

{context}

回复要求：
1. {style_instruction}
2. 如果有相关知识，请基于知识库信息回答
3. 如果没有相关知识，请诚实说明并提供替代方案
4. 保持回复简洁明了，不超过200字
5. 如果问题复杂，建议用户联系专门的技术支持
            """),
            UserMessage(content=message)
        ]
        
        try:
            response = await self.llm.astream(messages).__anext__()
            return response.content
        except Exception as e:
            return "抱歉，我现在无法处理您的请求。请稍后再试或联系人工客服。"
    
    def _should_create_ticket(self, sentiment: Dict, intent: Dict) -> bool:
        """判断是否需要创建工单"""
        # 负面情感且置信度高
        if sentiment['sentiment'] == 'negative' and sentiment['confidence'] > 0.7:
            return True
        
        # 紧急程度高
        if sentiment['urgency'] in ['high', 'urgent']:
            return True
        
        # 特定意图类型
        if intent['intent'] in ['complaint', 'refund_request', 'technical_support']:
            return True
        
        return False


class TicketManager:
    """工单管理器"""
    
    def __init__(self):
        self.tickets = {}
        self.ticket_counter = 1
    
    def create_ticket(
        self, 
        customer_id: str, 
        title: str, 
        description: str, 
        intent: Dict, 
        sentiment: Dict
    ) -> CustomerTicket:
        """创建工单"""
        ticket_id = f"T{self.ticket_counter:06d}"
        self.ticket_counter += 1
        
        # 根据情感和意图确定优先级
        if sentiment['urgency'] == 'urgent':
            priority = TicketPriority.URGENT
        elif sentiment['urgency'] == 'high':
            priority = TicketPriority.HIGH
        elif sentiment['sentiment'] == 'negative':
            priority = TicketPriority.MEDIUM
        else:
            priority = TicketPriority.LOW
        
        ticket = CustomerTicket(
            id=ticket_id,
            customer_id=customer_id,
            title=title,
            description=description,
            priority=priority,
            status=TicketStatus.OPEN,
            category=intent.get('suggested_category', '一般咨询'),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.tickets[ticket_id] = ticket
        return ticket
    
    def get_ticket(self, ticket_id: str) -> Optional[CustomerTicket]:
        """获取工单"""
        return self.tickets.get(ticket_id)
    
    def update_ticket_status(self, ticket_id: str, status: TicketStatus, resolution: str = None):
        """更新工单状态"""
        if ticket_id in self.tickets:
            self.tickets[ticket_id].status = status
            self.tickets[ticket_id].updated_at = datetime.now()
            if resolution:
                self.tickets[ticket_id].resolution = resolution


class IntelligentCustomerService:
    """智能客服系统"""
    
    def __init__(self, llm_provider: str = "zhipu", **llm_kwargs):
        self.agent = CustomerServiceAgent(llm_provider, **llm_kwargs)
        self.ticket_manager = TicketManager()
    
    async def handle_customer_inquiry(self, customer_id: str, message: str) -> Dict[str, Any]:
        """处理客户咨询"""
        print(f"\n🔄 处理客户 {customer_id} 的咨询...")
        
        # 处理消息
        result = await self.agent.process_customer_message(message, customer_id)
        
        # 如果需要创建工单
        ticket = None
        if result['needs_ticket']:
            ticket = self.ticket_manager.create_ticket(
                customer_id=customer_id,
                title=f"客户咨询 - {result['intent']['intent']}",
                description=message,
                intent=result['intent'],
                sentiment=result['sentiment']
            )
            print(f"📋 已创建工单: {ticket.id} (优先级: {ticket.priority.value})")
        
        return {
            **result,
            "ticket": ticket
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        total_tickets = len(self.ticket_manager.tickets)
        open_tickets = sum(1 for t in self.ticket_manager.tickets.values() 
                          if t.status == TicketStatus.OPEN)
        
        return {
            "total_conversations": len(self.agent.conversation_history),
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "ticket_creation_rate": total_tickets / max(len(self.agent.conversation_history), 1)
        }


async def demo_customer_service():
    """演示智能客服系统"""
    print("🤖 智能客服系统演示")
    print("=" * 50)
    
    # 检查API密钥
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        print("❌ 请设置 ZHIPU_API_KEY 环境变量")
        return
    
    # 初始化客服系统
    customer_service = IntelligentCustomerService(
        llm_provider="zhipu",
        api_key=api_key,
        model="glm-4"
    )
    
    # 模拟客户咨询场景
    test_scenarios = [
        {
            "customer_id": "CUST001",
            "message": "你好，我想了解一下你们产品的价格和功能特性。",
            "description": "正面咨询"
        },
        {
            "customer_id": "CUST002",
            "message": "我的账户无法登录，试了很多次都不行，很着急！",
            "description": "技术问题 + 负面情感"
        },
        {
            "customer_id": "CUST003",
            "message": "你们的系统太慢了，我要投诉！这个月已经出现好几次问题了，我要求退款！",
            "description": "投诉 + 强烈负面情感"
        },
        {
            "customer_id": "CUST004",
            "message": "请问如何申请发票？我需要报销。",
            "description": "账单问题"
        }
    ]
    
    # 处理各种场景
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📞 场景 {i}: {scenario['description']}")
        print(f"👤 客户 {scenario['customer_id']}: {scenario['message']}")
        
        try:
            result = await customer_service.handle_customer_inquiry(
                scenario['customer_id'], 
                scenario['message']
            )
            
            print(f"🤖 客服回复: {result['response']}")
            print(f"😊 情感分析: {result['sentiment']['sentiment']} (置信度: {result['sentiment']['confidence']:.2f})")
            print(f"🎯 意图识别: {result['intent']['intent']}")
            
            if result['ticket']:
                ticket = result['ticket']
                print(f"📋 工单信息: {ticket.id} | {ticket.priority.value} | {ticket.category}")
            else:
                print("📋 无需创建工单")
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
        
        print("-" * 50)
    
    # 显示系统统计
    stats = customer_service.get_system_stats()
    print(f"\n📊 系统统计:")
    print(f"   总对话数: {stats['total_conversations']}")
    print(f"   总工单数: {stats['total_tickets']}")
    print(f"   待处理工单: {stats['open_tickets']}")
    print(f"   工单创建率: {stats['ticket_creation_rate']:.2%}")


def main():
    """主函数"""
    print("AI Agent Scaffold SDK - 智能客服系统示例")
    print("=" * 60)
    
    try:
        asyncio.run(demo_customer_service())
    except KeyboardInterrupt:
        print("\n演示被用户中断")
    except Exception as e:
        print(f"\n演示运行出错: {e}")
    
    print("\n🎉 智能客服系统演示完成！")
    print("\n💡 这个示例展示了如何使用 AI Agent Scaffold SDK 构建复杂的AI应用：")
    print("   ✅ 多LLM提供商集成")
    print("   ✅ 情感分析和意图识别")
    print("   ✅ 知识库集成")
    print("   ✅ 智能工单管理")
    print("   ✅ 完整的业务流程")


if __name__ == "__main__":
    main()