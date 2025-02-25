"""Main module for code quality checking.

This module provides tools for checking and maintaining code quality, focusing on:
1. File structure analysis
2. Code complexity analysis
3. Naming convention checks
4. Documentation coverage checks
5. Code metrics collection
6. Git change tracking
"""

import ast
import os
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from .analyzers.base import BaseAnalyzer
from .analyzers.complexity import ComplexityAnalyzer
from .analyzers.naming import NamingAnalyzer
from .analyzers.documentation import DocumentationAnalyzer
from .analyzers.metrics import MetricsAnalyzer
from .analyzers.complexity.strategies import (
    ControlFlowComplexity,
    BooleanOperationComplexity
)
from .file_iterator import FileIterator
from .report import ReportGenerator, create_report_generator
from .config import ConfigManager

logger = logging.getLogger(__name__)

@dataclass
class CodeMetrics:
    """代码度量指标"""
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    complexity: int = 0
    functions: int = 0
    classes: int = 0
    docstring_coverage: float = 0.0

@dataclass
class FileStructure:
    """文件结构信息"""
    imports: List[str]
    classes: List[str]
    functions: List[str]
    globals: List[str]

@dataclass
class CodeQualityReport:
    """Report containing code quality analysis results."""
    total_files: int
    total_lines: int
    code_lines: int
    avg_complexity: float
    issues: List[str]
    file_metrics: Dict[str, Dict]

class CodeQualityChecker:
    """代码质量检查器
    
    使用不同的分析器检查代码质量的各个方面。
    """
    
    def __init__(self, project_root: str, config_path: Optional[str] = None):
        """初始化代码质量检查器
        
        Args:
            project_root: 项目根目录
            config_path: 配置文件路径
        """
        # 加载配置
        self.config_manager = ConfigManager()
        if config_path:
            self.config_manager.load_from_file(config_path)
        config = self.config_manager.get_config()
        
        # 初始化文件遍历器
        self.file_iterator = FileIterator(project_root, config.exclude_patterns)
        
        # 初始化分析器
        self.complexity_analyzer = ComplexityAnalyzer([
            ControlFlowComplexity(),
            BooleanOperationComplexity()
        ])
        self.naming_analyzer = NamingAnalyzer()
        self.documentation_analyzer = DocumentationAnalyzer()
        self.metrics_analyzer = MetricsAnalyzer()
        
        # Analysis thresholds
        self.max_complexity = 10
        self.min_doc_coverage = 0.8
        
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            分析结果字典
        """
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 解析AST
            tree = ast.parse(content)
            
            # 运行各个分析器
            results = {}
            results['metrics'] = self.metrics_analyzer.analyze(tree, content)
            results['complexity'] = self.complexity_analyzer.analyze(tree)
            results['naming'] = self.naming_analyzer.analyze(tree)
            results['documentation'] = self.documentation_analyzer.analyze(tree)
            
            return results
            
        except Exception as e:
            logger.error(f"分析文件 {file_path} 时发生错误: {str(e)}")
            return {'error': str(e)}
            
    def check_project(self, days: Optional[int] = None) -> CodeQualityReport:
        """检查整个项目
        
        Args:
            days: 可选，只检查最近几天修改的文件
            
        Returns:
            项目检查结果
        """
        total_files = 0
        total_lines = 0
        total_code_lines = 0
        total_complexity = 0
        issues = []
        file_metrics = {}
        
        # 遍历项目文件
        for rel_path, abs_path in self.file_iterator.iter_python_files(days):
            total_files += 1
            
            # 分析文件
            file_results = self.analyze_file(Path(abs_path))
            
            if 'error' in file_results:
                issues.append(f"{rel_path}: {file_results['error']}")
                continue
                
            # Record metrics
            metrics = file_results['metrics']
            total_lines += metrics.total_lines
            total_code_lines += metrics.code_lines
            
            # Check complexity
            complexity = file_results['complexity']
            total_complexity += complexity.score
            if complexity.score > self.max_complexity:
                for detail in complexity.details:
                    issues.append(
                        f"{rel_path}: High complexity ({detail.score}) at {detail.location}"
                    )
            
            # Check naming
            naming = file_results['naming']
            for issue in naming.issues:
                issues.append(f"{rel_path}: {issue}")
            
            # Check documentation
            documentation = file_results['documentation']
            if documentation.coverage < self.min_doc_coverage:
                issues.append(
                    f"{rel_path}: Low documentation coverage ({documentation.coverage:.0%})"
                )
            
            # Record file metrics
            file_metrics[rel_path] = {
                'lines': metrics.total_lines,
                'code_lines': metrics.code_lines,
                'complexity': complexity.score,
                'doc_coverage': documentation.coverage
            }
        
        return CodeQualityReport(
            total_files=total_files,
            total_lines=total_lines,
            code_lines=total_code_lines,
            avg_complexity=total_complexity / total_files if total_files > 0 else 0,
            issues=issues,
            file_metrics=file_metrics
        )
        
    def generate_report(self, format: str = 'text', days: Optional[int] = None) -> str:
        """生成检查报告
        
        Args:
            format: 报告格式（text/json/html）
            days: 可选，只检查最近几天修改的文件
            
        Returns:
            生成的报告
        """
        # 运行检查
        results = self.check_project(days)
        
        # 创建报告生成器
        generator = create_report_generator(format)
        
        # 构建报告数据
        report_data = {
            'total_files': results.total_files,
            'total_lines': results.total_lines,
            'code_lines': results.code_lines,
            'avg_complexity': results.avg_complexity,
            'issues': results.issues,
            'file_metrics': results.file_metrics
        }
        
        # 生成报告
        return generator.generate(report_data) 