#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from typing import List, Dict
from datetime import datetime
from .test_executor import TestExecutor
from .result_manager import ResultManager
from src.config.yx_config import YxConfig

def main():
    """主程序入口"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("开始执行自动化测试...")
    
    # 初始化测试执行器和结果管理器
    test_executor = TestExecutor()
    result_manager = ResultManager()
    
    # 示例测试用例数据
    test_cases = [
        {
            'id': 'TEST_001',
            'data': {
                'auto_type': '是'
            }
        }
    ]
    
    try:
        # 执行测试套件
        results = test_executor.execute_test_suite(test_cases)
        
        # 保存测试结果
        result_manager.save_suite_results(results)
        
        # 输出测试结果
        for result in results:
            logger.info(f"测试用例 {result['case_id']} 执行{'成功' if result['status'] == 'passed' else '失败'}")
            if result['error_message']:
                logger.error(f"错误信息: {result['error_message']}")
                
    except Exception as e:
        logger.error(f"执行过程中出现错误: {str(e)}")
        raise
        
    finally:
        logger.info("自动化测试执行完成")

if __name__ == '__main__':
    main()