from typing import Dict, List, Optional
from datetime import datetime
import logging
import time

class TestExecutor:
    """测试执行器，负责执行自动化测试用例"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results: Dict[str, Dict] = {}
        
    def setup_test_environment(self) -> None:
        """设置测试环境"""
        try:
            # 初始化WebDriver
            from src.utils.driver.webdriver_manager import WebDriverManager
            self.driver_manager = WebDriverManager()
            self.driver = self.driver_manager.init_driver()
            self.logger.info('测试环境设置完成')
        except Exception as e:
            self.logger.error(f'设置测试环境失败: {str(e)}')
            raise

    def execute_test(self, test_case_id: str, test_data: Dict) -> Dict:
        """执行单个测试用例
        
        Args:
            test_case_id: 测试用例ID
            test_data: 测试数据
            
        Returns:
            包含测试结果的字典
        """
        try:
            # 记录开始时间
            start_time = datetime.now()
            
            # 设置测试环境
            self.setup_test_environment()
            
            # 加载测试用例管理器
            from src.core.test_case.case_manager import TestCaseManager
            case_manager = TestCaseManager(self.driver)
            
            # 执行自动化测试步骤
            case_manager.mark_auto_type(test_case_id, test_data.get('auto_type', '是'))
            test_passed = True
            
            # 构建测试结果
            result = {
                'case_id': test_case_id,
                'status': 'passed' if test_passed else 'failed',
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'error_message': None
            }
            
            self.test_results[test_case_id] = result
            return result
            
        except Exception as e:
            self.logger.error(f'Test case {test_case_id} failed: {str(e)}')
            result = {
                'case_id': test_case_id,
                'status': 'failed',
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'error_message': str(e)
            }
            self.test_results[test_case_id] = result
            return result
        finally:
            self.cleanup()
            
    def cleanup(self) -> None:
        """清理测试环境"""
        try:
            if hasattr(self, 'driver_manager'):
                self.driver_manager.quit_driver()
            self.logger.info('测试环境清理完成')
        except Exception as e:
            self.logger.error(f'清理测试环境失败: {str(e)}')

    def execute_test_suite(self, test_cases: List[Dict]) -> List[Dict]:
        """执行测试套件
        
        Args:
            test_cases: 测试用例列表
            
        Returns:
            测试结果列表
        """
        results = []
        try:
            self.logger.info("开始执行测试套件")
            self.logger.info(f"测试用例列表: {test_cases}")
            
            # 在套件级别设置测试环境
            self.logger.info("正在设置测试环境...")
            self.setup_test_environment()
            self.logger.info("测试环境设置完成")
            
            # 加载测试用例管理器
            self.logger.info("正在初始化测试用例管理器...")
            from src.core.test_case.case_manager import TestCaseManager
            case_manager = TestCaseManager(self.driver)
            self.logger.info("测试用例管理器初始化完成")
            
            for test_case in test_cases:
                try:
                    # 记录开始时间
                    start_time = datetime.now()
                    test_case_id = test_case.get('id')
                    test_data = test_case.get('data', {})
                    
                    self.logger.info(f"开始执行测试用例 {test_case_id}")
                    self.logger.info(f"测试数据: {test_data}")
                    
                    # 执行自动化测试步骤
                    self.logger.info("正在标记自动化类型...")
                    case_manager.mark_auto_type(test_case_id, test_data.get('auto_type', '是'))
                    test_passed = True
                    self.logger.info("自动化类型标记完成")
                    
                    # 构建测试结果
                    result = {
                        'case_id': test_case_id,
                        'status': 'passed' if test_passed else 'failed',
                        'start_time': start_time.isoformat(),
                        'end_time': datetime.now().isoformat(),
                        'error_message': None
                    }
                    self.logger.info(f"测试用例 {test_case_id} 执行成功")
                    
                except Exception as e:
                    self.logger.error(f"测试用例 {test_case_id} 执行失败")
                    self.logger.error(f"错误信息: {str(e)}")
                    self.logger.exception("详细错误信息:")
                    result = {
                        'case_id': test_case_id,
                        'status': 'failed',
                        'start_time': start_time.isoformat(),
                        'end_time': datetime.now().isoformat(),
                        'error_message': str(e)
                    }
                
                self.test_results[test_case_id] = result
                results.append(result)
                
        except Exception as e:
            self.logger.error("测试套件执行过程中发生错误")
            self.logger.error(f"错误信息: {str(e)}")
            self.logger.exception("详细错误信息:")
            raise
            
        finally:
            # 在套件执行完成后清理环境
            self.logger.info("正在清理测试环境...")
            self.cleanup()
            self.logger.info("测试环境清理完成")
            self.logger.info("测试套件执行完成")
            
        return results