# 贡献指南

感谢您对AI Agent Scaffold项目的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ✨ 添加新功能
- 🧪 编写测试
- 🎨 改进用户体验

## 开始之前

### 行为准则

参与本项目即表示您同意遵守我们的[行为准则](CODE_OF_CONDUCT.md)。我们致力于为所有人提供友好、安全和包容的环境。

### 许可证

通过向本项目贡献代码，您同意您的贡献将在[MIT许可证](LICENSE)下发布。

## 如何贡献

### 报告问题

如果您发现了bug或有功能建议，请：

1. 首先搜索[现有issues](https://github.com/ai-agent-scaffold/ai-agent-scaffold/issues)，确保问题尚未被报告
2. 如果是新问题，请创建一个新的issue
3. 使用清晰、描述性的标题
4. 提供详细的问题描述，包括：
   - 重现步骤
   - 期望行为
   - 实际行为
   - 环境信息（Python版本、操作系统等）
   - 相关的错误日志或截图

### 提交代码

#### 开发环境设置

1. **Fork项目**
   ```bash
   # 在GitHub上fork项目，然后克隆到本地
   git clone https://github.com/YOUR_USERNAME/ai-agent-scaffold.git
   cd ai-agent-scaffold
   ```

2. **设置开发环境**
   ```bash
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   
   # 安装开发依赖
   make setup-dev
   # 或手动安装
   pip install -e ".[dev]"
   ```

3. **配置环境变量**
   ```bash
   # 复制环境变量模板
   cp .env.example .env
   # 编辑.env文件，添加必要的API密钥（用于测试）
   ```

4. **验证环境**
   ```bash
   # 运行测试确保环境正常
   make test-unit
   ```

#### 开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

2. **编写代码**
   - 遵循项目的代码风格和约定
   - 为新功能编写测试
   - 更新相关文档
   - 确保代码通过所有检查

3. **代码质量检查**
   ```bash
   # 格式化代码
   make format
   
   # 运行代码检查
   make lint
   
   # 类型检查
   make type-check
   
   # 运行测试
   make test
   
   # 运行所有pre-commit检查
   make pre-commit
   ```

4. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **推送并创建PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   然后在GitHub上创建Pull Request。

#### 提交消息规范

我们使用[Conventional Commits](https://www.conventionalcommits.org/)规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**类型（type）**：
- `feat`: 新功能
- `fix`: bug修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动
- `perf`: 性能优化
- `ci`: CI/CD相关

**示例**：
```
feat(adapters): add support for Claude API

fix(core): resolve memory leak in LLM factory

docs: update installation guide for Windows

test(frameworks): add integration tests for LangChain
```

## 代码规范

### Python代码风格

我们遵循以下代码规范：

- **PEP 8**: Python代码风格指南
- **Black**: 代码格式化（行长度88字符）
- **isort**: import语句排序
- **Google风格**: 文档字符串格式

### 文档字符串

使用Google风格的文档字符串：

```python
def example_function(param1: str, param2: int) -> bool:
    """示例函数的简短描述。
    
    更详细的描述可以写在这里，解释函数的用途、
    算法或其他重要信息。
    
    Args:
        param1: 第一个参数的描述。
        param2: 第二个参数的描述。
        
    Returns:
        返回值的描述。
        
    Raises:
        ValueError: 当参数无效时抛出。
        
    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

### 类型注解

所有公共API都应该有完整的类型注解：

```python
from typing import List, Optional, Dict, Any

def process_messages(
    messages: List[Message], 
    config: Optional[Dict[str, Any]] = None
) -> LLMResponse:
    """处理消息列表。"""
    pass
```

### 错误处理

- 使用项目定义的异常类
- 提供有意义的错误消息
- 包含错误处理建议

```python
from ai_agent_scaffold.core.exceptions import LLMError

def api_call():
    try:
        # API调用
        pass
    except Exception as e:
        raise LLMError(
            f"API调用失败: {str(e)}",
            suggestion="请检查API密钥是否正确"
        ) from e
```

## 测试指南

### 测试类型

1. **单元测试**: 测试单个函数或类
2. **集成测试**: 测试组件间的交互
3. **端到端测试**: 测试完整的用户场景

### 测试结构

```
tests/
├── unit/           # 单元测试
│   ├── test_core.py
│   ├── test_adapters.py
│   └── test_frameworks.py
├── integration/    # 集成测试
│   ├── test_llm_integration.py
│   └── test_framework_integration.py
├── e2e/           # 端到端测试
│   └── test_scenarios.py
└── fixtures/      # 测试数据
    └── sample_data.py
```

### 编写测试

```python
import pytest
from ai_agent_scaffold.core import Message, LLMFactory

class TestMessage:
    """Message类的测试。"""
    
    def test_create_text_message(self):
        """测试创建文本消息。"""
        message = Message.text("Hello, world!")
        assert message.content == "Hello, world!"
        assert message.type == "text"
    
    def test_message_serialization(self):
        """测试消息序列化。"""
        message = Message.text("Test")
        data = message.to_dict()
        assert data["content"] == "Test"
        assert data["type"] == "text"
    
    @pytest.mark.asyncio
    async def test_async_operation(self):
        """测试异步操作。"""
        # 异步测试示例
        pass
```

### 运行测试

```bash
# 运行所有测试
make test

# 运行单元测试
make test-unit

# 运行集成测试（需要API密钥）
make test-integration

# 生成覆盖率报告
make test-coverage

# 监视模式（自动重新运行）
make test-watch
```

## 文档贡献

### 文档类型

1. **API文档**: 自动从代码生成
2. **用户指南**: 使用教程和示例
3. **开发者文档**: 架构和设计文档
4. **README**: 项目介绍和快速开始

### 文档格式

- 使用Markdown格式
- 遵循[中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)
- 提供英文和中文版本（如适用）

### 构建文档

```bash
# 构建HTML文档
make docs

# 启动文档服务器
make docs-serve

# 清理文档
make docs-clean
```

## 发布流程

### 版本管理

我们使用[语义化版本](https://semver.org/)：

- `MAJOR.MINOR.PATCH`
- 主版本：不兼容的API更改
- 次版本：向后兼容的新功能
- 修订版本：向后兼容的bug修复

### 发布步骤

1. **更新版本号**
   ```bash
   # 补丁版本
   make bump-patch
   
   # 次版本
   make bump-minor
   
   # 主版本
   make bump-major
   ```

2. **更新CHANGELOG**
   - 记录所有重要变更
   - 按类型分组（Added, Changed, Fixed等）

3. **创建发布PR**
   - 包含版本更新和CHANGELOG
   - 通过所有检查后合并

4. **创建GitHub Release**
   - 标记版本
   - 自动触发PyPI发布

## 社区

### 沟通渠道

- **GitHub Issues**: 问题报告和功能请求
- **GitHub Discussions**: 一般讨论和问答
- **Email**: contact@ai-agent-scaffold.com

### 获得帮助

如果您在贡献过程中遇到问题：

1. 查看现有的issues和discussions
2. 阅读项目文档
3. 在GitHub上创建新的discussion
4. 发送邮件给维护者

### 认可贡献者

我们会在以下地方认可贡献者：

- README.md的贡献者列表
- 发布说明中的感谢
- GitHub的贡献者图表

## 常见问题

### Q: 我应该从哪里开始？
A: 查看标记为"good first issue"的issues，这些通常适合新贡献者。

### Q: 我的PR需要多长时间才能被审查？
A: 我们努力在一周内审查所有PR。复杂的PR可能需要更长时间。

### Q: 我可以添加新的LLM提供商吗？
A: 当然可以！请先创建一个issue讨论实现方案。

### Q: 如何报告安全漏洞？
A: 请发送邮件到security@ai-agent-scaffold.com，不要在公开的issue中报告。

---

再次感谢您的贡献！每一个贡献都让这个项目变得更好。🚀