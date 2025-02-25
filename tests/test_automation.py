import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import os
import json
from src.core.automation.test_executor import TestExecutor
from src.core.automation.result_manager import ResultManager

class TestAutomationCore(unittest.TestCase):
    def setUp(self):
        self.test_executor = TestExecutor()
        self.result_manager = ResultManager(output_dir='tests/test_output')
        
    def tearDown(self):
        # 清理测试输出目录
        if os.path.exists('tests/test_output'):
            for file in os.listdir('tests/test_output'):
                os.remove(os.path.join('tests/test_output', file))
            os.rmdir('tests/test_output')
            
    def test_execute_single_test(self):
        """测试单个测试用例执行"""
        test_case_id = 'TEST_001'
        test_data = {'input': 'test_value'}
        
        result = self.test_executor.execute_test(test_case_id, test_data)
        
        self.assertEqual(result['case_id'], test_case_id)
        self.assertIn(result['status'], ['passed', 'failed'])
        self.assertIsNotNone(result['start_time'])
        
    def test_execute_test_suite(self):
        """测试套件执行"""
        test_cases = [
            {'id': 'TEST_001', 'data': {'input': 'value1'}},
            {'id': 'TEST_002', 'data': {'input': 'value2'}}
        ]
        
        results = self.test_executor.execute_test_suite(test_cases)
        
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn(result['status'], ['passed', 'failed'])
            
    def test_save_and_get_result(self):
        """测试结果保存和获取"""
        test_result = {
            'case_id': 'TEST_001',
            'status': 'passed',
            'start_time': datetime.now().isoformat(),
            'end_time': datetime.now().isoformat(),
            'error_message': None
        }
        
        self.result_manager.save_result(test_result)
        retrieved_result = self.result_manager.get_result('TEST_001')
        
        self.assertIsNotNone(retrieved_result)
        self.assertEqual(retrieved_result['case_id'], test_result['case_id'])
        self.assertEqual(retrieved_result['status'], test_result['status'])
        
    def test_save_and_get_suite_results(self):
        """测试套件结果保存和获取"""
        suite_results = [
            {
                'case_id': 'TEST_001',
                'status': 'passed',
                'start_time': datetime.now().isoformat(),
                'end_time': datetime.now().isoformat()
            },
            {
                'case_id': 'TEST_002',
                'status': 'failed',
                'start_time': datetime.now().isoformat(),
                'end_time': datetime.now().isoformat(),
                'error_message': 'Test failed'
            }
        ]
        
        self.result_manager.save_suite_results(suite_results)
        retrieved_results = self.result_manager.get_suite_results('test_suite')
        
        self.assertIsNotNone(retrieved_results)
        self.assertEqual(len(retrieved_results), 2)
        self.assertEqual(retrieved_results[0]['status'], 'passed')
        self.assertEqual(retrieved_results[1]['status'], 'failed')

if __name__ == '__main__':
    unittest.main()