"""文档规范策略模块

这个模块定义了不同类型的文档规范检查策略，包括模块级文档、类文档和函数文档的检查。
每个策略都实现了统一的接口，使用ast模块来分析和验证文档字符串的存在性。
"""

import ast
from dataclasses import dataclass
from typing import List

@dataclass
class DocumentationResult:
    """文档分析结果
    
    用于存储文档检查的结果，包括文档覆盖率和缺失文档的列表。
    
    Attributes:
        coverage: 文档覆盖率，范围0-1
        missing_docs: 缺失文档的项目列表，每个元素是一个描述字符串
    """
    coverage: float
    missing_docs: List[str]

class DocumentationStrategy:
    """文档规范检查策略基类
    
    定义了检查文档规范的标准接口。所有具体的文档检查策略都必须继承此类，
    并实现get_type方法。check方法提供了默认实现，检查节点是否包含文档字符串。
    """
    
    def check(self, node: ast.AST) -> bool:
        """检查节点是否有文档字符串
        
        使用ast.get_docstring函数检查给定的AST节点是否包含文档字符串。
        
        Args:
            node: 要检查的AST节点
            
        Returns:
            bool: 如果节点有文档字符串返回True，否则返回False
            
        Example:
            >>> strategy = DocumentationStrategy()
            >>> node = ast.parse("def func():\\n    '''Doc.'''\\n    pass")
            >>> strategy.check(node.body[0])
            True
        """
        return ast.get_docstring(node) is not None
        
    def get_type(self) -> str:
        """获取文档类型名称
        
        Returns:
            str: 返回文档类型的中文描述
            
        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError

class ModuleDocumentation(DocumentationStrategy):
    """模块文档检查策略
    
    检查Python模块是否包含模块级文档字符串。模块级文档应该：
    1. 位于模块的最开始
    2. 描述模块的主要功能和用途
    3. 列出模块的主要组件
    4. 提供使用示例（如果适用）
    """
    
    def get_type(self) -> str:
        """获取文档类型名称
        
        Returns:
            str: 返回"模块"作为文档类型描述
        """
        return "模块"

class ClassDocumentation(DocumentationStrategy):
    """类文档检查策略
    
    检查Python类是否包含类文档字符串。类文档应该：
    1. 描述类的用途和职责
    2. 列出重要的属性和方法
    3. 提供使用示例
    4. 说明类的依赖关系（如果有）
    """
    
    def get_type(self) -> str:
        """获取文档类型名称
        
        Returns:
            str: 返回"类"作为文档类型描述
        """
        return "类"

class FunctionDocumentation(DocumentationStrategy):
    """函数文档检查策略
    
    检查Python函数是否包含函数文档字符串。函数文档应该：
    1. 描述函数的功能
    2. 列出参数及其类型
    3. 说明返回值
    4. 提供使用示例
    5. 说明可能的异常（如果有）
    """
    
    def get_type(self) -> str:
        """获取文档类型名称
        
        Returns:
            str: 返回"函数"作为文档类型描述
        """
        return "函数" 