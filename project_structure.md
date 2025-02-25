# 云效自动化测试项目结构规划

## 目录结构

```
yunxiao/
├── src/                      # 源代码目录
│   ├── core/                 # 核心功能模块
│   │   ├── login/            # 登录相关
│   │   ├── test_case/        # 测试用例管理
│   │   └── automation/       # 自动化测试核心
│   ├── utils/                # 工具类
│   │   ├── driver/           # 浏览器驱动管理
│   │   └── helpers/          # 辅助函数
│   └── config/               # 配置管理
├── tests/                    # 测试目录
├── logs/                     # 日志目录
├── data/                     # 测试数据
└── docs/                     # 文档
```

## 模块说明

### 1. core 核心模块

#### 1.1 login
- 统一登录功能实现
- 验证码/滑块处理

#### 1.2 test_case
- 测试用例管理
- 用例导入导出
- 用例标记

#### 1.3 automation
- 自动化测试执行
- 结果管理

### 2. utils 工具模块

#### 2.1 driver
- WebDriver 管理
- 浏览器配置

#### 2.2 helpers
- 通用工具函数
- 日志处理

### 3. config 配置模块
- 环境配置
- 用户配置
- URL配置

## 代码合并方案

1. 合并重复的登录实现
   - 合并 T_5.py、T_5_p.py 中的登录功能
   - 整合到 src/core/login 模块

2. 合并自动化测试功能
   - 合并 automaticLabeling.py 和 automaticLabeling_self.py
   - 重构到 src/core/automation 模块

3. 统一配置管理
   - 重构 yxConfig.py
   - 迁移到 src/config 模块

4. 删除冗余文件
   - 删除重复的测试文件（T_1.py ~ T_4.py）
   - 删除未使用的临时文件

## 优化建议

1. 统一代码风格和命名规范
2. 添加异常处理和日志记录
3. 引入配置文件管理
4. 添加单元测试
5. 完善文档说明