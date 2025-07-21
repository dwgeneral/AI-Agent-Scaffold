"""AI Agent Scaffold SDK setup configuration"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 核心依赖
core_requirements = [
    "pydantic>=2.0.0",
    "httpx>=0.24.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
    "typing-extensions>=4.0.0",
]

# 可选依赖 - LLM厂商
llm_requirements = {
    "zhipu": ["zhipuai>=1.0.0"],
    "moonshot": ["openai>=1.0.0"],  # Moonshot使用OpenAI兼容接口
    "tongyi": ["dashscope>=1.0.0"],
    "volcano": ["volcengine>=1.0.0"],
}

# 可选依赖 - Agent框架
framework_requirements = {
    "langchain": [
        "langchain>=0.1.0",
        "langchain-core>=0.1.0",
        "langchain-community>=0.0.10"
    ],
    "langgraph": [
        "langgraph>=0.0.30",
        "langchain>=0.1.0"
    ],
    "crewai": ["crewai>=0.1.0"],
    "llamaindex": [
        "llama-index>=0.9.0",
        "llama-index-core>=0.9.0"
    ],
    "autogen": ["pyautogen>=0.2.0"],
    "metagpt": ["metagpt>=0.6.0"],
    "pocketflow": [],  # 示例框架，暂无实际依赖
}

# 开发依赖
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.2.0",
]

# 所有LLM厂商依赖
all_llm_requirements = []
for deps in llm_requirements.values():
    all_llm_requirements.extend(deps)

# 所有框架依赖
all_framework_requirements = []
for deps in framework_requirements.values():
    all_framework_requirements.extend(deps)

# 完整依赖（除了开发依赖）
all_requirements = core_requirements + all_llm_requirements + all_framework_requirements

setup(
    name="ai-agent-scaffold",
    version="0.1.0",
    author="AI Agent Scaffold Team",
    author_email="contact@ai-agent-scaffold.com",
    description="A comprehensive Python SDK for integrating LLM providers and Agent frameworks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ai-agent-scaffold/ai-agent-scaffold",
    project_urls={
        "Bug Tracker": "https://github.com/ai-agent-scaffold/ai-agent-scaffold/issues",
        "Documentation": "https://ai-agent-scaffold.readthedocs.io/",
        "Source Code": "https://github.com/ai-agent-scaffold/ai-agent-scaffold",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=core_requirements,
    extras_require={
        # LLM厂商
        **llm_requirements,
        "all-llm": all_llm_requirements,
        
        # Agent框架
        **framework_requirements,
        "all-frameworks": all_framework_requirements,
        
        # 组合安装
        "all": all_requirements,
        "dev": dev_requirements,
        "full": all_requirements + dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "ai-agent-scaffold=ai_agent_scaffold.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_agent_scaffold": [
            "templates/*.yaml",
            "templates/*.json",
            "examples/*.py",
        ],
    },
    keywords=[
        "ai", "agent", "llm", "langchain", "langgraph", "crewai", 
        "llamaindex", "autogen", "metagpt", "scaffold", "framework"
    ],
    zip_safe=False,
)