import pytest
from datetime import datetime
from selenium.common.exceptions import WebDriverException
from src.core.automation.test_executor import TestExecutor
from src.utils.helpers import wait_for_condition

@pytest.mark.unit
class TestExecutorUnit:
    """测试执行器单元测试"""
    
    def test_initialization(self):
        """测试执行器初始化"""
        executor = TestExecutor()
        assert hasattr(executor, 'logger')
        assert hasattr(executor, 'test_results')
        assert isinstance(executor.test_results, dict)
        
    def test_cleanup(self):
        """测试清理功能"""
        executor = TestExecutor()
        executor.cleanup()  # 应该不会抛出异常
        
    def test_execute_test_result_format(self, mock_driver):
        """测试执行结果格式"""
        executor = TestExecutor()
        executor.driver = mock_driver
        
        test_case_id = "TEST_001"
        test_data = {"auto_type": "是"}
        
        result = executor.execute_test(test_case_id, test_data)
        
        assert isinstance(result, dict)
        assert "case_id" in result
        assert "status" in result
        assert "start_time" in result
        assert "end_time" in result
        assert "error_message" in result
        
        assert result["case_id"] == test_case_id
        assert result["status"] in ["passed", "failed"]
        assert isinstance(datetime.fromisoformat(result["start_time"]), datetime)
        assert isinstance(datetime.fromisoformat(result["end_time"]), datetime)
        
    def test_result_aggregation(self, mock_driver):
        """测试结果聚合功能"""
        executor = TestExecutor()
        executor.driver = mock_driver
        
        test_cases = [
            {"id": "TEST_001", "data": {"auto_type": "是"}},
            {"id": "TEST_002", "data": {"auto_type": "否"}}
        ]
        
        results = executor.execute_test_suite(test_cases)
        
        assert len(results) == len(test_cases)
        assert all(isinstance(result, dict) for result in results)
        assert all("case_id" in result for result in results)
        assert all("status" in result for result in results)

@pytest.mark.integration
class TestExecutorIntegration:
    """测试执行器集成测试"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, driver):
        """每个测试前后的设置和清理"""
        yield
        try:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
        except:
            pass
    
    def test_setup_test_environment(self):
        """测试环境设置"""
        executor = TestExecutor()
        try:
            executor.setup_test_environment()
            assert hasattr(executor, 'driver')
            assert hasattr(executor, 'driver_manager')
        finally:
            executor.cleanup()
            
    @pytest.mark.slow
    def test_execute_test_suite_workflow(self):
        """测试完整的测试套件执行工作流"""
        executor = TestExecutor()
        test_cases = [
            {
                "id": "TEST_001",
                "data": {"auto_type": "是"}
            },
            {
                "id": "TEST_002",
                "data": {"auto_type": "否"}
            }
        ]
        
        try:
            # 1. 设置测试环境
            executor.setup_test_environment()
            
            # 2. 执行测试套件
            results = executor.execute_test_suite(test_cases)
            
            # 3. 验证结果
            assert isinstance(results, list)
            assert len(results) == len(test_cases)
            
            for result in results:
                assert isinstance(result, dict)
                assert "case_id" in result
                assert "status" in result
                assert "start_time" in result
                assert "end_time" in result
                
            # 4. 验证测试结果已保存
            assert len(executor.test_results) == len(test_cases)
            
        except Exception as e:
            pytest.fail(f"测试套件执行失败: {str(e)}")
            
        finally:
            executor.cleanup()
            
    def test_parallel_execution(self):
        """测试并行执行功能"""
        executor1 = TestExecutor()
        executor2 = TestExecutor()
        
        test_case = {
            "id": "TEST_001",
            "data": {"auto_type": "是"}
        }
        
        try:
            # 1. 设置测试环境
            executor1.setup_test_environment()
            executor2.setup_test_environment()
            
            # 2. 并行执行测试
            result1 = executor1.execute_test(test_case["id"], test_case["data"])
            result2 = executor2.execute_test(test_case["id"], test_case["data"])
            
            # 3. 验证结果
            assert result1["case_id"] == result2["case_id"]
            assert isinstance(result1["start_time"], str)
            assert isinstance(result2["start_time"], str)
            
        finally:
            executor1.cleanup()
            executor2.cleanup()
            
    def test_error_recovery(self):
        """测试错误恢复功能"""
        executor = TestExecutor()
        test_cases = [
            {
                "id": "INVALID_TEST",  # 无效的测试用例ID
                "data": {}
            },
            {
                "id": "TEST_001",  # 有效的测试用例ID
                "data": {"auto_type": "是"}
            }
        ]
        
        try:
            # 1. 设置测试环境
            executor.setup_test_environment()
            
            # 2. 执行测试套件
            results = executor.execute_test_suite(test_cases)
            
            # 3. 验证结果
            assert len(results) == len(test_cases)
            
            # 第一个用例应该失败
            assert results[0]["status"] == "failed"
            assert results[0]["error_message"] is not None
            
            # 第二个用例应该能够正常执行
            assert results[1]["status"] in ["passed", "failed"]
            
        finally:
            executor.cleanup()
            
    def test_resource_cleanup(self):
        """测试资源清理功能"""
        executor = TestExecutor()
        
        try:
            # 1. 设置测试环境
            executor.setup_test_environment()
            assert hasattr(executor, 'driver')
            
            # 2. 模拟异常情况
            def simulate_error():
                raise WebDriverException("模拟的WebDriver异常")
                
            try:
                simulate_error()
            except:
                pass
                
            # 3. 清理资源
            executor.cleanup()
            
            # 4. 验证资源已清理
            assert not hasattr(executor, 'driver') or executor.driver is None
            
        except Exception as e:
            pytest.fail(f"资源清理测试失败: {str(e)}")
            
    @pytest.mark.parametrize("test_data", [
        {"case_id": "TEST_001", "auto_type": "是", "expected_status": "passed"},
        {"case_id": "TEST_002", "auto_type": "否", "expected_status": "passed"},
        {"case_id": "INVALID_TEST", "auto_type": "是", "expected_status": "failed"}
    ])
    def test_different_test_scenarios(self, test_data):
        """测试不同场景的测试用例执行"""
        executor = TestExecutor()
        
        try:
            # 1. 设置测试环境
            executor.setup_test_environment()
            
            # 2. 执行测试
            result = executor.execute_test(test_data["case_id"], {"auto_type": test_data["auto_type"]})
            
            # 3. 验证结果
            assert result["case_id"] == test_data["case_id"]
            assert result["status"] == test_data["expected_status"]
            
        finally:
            executor.cleanup() 