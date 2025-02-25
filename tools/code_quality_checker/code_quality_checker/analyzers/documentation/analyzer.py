"""文档分析器模块

这个模块实现了文档规范分析器。
"""

import ast
from ..base import BaseAnalyzer
from .strategies import (
    DocumentationResult,
    ModuleDocumentation,
    ClassDocumentation,
    FunctionDocumentation
)

class DocumentationAnalyzer(BaseAnalyzer):
    """文档规范分析器
    
    使用不同的策略检查各类文档是否符合规范。
    """
    
    def __init__(self):
        """初始化文档规范分析器"""
        self.strategies = {
            ast.Module: ModuleDocumentation(),
            ast.ClassDef: ClassDocumentation(),
            ast.FunctionDef: FunctionDocumentation()
        }
        
    def analyze(self, node: ast.AST) -> DocumentationResult:
        """分析文档规范
        
        Args:
            node: AST节点
            
        Returns:
            文档规范分析结果
        """
        missing_docs = []
        total_nodes = 0
        documented_nodes = 0
        
        # 首先检查模块级文档
        if isinstance(node, ast.Module):
            total_nodes += 1
            if self.strategies[ast.Module].check(node):
                documented_nodes += 1
            else:
                missing_docs.append("模块缺少文档字符串")
        
        # 遍历所有需要文档的节点
        for child in ast.walk(node):
            node_type = type(child)
            if node_type in self.strategies and node_type != ast.Module:  # 模块已经检查过了
                total_nodes += 1
                strategy = self.strategies[node_type]
                
                if strategy.check(child):
                    documented_nodes += 1
                else:
                    name = child.name if hasattr(child, 'name') else '<anonymous>'
                    missing_docs.append(f"{strategy.get_type()} '{name}' 缺少文档字符串")
                    
        coverage = (documented_nodes / total_nodes * 100) if total_nodes > 0 else 100.0
        return DocumentationResult(coverage=coverage, missing_docs=missing_docs) 