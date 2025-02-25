from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import logging

class ResultManager:
    """测试结果管理器，负责处理和存储测试结果"""
    
    def __init__(self, output_dir: str = 'output/test_results'):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        self._ensure_output_dir()
        
    def _ensure_output_dir(self) -> None:
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def save_result(self, result: Dict) -> None:
        """保存单个测试结果
        
        Args:
            result: 测试结果字典
        """
        try:
            case_id = result.get('case_id')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{case_id}_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f'Result saved: {filepath}')
            
        except Exception as e:
            self.logger.error(f'Failed to save result: {str(e)}')
            
    def save_suite_results(self, results: List[Dict]) -> None:
        """保存测试套件的所有结果
        
        Args:
            results: 测试结果列表
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        suite_filename = f"test_suite_{timestamp}.json"
        suite_filepath = os.path.join(self.output_dir, suite_filename)
        
        try:
            with open(suite_filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f'Suite results saved: {suite_filepath}')
            
        except Exception as e:
            self.logger.error(f'Failed to save suite results: {str(e)}')
            
    def get_result(self, case_id: str) -> Optional[Dict]:
        """获取指定测试用例的最新结果
        
        Args:
            case_id: 测试用例ID
            
        Returns:
            测试结果字典，如果未找到则返回None
        """
        try:
            # 获取所有结果文件
            result_files = [f for f in os.listdir(self.output_dir) 
                          if f.startswith(case_id) and f.endswith('.json')]
            
            if not result_files:
                return None
                
            # 获取最新的结果文件
            latest_file = sorted(result_files)[-1]
            filepath = os.path.join(self.output_dir, latest_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f'Failed to get result: {str(e)}')
            return None
            
    def get_suite_results(self, suite_id: str) -> Optional[List[Dict]]:
        """获取测试套件的结果
        
        Args:
            suite_id: 测试套件ID
            
        Returns:
            测试结果列表，如果未找到则返回None
        """
        try:
            suite_files = [f for f in os.listdir(self.output_dir) 
                          if f.startswith('test_suite_') and f.endswith('.json')]
            
            if not suite_files:
                return None
                
            # 获取最新的结果文件
            latest_file = sorted(suite_files)[-1]
            filepath = os.path.join(self.output_dir, latest_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
            
            if not suite_files:
                return None
                
            latest_file = sorted(suite_files)[-1]
            filepath = os.path.join(self.output_dir, latest_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f'Failed to get suite results: {str(e)}')
            return None