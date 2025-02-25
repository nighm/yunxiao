"""命名规范策略模块

这个模块定义了不同类型的命名规范检查策略，包括类名、函数名和变量名的检查规则。
每个策略都实现了统一的接口，使用正则表达式进行命名规范的验证。
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

@dataclass
class NamingResult:
    """命名规范分析结果
    
    用于存储命名规范检查过程中发现的问题。每个问题都会被记录为一个字符串，
    描述具体的命名不符合规范的原因。
    
    Attributes:
        issues: 发现的命名问题列表，每个元素是一个描述性的错误消息
    """
    issues: List[str] = field(default_factory=list)

class NamingStrategy(ABC):
    """命名规范检查策略基类
    
    定义了检查命名规范的标准接口。所有具体的命名规范检查策略都必须继承此类，
    并实现check和get_type方法。这种设计允许灵活地添加新的命名规范检查规则。
    """
    
    @abstractmethod
    def check(self, name: str) -> bool:
        """检查名称是否符合规范
        
        Args:
            name: 要检查的名称字符串
            
        Returns:
            bool: 如果名称符合规范返回True，否则返回False
            
        Example:
            >>> strategy = SomeNamingStrategy()
            >>> strategy.check("validName")
            True
        """
        pass
        
    @abstractmethod
    def get_type(self) -> str:
        """获取命名类型描述
        
        Returns:
            str: 返回命名类型的中文描述，如"类名"、"函数名"等
            
        Example:
            >>> strategy = SomeNamingStrategy()
            >>> strategy.get_type()
            '类名'
        """
        pass

class ClassNaming(NamingStrategy):
    """类命名规范检查
    
    检查类名是否符合大驼峰命名规范（PascalCase）。
    规则要求：
    1. 必须以大写字母开头
    2. 后续字符只能是字母或数字
    3. 不允许使用下划线
    """
    
    def check(self, name: str) -> bool:
        """检查类名是否符合大驼峰命名规范
        
        Args:
            name: 要检查的类名
            
        Returns:
            bool: 如果类名符合大驼峰命名规范返回True，否则返回False
            
        Example:
            >>> class_naming = ClassNaming()
            >>> class_naming.check("MyClass")
            True
            >>> class_naming.check("my_class")
            False
        """
        return bool(re.match(r'^[A-Z][a-zA-Z0-9]*$', name))
        
    def get_type(self) -> str:
        """获取命名类型描述
        
        Returns:
            str: 返回"类名"作为命名类型描述
        """
        return "类名"

class FunctionNaming(NamingStrategy):
    """函数命名规范检查
    
    检查函数名是否符合小写字母开头，可包含下划线的规范。
    规则要求：
    1. 必须以小写字母开头
    2. 可以包含字母、数字和下划线
    3. 建议使用下划线分隔单词（snake_case）
    """
    
    def check(self, name: str) -> bool:
        """检查函数名是否符合命名规范
        
        Args:
            name: 要检查的函数名
            
        Returns:
            bool: 如果函数名符合命名规范返回True，否则返回False
            
        Example:
            >>> func_naming = FunctionNaming()
            >>> func_naming.check("calculate_total")
            True
            >>> func_naming.check("CalculateTotal")
            False
        """
        return bool(re.match(r'^[a-z][a-zA-Z0-9_]*$', name))
        
    def get_type(self) -> str:
        """获取命名类型描述
        
        Returns:
            str: 返回"函数名"作为命名类型描述
        """
        return "函数名"

class VariableNaming(NamingStrategy):
    """变量命名规范检查
    
    检查变量名是否符合小写字母开头，可包含下划线的规范。
    规则要求：
    1. 必须以小写字母开头
    2. 可以包含字母、数字和下划线
    3. 建议使用下划线分隔单词（snake_case）
    4. 避免使用单个字母（除非是循环计数器）
    """
    
    def check(self, name: str) -> bool:
        """检查变量名是否符合命名规范
        
        Args:
            name: 要检查的变量名
            
        Returns:
            bool: 如果变量名符合命名规范返回True，否则返回False
            
        Example:
            >>> var_naming = VariableNaming()
            >>> var_naming.check("user_name")
            True
            >>> var_naming.check("UserName")
            False
        """
        return bool(re.match(r'^[a-z][a-zA-Z0-9_]*$', name))
        
    def get_type(self) -> str:
        """获取命名类型描述
        
        Returns:
            str: 返回"变量名"作为命名类型描述
        """
        return "变量名" 