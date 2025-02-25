"""代码质量检查工具包

这个包提供了一个简单但功能强大的代码质量检查工具，专注于项目自身代码的质量检查。
主要功能包括：
1. 文件结构检查
2. 代码复杂度检查
3. 命名规范检查
4. 文档完整性检查
5. 代码行数统计
6. Git变更文件检查

使用示例:
    >>> from code_quality_checker import CodeQualityChecker
    >>> checker = CodeQualityChecker("path/to/project")
    >>> report = checker.generate_report(changed_only=True)
    >>> print(report)
"""

from .checker import CodeQualityChecker

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com" 