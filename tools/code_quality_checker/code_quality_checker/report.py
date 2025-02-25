"""Report generation for code quality analysis."""

from abc import ABC, abstractmethod
from typing import Dict, List


class ReportGenerator(ABC):
    """Base class for report generators."""

    @abstractmethod
    def generate(self, metrics: Dict) -> str:
        """Generate a report from metrics.
        
        Args:
            metrics: Dictionary containing analysis metrics
            
        Returns:
            Generated report as a string
        """
        pass


class TextReportGenerator(ReportGenerator):
    """Generate text format reports."""

    def generate(self, metrics: Dict) -> str:
        lines = [
            "Code Quality Report",
            "==================",
            "",
            "Project Overview:",
            f"Total files: {metrics['total_files']}",
            f"Total lines: {metrics['total_lines']}",
            f"Code lines: {metrics['code_lines']}",
            f"Average complexity: {metrics['avg_complexity']:.2f}",
            "",
            "File Analysis:",
            "-------------"
        ]
        
        # Add file metrics
        for file_path, file_metrics in metrics['file_metrics'].items():
            lines.extend([
                f"\n{file_path}:",
                f"  Lines: {file_metrics['lines']}",
                f"  Code lines: {file_metrics['code_lines']}",
                f"  Complexity: {file_metrics['complexity']}",
                f"  Documentation coverage: {file_metrics['doc_coverage']:.0%}"
            ])
        
        # Add issues
        if metrics['issues']:
            lines.extend([
                "",
                "Issues Found:",
                "------------"
            ])
            for issue in metrics['issues']:
                lines.append(f"- {issue}")
        
        return "\n".join(lines)


class JsonReportGenerator(ReportGenerator):
    """Generate JSON format reports."""

    def generate(self, metrics: Dict) -> str:
        import json
        return json.dumps(metrics, indent=2)


class HtmlReportGenerator(ReportGenerator):
    """Generate HTML format reports."""

    def generate(self, metrics: Dict) -> str:
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<title>Code Quality Report</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; }",
            "h1, h2 { color: #333; }",
            ".overview { background: #f5f5f5; padding: 15px; border-radius: 5px; }",
            ".file { margin: 20px 0; padding: 10px; border: 1px solid #ddd; }",
            ".issues { color: #d73a49; }",
            "</style>",
            "</head>",
            "<body>",
            "<h1>Code Quality Report</h1>",
            
            '<div class="overview">',
            "<h2>Project Overview</h2>",
            f"<p>Total files: {metrics['total_files']}</p>",
            f"<p>Total lines: {metrics['total_lines']}</p>",
            f"<p>Code lines: {metrics['code_lines']}</p>",
            f"<p>Average complexity: {metrics['avg_complexity']:.2f}</p>",
            "</div>",
            
            "<h2>File Analysis</h2>"
        ]
        
        # Add file metrics
        for file_path, file_metrics in metrics['file_metrics'].items():
            html.extend([
                '<div class="file">',
                f"<h3>{file_path}</h3>",
                "<ul>",
                f"<li>Lines: {file_metrics['lines']}</li>",
                f"<li>Code lines: {file_metrics['code_lines']}</li>",
                f"<li>Complexity: {file_metrics['complexity']}</li>",
                f"<li>Documentation coverage: {file_metrics['doc_coverage']:.0%}</li>",
                "</ul>",
                "</div>"
            ])
        
        # Add issues
        if metrics['issues']:
            html.extend([
                '<div class="issues">',
                "<h2>Issues Found</h2>",
                "<ul>"
            ])
            for issue in metrics['issues']:
                html.append(f"<li>{issue}</li>")
            html.extend([
                "</ul>",
                "</div>"
            ])
        
        html.extend([
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html)


def create_report_generator(format: str) -> ReportGenerator:
    """Create a report generator for the specified format.
    
    Args:
        format: Report format ('text', 'json', or 'html')
        
    Returns:
        Appropriate report generator instance
        
    Raises:
        ValueError: If format is not supported
    """
    generators = {
        'text': TextReportGenerator,
        'json': JsonReportGenerator,
        'html': HtmlReportGenerator
    }
    
    if format not in generators:
        raise ValueError(f"Unsupported report format: {format}")
        
    return generators[format]() 