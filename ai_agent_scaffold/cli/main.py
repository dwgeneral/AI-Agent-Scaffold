"""AI Agent Scaffold CLI主模块。

提供命令行工具的核心功能，包括项目初始化、配置管理、
框架信息查询等功能。
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from ..core import LLMFactory, Config
from ..frameworks import (
    LangChainIntegration,
    LangGraphIntegration,
    CrewAIIntegration,
    LlamaIndexIntegration,
    AutoGenIntegration,
    MetaGPTIntegration,
    PocketFlowIntegration,
)

console = Console()


def create_project_template(project_name: str, project_path: Path) -> None:
    """创建项目模板。
    
    Args:
        project_name: 项目名称
        project_path: 项目路径
    """
    # 创建项目目录结构
    directories = [
        project_path,
        project_path / "src",
        project_path / "tests",
        project_path / "docs",
        project_path / "examples",
        project_path / "config",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    # 创建基础文件
    files = {
        "README.md": f"# {project_name}\n\n使用AI Agent Scaffold构建的AI Agent项目。\n",
        "requirements.txt": "ai-agent-scaffold\n",
        ".env.example": "# 环境变量配置\nZHIPU_API_KEY=your_api_key_here\n",
        "src/__init__.py": "",
        "tests/__init__.py": "",
        "examples/basic_usage.py": '''"""基础使用示例。"""\n\nfrom ai_agent_scaffold import LLMFactory\n\ndef main():\n    """主函数。"""\n    # 创建LLM实例\n    llm = LLMFactory.create_llm("zhipu", model="glm-4")\n    \n    # 发送消息\n    response = llm.chat("你好，世界！")\n    print(response.content)\n\nif __name__ == "__main__":\n    main()\n''',
        "config/config.yaml": '''# AI Agent Scaffold 配置文件\nllm:\n  default_provider: "zhipu"\n  default_model: "glm-4"\n  timeout: 30\n  max_retries: 3\n\nlogging:\n  level: "INFO"\n  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"\n''',
    }
    
    for file_path, content in files.items():
        full_path = project_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
    
    console.print(f"✅ 项目 '{project_name}' 创建成功！", style="green")
    console.print(f"📁 项目路径: {project_path}")
    console.print("\n🚀 下一步:")
    console.print(f"   cd {project_name}")
    console.print("   pip install -r requirements.txt")
    console.print("   cp .env.example .env")
    console.print("   # 编辑 .env 文件添加API密钥")
    console.print("   python examples/basic_usage.py")


def show_providers_info() -> None:
    """显示LLM提供商信息。"""
    factory = LLMFactory()
    providers = factory.list_providers()
    
    if not providers:
        console.print("❌ 没有可用的LLM提供商", style="red")
        return
    
    table = Table(title="🤖 可用的LLM提供商")
    table.add_column("提供商", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("支持的模型", style="yellow")
    table.add_column("描述")
    
    for provider_name in providers:
        try:
            provider_class = factory._providers[provider_name]
            models = ", ".join(provider_class.get_supported_models()[:3])  # 显示前3个模型
            if len(provider_class.get_supported_models()) > 3:
                models += "..."
            
            table.add_row(
                provider_name,
                "✅ 可用",
                models,
                getattr(provider_class, '__doc__', '').split('\n')[0] if provider_class.__doc__ else "无描述"
            )
        except Exception as e:
            table.add_row(
                provider_name,
                f"❌ 错误: {str(e)}",
                "N/A",
                "无法加载"
            )
    
    console.print(table)


def show_frameworks_info() -> None:
    """显示Agent框架信息。"""
    frameworks = [
        LangChainIntegration(),
        LangGraphIntegration(),
        CrewAIIntegration(),
        LlamaIndexIntegration(),
        AutoGenIntegration(),
        MetaGPTIntegration(),
        PocketFlowIntegration(),
    ]
    
    table = Table(title="🔧 可用的Agent框架")
    table.add_column("框架", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("版本")
    table.add_column("描述")
    table.add_column("用例", style="yellow")
    
    for framework in frameworks:
        info = framework.get_framework_info()
        is_available = framework.is_available()
        
        status = "✅ 可用" if is_available else "❌ 未安装"
        version = "已安装" if is_available else "未安装"
        
        table.add_row(
            info["name"],
            status,
            version,
            info["description"][:50] + "..." if len(info["description"]) > 50 else info["description"],
            ", ".join(info["use_cases"][:2])  # 显示前2个用例
        )
    
    console.print(table)


def test_connection(provider: str, model: Optional[str] = None) -> None:
    """测试LLM连接。
    
    Args:
        provider: LLM提供商名称
        model: 模型名称（可选）
    """
    try:
        console.print(f"🔍 测试 {provider} 连接...")
        
        # 创建LLM实例
        llm = LLMFactory.create_llm(provider, model=model)
        
        # 发送测试消息
        response = llm.chat("Hello, this is a test message.")
        
        console.print(f"✅ {provider} 连接成功！", style="green")
        console.print(f"📝 响应: {response.content[:100]}...", style="dim")
        
    except Exception as e:
        console.print(f"❌ {provider} 连接失败: {str(e)}", style="red")
        console.print("💡 请检查:")
        console.print("   - API密钥是否正确")
        console.print("   - 网络连接是否正常")
        console.print("   - 模型名称是否支持")


def show_config() -> None:
    """显示当前配置。"""
    try:
        config = Config.load()
        
        panel_content = []
        
        # LLM配置
        llm_config = config.llm
        panel_content.append(f"🤖 默认LLM提供商: {llm_config.default_provider}")
        panel_content.append(f"📋 默认模型: {llm_config.default_model}")
        panel_content.append(f"⏱️  超时时间: {llm_config.timeout}秒")
        panel_content.append(f"🔄 最大重试次数: {llm_config.max_retries}")
        
        # 环境变量
        panel_content.append("\n🔑 环境变量:")
        env_vars = [
            "ZHIPU_API_KEY",
            "MOONSHOT_API_KEY", 
            "TONGYI_API_KEY",
            "VOLCANO_API_KEY",
        ]
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                masked_value = value[:8] + "*" * (len(value) - 8) if len(value) > 8 else "*" * len(value)
                panel_content.append(f"   {var}: {masked_value}")
            else:
                panel_content.append(f"   {var}: 未设置")
        
        console.print(Panel(
            "\n".join(panel_content),
            title="⚙️ 当前配置",
            border_style="blue"
        ))
        
    except Exception as e:
        console.print(f"❌ 无法加载配置: {str(e)}", style="red")


def main() -> None:
    """CLI主函数。"""
    parser = argparse.ArgumentParser(
        description="AI Agent Scaffold - 统一的AI Agent开发框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  ai-agent-scaffold init my-project          # 创建新项目
  ai-agent-scaffold providers               # 查看可用的LLM提供商
  ai-agent-scaffold frameworks              # 查看可用的Agent框架
  ai-agent-scaffold test zhipu              # 测试智谱AI连接
  ai-agent-scaffold config                  # 查看当前配置

更多信息请访问: https://github.com/ai-agent-scaffold/ai-agent-scaffold
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # init命令
    init_parser = subparsers.add_parser("init", help="创建新的AI Agent项目")
    init_parser.add_argument("project_name", help="项目名称")
    init_parser.add_argument(
        "--path", 
        type=Path, 
        default=None,
        help="项目路径（默认为当前目录下的项目名称）"
    )
    
    # providers命令
    subparsers.add_parser("providers", help="显示可用的LLM提供商")
    
    # frameworks命令
    subparsers.add_parser("frameworks", help="显示可用的Agent框架")
    
    # test命令
    test_parser = subparsers.add_parser("test", help="测试LLM连接")
    test_parser.add_argument("provider", help="LLM提供商名称")
    test_parser.add_argument("--model", help="模型名称（可选）")
    
    # config命令
    subparsers.add_parser("config", help="显示当前配置")
    
    # version命令
    subparsers.add_parser("version", help="显示版本信息")
    
    args = parser.parse_args()
    
    # 显示欢迎信息
    if args.command != "version":
        console.print(Panel(
            Text("AI Agent Scaffold", style="bold blue") + 
            Text("\n统一的AI Agent开发框架", style="dim"),
            border_style="blue"
        ))
    
    try:
        if args.command == "init":
            project_path = args.path or Path.cwd() / args.project_name
            create_project_template(args.project_name, project_path)
            
        elif args.command == "providers":
            show_providers_info()
            
        elif args.command == "frameworks":
            show_frameworks_info()
            
        elif args.command == "test":
            test_connection(args.provider, args.model)
            
        elif args.command == "config":
            show_config()
            
        elif args.command == "version":
            from .. import __version__
            console.print(f"AI Agent Scaffold v{__version__}")
            
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        console.print("\n👋 操作已取消", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"❌ 发生错误: {str(e)}", style="red")
        console.print("💡 如需帮助，请访问: https://github.com/ai-agent-scaffold/ai-agent-scaffold/issues")
        sys.exit(1)


if __name__ == "__main__":
    main()