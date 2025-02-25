"""File iteration utilities for code quality checking."""

import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator, List, Optional, Tuple


class FileIterator:
    """Iterator for Python files in a project."""

    def __init__(self, project_root: str, exclude_patterns: List[str] = None):
        """Initialize the file iterator.
        
        Args:
            project_root: Root directory of the project
            exclude_patterns: List of glob patterns for files to exclude
        """
        self.project_root = Path(project_root)
        self.exclude_patterns = exclude_patterns or [
            '**/.*',
            '**/venv/**',
            '**/env/**',
            '**/build/**',
            '**/dist/**',
            '**/__pycache__/**',
            '**/*.pyc',
            '**/*.pyo',
            '**/*.pyd',
            '**/setup.py'
        ]

    def should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded based on patterns.
        
        Args:
            path: Path to check
            
        Returns:
            True if the path should be excluded
        """
        rel_path = str(path.relative_to(self.project_root))
        return any(re.match(pattern.replace('*', '.*'), rel_path)
                  for pattern in self.exclude_patterns)

    def get_git_changed_files(self, days: int) -> List[str]:
        """Get list of Python files changed in Git within specified days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of relative paths to changed Python files
        """
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        try:
            result = subprocess.run(
                ['git', 'log', '--name-only', '--pretty=format:', f'--since={since_date}'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            changed_files = set(
                line for line in result.stdout.splitlines()
                if line and line.endswith('.py')
            )
            return list(changed_files)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []

    def iter_python_files(self, days: Optional[int] = None) -> Iterator[Tuple[str, str]]:
        """Iterate over Python files in the project.
        
        Args:
            days: Optional number of days to limit to recently changed files
            
        Yields:
            Tuples of (relative_path, absolute_path) for each Python file
        """
        changed_files = set(self.get_git_changed_files(days)) if days else None
        
        for root, _, files in os.walk(self.project_root):
            root_path = Path(root)
            if self.should_exclude(root_path):
                continue
                
            for file in files:
                if not file.endswith('.py'):
                    continue
                    
                file_path = root_path / file
                if self.should_exclude(file_path):
                    continue
                    
                rel_path = file_path.relative_to(self.project_root)
                if changed_files is not None and str(rel_path) not in changed_files:
                    continue
                    
                yield str(rel_path), str(file_path) 