"""命名规范分析器模块

这个模块实现了命名规范分析器。
"""

import ast
from ..base import BaseAnalyzer
from .strategies import (
    NamingResult,
    ClassNaming,
    FunctionNaming,
    VariableNaming
)

class NamingAnalyzer(BaseAnalyzer):
    """命名规范分析器
    
    使用不同的策略检查各类命名是否符合规范。
    """
    
    def __init__(self):
        """初始化命名规范分析器"""
        self.strategies = {
            ast.ClassDef: ClassNaming(),
            ast.FunctionDef: FunctionNaming(),
            ast.Name: VariableNaming()
        }
        
    def is_special_name(self, name: str) -> bool:
        """检查是否是特殊名称
        
        Args:
            name: 要检查的名称
            
        Returns:
            是否是特殊名称
        """
        return (name.startswith('__') and name.endswith('__')) or \
               (name.startswith('_') and not name.startswith('__'))
               
    def analyze(self, node: ast.AST) -> NamingResult:
        """分析命名规范
        
        Args:
            node: AST节点
            
        Returns:
            命名规范分析结果
        """
        issues = []
        
        for child in ast.walk(node):
            node_type = type(child)
            if node_type in self.strategies:
                strategy = self.strategies[node_type]
                name = child.name if hasattr(child, 'name') else \
                       child.id if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store) else None
                       
                if name and not self.is_special_name(name) and not strategy.check(name):
                    issues.append(f"{strategy.get_type()} '{name}' 不符合命名规范")
                    
        return NamingResult(issues=issues) 