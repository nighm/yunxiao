# 贡献指南

感谢您考虑为云效自动化测试项目做出贡献！

## 开发流程

1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 开发环境设置

1. 克隆项目
```bash
git clone [your-fork-url]
cd yunxiao-automation
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -e .[dev]
```

## 代码规范

- 遵循 PEP 8 编码规范
- 使用 black 进行代码格式化
- 使用 flake8 进行代码检查
- 使用 mypy 进行类型检查

## 提交规范

提交信息应该清晰描述更改内容，建议使用以下格式：

- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- style: 代码格式（不影响代码运行的变动）
- refactor: 重构（既不是新增功能，也不是修改bug的代码变动）
- test: 增加测试
- chore: 构建过程或辅助工具的变动

示例：
```
feat: 添加自动化用例批量导入功能
```

## 测试

- 所有新功能都需要编写单元测试
- 所有修复都需要包含相关的测试用例
- 提交前运行所有测试确保通过

```bash
# 运行所有测试
make test

# 运行单元测试
pytest -m unit

# 运行集成测试
pytest -m integration

# 生成覆盖率报告
make coverage
```

## Pull Request 流程

1. 确保本地测试通过
2. 更新相关文档
3. 创建 Pull Request 并描述更改内容
4. 等待 CI 检查通过
5. 等待代码审查
6. 根据反馈进行修改
7. 合并到主分支

## 问题反馈

如果您发现任何问题或有改进建议，请：

1. 检查是否已存在相关的 Issue
2. 创建新的 Issue 并详细描述问题
3. 包含重现步骤和预期行为
4. 如果可能，提供错误日志或截图

## 行为准则

- 尊重所有贡献者
- 保持专业和友善的交流
- 接受建设性的批评和建议
- 关注问题本身而不是个人

## 许可证

通过贡献代码，您同意您的贡献将采用与项目相同的 MIT 许可证。 