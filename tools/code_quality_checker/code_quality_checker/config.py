"""配置管理器模块

这个模块负责管理代码质量检查工具的配置。
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import json
from pathlib import Path

@dataclass
class QualityConfig:
    """代码质量检查配置
    
    Attributes:
        complexity_threshold: 复杂度阈值
        doc_coverage_threshold: 文档覆盖率阈值
        exclude_patterns: 要排除的文件模式
        naming_conventions: 命名规范配置
    """
    complexity_threshold: int = 10
    doc_coverage_threshold: float = 80.0
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "venv/*",
        ".*",
        "build/*",
        "dist/*",
        "*egg-info/*",
        "__pycache__/*",
        "tests/*"
    ])
    naming_conventions: Dict[str, str] = field(default_factory=lambda: {
        "class": r"^[A-Z][a-zA-Z0-9]*$",
        "function": r"^[a-z][a-zA-Z0-9_]*$",
        "variable": r"^[a-z][a-zA-Z0-9_]*$"
    })

class ConfigManager:
    """配置管理器
    
    负责加载和管理代码质量检查工具的配置。
    """
    
    DEFAULT_CONFIG_NAME = ".code-quality.json"
    
    def __init__(self):
        """初始化配置管理器"""
        self.config = QualityConfig()
        
    def load_from_file(self, config_path: Optional[str] = None) -> bool:
        """从文件加载配置
        
        Args:
            config_path: 配置文件路径，如果为None则搜索默认位置
            
        Returns:
            是否成功加载配置
        """
        if config_path is None:
            # 搜索默认配置文件
            search_paths = [
                Path.cwd() / self.DEFAULT_CONFIG_NAME,
                Path.home() / self.DEFAULT_CONFIG_NAME
            ]
            for path in search_paths:
                if path.exists():
                    config_path = str(path)
                    break
                    
        if not config_path or not os.path.exists(config_path):
            return False
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 更新配置
            if 'complexity_threshold' in data:
                self.config.complexity_threshold = int(data['complexity_threshold'])
                
            if 'doc_coverage_threshold' in data:
                self.config.doc_coverage_threshold = float(data['doc_coverage_threshold'])
                
            if 'exclude_patterns' in data:
                self.config.exclude_patterns = list(data['exclude_patterns'])
                
            if 'naming_conventions' in data:
                self.config.naming_conventions.update(data['naming_conventions'])
                
            return True
            
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
            return False
            
    def save_to_file(self, config_path: str) -> bool:
        """保存配置到文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            是否成功保存配置
        """
        try:
            data = {
                'complexity_threshold': self.config.complexity_threshold,
                'doc_coverage_threshold': self.config.doc_coverage_threshold,
                'exclude_patterns': self.config.exclude_patterns,
                'naming_conventions': self.config.naming_conventions
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            return True
            
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False
            
    def get_config(self) -> QualityConfig:
        """获取当前配置
        
        Returns:
            配置对象
        """
        return self.config
        
    def update_config(self, **kwargs) -> None:
        """更新配置
        
        Args:
            **kwargs: 要更新的配置项
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value) 