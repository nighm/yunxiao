"""Complexity analyzer module."""

import ast
from typing import List

from ..base import BaseAnalyzer
from .strategies import ComplexityResult, ComplexityStrategy

class ComplexityAnalyzer(BaseAnalyzer):
    """Analyzer for code complexity."""

    def __init__(self, strategies: List[ComplexityStrategy] = None):
        """Initialize the complexity analyzer.
        
        Args:
            strategies: List of complexity calculation strategies to use
        """
        self.strategies = strategies or []

    def analyze(self, node: ast.AST) -> ComplexityResult:
        """Analyze the AST node for code complexity.
        
        Args:
            node: The AST node to analyze
        
        Returns:
            ComplexityResult containing the complexity score and details
        """
        total = 0
        details = []
        
        for strategy in self.strategies:
            result = strategy.calculate_complexity(node)
            total += result.score
            details.extend(result.details)
            
        return ComplexityResult(score=total, details=details) 