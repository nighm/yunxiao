"""代码分析器模块

这个模块包含了各种专门的代码分析器，每个分析器负责一个特定的分析任务。
使用策略模式和访问者模式来保持代码简洁和可维护。

主要组件：
1. 分析结果类 - 用于存储各种分析的结果
2. 访问者接口 - 提供AST遍历的统一接口
3. 复杂度策略 - 不同类型的复杂度计算策略
4. 命名规范策略 - 不同类型的命名规范检查
5. 分析器实现 - 具体的分析器类
"""

import ast
import re
from typing import List, Dict, Set, Optional, Protocol, Iterator
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ===== 基础结果类 =====

@dataclass
class AnalysisResult:
    """分析结果基类
    
    所有具体的分析结果类都应该继承自这个基类。
    """
    pass

@dataclass
class ComplexityResult(AnalysisResult):
    """复杂度分析结果
    
    Attributes:
        score: 总体复杂度分数
        details: 各部分复杂度的详细信息
    """
    score: int = 0
    details: Dict[str, int] = field(default_factory=dict)

@dataclass
class NamingResult(AnalysisResult):
    """命名规范分析结果
    
    Attributes:
        issues: 发现的命名问题列表
    """
    issues: List[str] = field(default_factory=list)

@dataclass
class DocumentationResult(AnalysisResult):
    """文档分析结果
    
    Attributes:
        coverage: 文档覆盖率（0.0-1.0）
        documented_items: 已文档化的项目数
        total_items: 总项目数
    """
    coverage: float = 0.0
    documented_items: int = 0
    total_items: int = 0

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

# ===== 复杂度分析策略 =====

class ComplexityStrategy(ABC):
    """复杂度计算策略基类
    
    定义了计算代码复杂度的标准接口。
    """
    
    @abstractmethod
    def calculate(self, node: ast.AST) -> int:
        """计算复杂度分数
        
        Args:
            node: AST节点
            
        Returns:
            复杂度分数
        """
        pass

class ControlFlowComplexity(ComplexityStrategy):
    """控制流复杂度计算策略
    
    计算代码中控制流语句（if、while、for、except）导致的复杂度。
    """
    
    def calculate(self, node: ast.AST) -> int:
        """计算控制流复杂度
        
        Args:
            node: AST节点
            
        Returns:
            控制流复杂度分数
        """
        return sum(1 for child in ast.walk(node)
                  if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)))

class BooleanOperationComplexity(ComplexityStrategy):
    """布尔运算复杂度计算策略
    
    计算代码中布尔运算（and、or）导致的复杂度。
    """
    
    def calculate(self, node: ast.AST) -> int:
        """计算布尔运算复杂度
        
        Args:
            node: AST节点
            
        Returns:
            布尔运算复杂度分数
        """
        return sum(len(child.values) - 1 for child in ast.walk(node)
                  if isinstance(child, ast.BoolOp))

# ===== 命名规范策略 =====

class NamingStrategy(ABC):
    """命名规范检查策略基类
    
    定义了检查命名规范的标准接口。
    """
    
    @abstractmethod
    def check(self, name: str) -> bool:
        """检查名称是否符合规范
        
        Args:
            name: 要检查的名称
            
        Returns:
            是否符合规范
        """
        pass
        
    @abstractmethod
    def get_type(self) -> str:
        """获取命名类型描述
        
        Returns:
            命名类型的中文描述
        """
        pass

class ClassNaming(NamingStrategy):
    """类命名规范检查
    
    检查类名是否符合大驼峰命名规范（PascalCase）。
    """
    
    def check(self, name: str) -> bool:
        return bool(re.match(r'^[A-Z][a-zA-Z0-9]*$', name))
        
    def get_type(self) -> str:
        return "类名"

class FunctionNaming(NamingStrategy):
    """函数命名规范检查
    
    检查函数名是否符合小写字母开头，可包含下划线的规范。
    """
    
    def check(self, name: str) -> bool:
        return bool(re.match(r'^[a-z][a-zA-Z0-9_]*$', name))
        
    def get_type(self) -> str:
        return "函数名"

class VariableNaming(NamingStrategy):
    """变量命名规范检查
    
    检查变量名是否符合小写字母开头，可包含下划线的规范。
    """
    
    def check(self, name: str) -> bool:
        return bool(re.match(r'^[a-z][a-zA-Z0-9_]*$', name))
        
    def get_type(self) -> str:
        return "变量名"

# ===== 分析器实现 =====

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

class ComplexityAnalyzer(BaseAnalyzer):
    """代码复杂度分析器
    
    使用不同的策略计算代码的总体复杂度。
    """
    
    def __init__(self):
        """初始化复杂度分析器"""
        self.strategies = [
            ControlFlowComplexity(),
            BooleanOperationComplexity()
        ]
        
    def analyze(self, node: ast.AST) -> ComplexityResult:
        """分析代码复杂度
        
        Args:
            node: AST节点
            
        Returns:
            复杂度分析结果
        """
        details = {'base': 1}  # 基础复杂度
        total = 1
        
        # 应用每个复杂度计算策略
        for strategy in self.strategies:
            score = strategy.calculate(node)
            strategy_name = strategy.__class__.__name__.lower()
            details[strategy_name] = score
            total += score
            
        return ComplexityResult(score=total, details=details)

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

class DocumentationAnalyzer(BaseAnalyzer):
    """文档完整性分析器
    
    检查模块、类和函数的文档字符串完整性。
    """
    
    def check_docstring(self, node: ast.AST) -> bool:
        """检查是否有文档字符串
        
        Args:
            node: AST节点
            
        Returns:
            是否有文档字符串
        """
        return ast.get_docstring(node) is not None
        
    def analyze(self, node: ast.AST) -> DocumentationResult:
        """分析文档完整性
        
        Args:
            node: AST节点
            
        Returns:
            文档分析结果
        """
        documentable_items = 1  # 模块本身
        documented_items = 1 if self.check_docstring(node) else 0
        
        # 检查类和函数的文档
        for child in ast.walk(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef)):
                documentable_items += 1
                if self.check_docstring(child):
                    documented_items += 1
                    
        coverage = documented_items / documentable_items if documentable_items > 0 else 1.0
        
        return DocumentationResult(
            coverage=coverage,
            documented_items=documented_items,
            total_items=documentable_items
        ) 