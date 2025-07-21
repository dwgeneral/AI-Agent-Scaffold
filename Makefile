# AI Agent Scaffold Makefile
# 简化常用开发任务的执行

.PHONY: help install install-dev install-all clean test test-unit test-integration lint format type-check security docs build publish pre-commit setup-dev

# 默认目标
help:
	@echo "AI Agent Scaffold 开发工具"
	@echo ""
	@echo "可用命令:"
	@echo "  install        - 安装基础依赖"
	@echo "  install-dev    - 安装开发依赖"
	@echo "  install-all    - 安装所有依赖（包括所有LLM和框架）"
	@echo "  setup-dev      - 设置开发环境（推荐首次使用）"
	@echo ""
	@echo "  test           - 运行所有测试"
	@echo "  test-unit      - 运行单元测试"
	@echo "  test-integration - 运行集成测试"
	@echo "  test-coverage  - 运行测试并生成覆盖率报告"
	@echo ""
	@echo "  lint           - 代码风格检查"
	@echo "  format         - 代码格式化"
	@echo "  type-check     - 类型检查"
	@echo "  security       - 安全检查"
	@echo "  pre-commit     - 运行pre-commit检查"
	@echo ""
	@echo "  docs           - 构建文档"
	@echo "  docs-serve     - 启动文档服务器"
	@echo ""
	@echo "  build          - 构建包"
	@echo "  publish        - 发布到PyPI"
	@echo "  publish-test   - 发布到TestPyPI"
	@echo ""
	@echo "  clean          - 清理临时文件"
	@echo "  clean-all      - 深度清理"

# 安装依赖
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-all:
	pip install -e ".[full]"

# 开发环境设置
setup-dev: install-dev
	@echo "设置开发环境..."
	pre-commit install
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "已创建 .env 文件，请填入您的API密钥"; \
	fi
	@echo "开发环境设置完成！"
	@echo "请编辑 .env 文件添加您的API密钥"

# 测试
test:
	pytest tests/ -v

test-unit:
	pytest tests/ -v -m "not integration"

test-integration:
	pytest tests/ -v -m "integration"

test-coverage:
	pytest tests/ -v --cov=ai_agent_scaffold --cov-report=html --cov-report=term-missing
	@echo "覆盖率报告已生成: htmlcov/index.html"

test-watch:
	pytest-watch tests/ -- -v

# 代码质量
lint:
	@echo "运行代码风格检查..."
	flake8 ai_agent_scaffold/ tests/ examples/
	@echo "运行文档字符串检查..."
	pydocstyle ai_agent_scaffold/ --convention=google

format:
	@echo "格式化代码..."
	black ai_agent_scaffold/ tests/ examples/
	isort ai_agent_scaffold/ tests/ examples/
	@echo "代码格式化完成"

type-check:
	@echo "运行类型检查..."
	mypy ai_agent_scaffold/

security:
	@echo "运行安全检查..."
	bandit -r ai_agent_scaffold/ -f json -o bandit-report.json
	safety check --json --output safety-report.json
	@echo "安全检查完成，报告已生成"

pre-commit:
	pre-commit run --all-files

# 文档
docs:
	@echo "构建文档..."
	cd docs && make html
	@echo "文档已构建: docs/_build/html/index.html"

docs-serve:
	@echo "启动文档服务器..."
	cd docs/_build/html && python -m http.server 8000

docs-clean:
	cd docs && make clean

# 构建和发布
build: clean
	@echo "构建包..."
	python -m build
	@echo "包构建完成: dist/"

check-build:
	twine check dist/*

publish-test: build check-build
	@echo "发布到TestPyPI..."
	twine upload --repository testpypi dist/*

publish: build check-build
	@echo "发布到PyPI..."
	twine upload dist/*

# 清理
clean:
	@echo "清理临时文件..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "清理完成"

clean-all: clean
	@echo "深度清理..."
	rm -rf .tox/
	rm -rf .nox/
	rm -rf .cache/
	rm -rf bandit-report.json
	rm -rf safety-report.json
	rm -rf docs/_build/
	@echo "深度清理完成"

# 开发工具
notebook:
	@echo "启动Jupyter Notebook..."
	jupyter notebook examples/

shell:
	@echo "启动Python交互式环境..."
	python -c "import ai_agent_scaffold; print('AI Agent Scaffold已加载'); print('版本:', ai_agent_scaffold.__version__)"
	ipython

# 性能分析
profile:
	@echo "运行性能分析..."
	python -m cProfile -o profile.stats examples/basic_llm_usage.py
	python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"

# 依赖管理
update-deps:
	@echo "更新依赖..."
	pip-compile requirements.in
	pip-compile requirements-dev.in

check-deps:
	@echo "检查依赖安全性..."
	safety check
	pip-audit

# 版本管理
bump-patch:
	bump2version patch

bump-minor:
	bump2version minor

bump-major:
	bump2version major

# 示例运行
run-examples:
	@echo "运行基础示例..."
	python examples/basic_llm_usage.py
	@echo "运行框架示例..."
	python examples/agent_frameworks_demo.py
	@echo "运行客服示例..."
	python examples/intelligent_customer_service.py

# Docker相关（如果需要）
docker-build:
	docker build -t ai-agent-scaffold .

docker-run:
	docker run -it --rm ai-agent-scaffold

# 统计信息
stats:
	@echo "项目统计信息:"
	@echo "代码行数:"
	find ai_agent_scaffold/ -name "*.py" | xargs wc -l | tail -1
	@echo "测试行数:"
	find tests/ -name "*.py" | xargs wc -l | tail -1
	@echo "示例行数:"
	find examples/ -name "*.py" | xargs wc -l | tail -1
	@echo "文件数量:"
	find ai_agent_scaffold/ -name "*.py" | wc -l