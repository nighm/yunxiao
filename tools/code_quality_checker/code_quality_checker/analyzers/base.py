"""分析器基础模块

这个模块定义了所有分析器共用的基础类和接口。
"""

import ast
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Protocol

# ===== 基础结果类 =====

@dataclass
class AnalysisResult:
    """分析结果基类
    
    所有具体的分析结果类都应该继承自这个基类。
    """
    pass

# ===== 访问者模式接口 =====

class NodeVisitor(Protocol):
    """AST节点访问者协议
    
    定义了访问AST节点的标准接口。所有需要遍历AST的类都应该实现这个协议。
    """
    def visit(self, node: ast.AST) -> None:
        """访问AST节点
        
        Args:
            node: 要访问的AST节点
        """
        pass

class BaseAnalyzer:
    """分析器基类
    
    所有具体的分析器都应该继承这个基类。
    """
    
    def analyze(self, node: ast.AST) -> AnalysisResult:
        """执行分析
        
        Args:
            node: AST节点
            
        Returns:
            分析结果
        """
        raise NotImplementedError 