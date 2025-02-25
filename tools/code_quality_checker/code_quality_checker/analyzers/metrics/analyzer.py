"""Module for analyzing code metrics.

This module provides functionality to analyze various code metrics including:
- Total lines of code
- Number of code lines
- Number of comment lines
- Number of blank lines
- Number of functions
- Number of classes
"""

import ast
from dataclasses import dataclass
from typing import List

from ..base import BaseAnalyzer, AnalysisResult


@dataclass
class MetricsResult(AnalysisResult):
    """Result class for code metrics analysis."""
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    num_functions: int = 0
    num_classes: int = 0


class MetricsAnalyzer(BaseAnalyzer):
    """Analyzer for collecting code metrics."""

    def analyze(self, node: ast.AST, code: str) -> MetricsResult:
        """Analyze the AST and source code to collect metrics.
        
        Args:
            node: The AST node to analyze
            code: The source code string
        
        Returns:
            MetricsResult containing the collected metrics
        """
        result = MetricsResult()
        
        # Calculate line metrics
        lines = code.splitlines()
        result.total_lines = len(lines)
        result.blank_lines = sum(1 for line in lines if not line.strip())
        result.comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        result.code_lines = result.total_lines - result.blank_lines - result.comment_lines
        
        # Count functions and classes
        for node in ast.walk(node):
            if isinstance(node, ast.FunctionDef):
                result.num_functions += 1
            elif isinstance(node, ast.ClassDef):
                result.num_classes += 1
        
        return result 