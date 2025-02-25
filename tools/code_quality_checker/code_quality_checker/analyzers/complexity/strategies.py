"""Complexity calculation strategies."""

import ast
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ComplexityDetail:
    """Details about a specific complexity contribution."""
    type: str
    score: int
    location: str


@dataclass
class ComplexityResult:
    """Result of complexity analysis."""
    score: int
    details: List[ComplexityDetail]


class ComplexityStrategy(ABC):
    """Base class for complexity calculation strategies."""
    
    @abstractmethod
    def calculate_complexity(self, node: ast.AST) -> ComplexityResult:
        """Calculate complexity score for an AST node.
        
        Args:
            node: The AST node to analyze
            
        Returns:
            ComplexityResult containing the complexity score and details
        """
        pass


class ControlFlowComplexity(ComplexityStrategy):
    """Calculate complexity based on control flow statements."""
    
    def calculate_complexity(self, node: ast.AST) -> ComplexityResult:
        score = 0
        details = []
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                score += 1
                details.append(ComplexityDetail(
                    type=child.__class__.__name__,
                    score=1,
                    location=f"line {child.lineno}"
                ))
                
        return ComplexityResult(score=score, details=details)


class BooleanOperationComplexity(ComplexityStrategy):
    """Calculate complexity based on boolean operations."""
    
    def calculate_complexity(self, node: ast.AST) -> ComplexityResult:
        score = 0
        details = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.BoolOp):
                # Add 1 for each additional operand beyond 2
                additional_score = len(child.values) - 2
                if additional_score > 0:
                    score += additional_score
                    details.append(ComplexityDetail(
                        type="BooleanOperation",
                        score=additional_score,
                        location=f"line {child.lineno}"
                    ))
                
        return ComplexityResult(score=score, details=details) 