# 云效自动化测试项目

这是一个基于 Selenium 的自动化测试项目，用于云效平台的测试用例管理自动化。

## 功能特性

- 自动化测试用例标记
  - 批量标记测试用例的自动化类型
  - 标记测试用例的执行结果
  - 设置测试执行人
- 测试计划管理
  - 导出测试计划用例
  - 用例挑选
- 多产品线支持
  - BIOS
  - BMC
  - 昆仑卫士
  - 机房管理系统

## 安装

1. 克隆项目
```bash
git clone [项目地址]
cd [项目目录]
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 配置

1. 在 `src/config/yx_config.py` 中配置：
   - 云效平台登录凭据
   - 产品类型
   - 测试计划名称
   - 文件导出配置

## 使用方法

1. 基本使用
```bash
python -m src.core.automation
```

2. 运行测试
```bash
pytest
```

## 项目结构

```
.
├── src/                    # 源代码
│   ├── config/            # 配置文件
│   ├── core/              # 核心功能
│   └── utils/             # 工具函数
├── tests/                 # 测试代码
├── docs/                  # 文档
├── data/                  # 测试数据
└── output/                # 输出结果
```

## 开发指南

- 遵循 PEP 8 编码规范
- 所有新功能都需要编写单元测试
- 提交代码前运行所有测试确保通过

## 测试覆盖率

使用 pytest-cov 生成测试覆盖率报告：
```bash
pytest --cov=src tests/
```

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[许可证类型] 