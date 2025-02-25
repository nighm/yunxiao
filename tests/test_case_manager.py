import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    ElementClickInterceptedException,
    WebDriverException
)
from src.core.test_case.case_manager import TestCaseManager
from src.utils.helpers import wait_for_condition

@pytest.mark.unit
@pytest.mark.case_management
class TestCaseManagerUnit:
    """测试用例管理器单元测试"""
    
    def test_initialization(self, mock_driver, **kwargs):
        """测试初始化"""
        manager = TestCaseManager(mock_driver)
        assert manager is not None
        assert manager.driver == mock_driver

    def test_get_element_existance(self, mock_driver):
        """测试元素存在性检查"""
        manager = TestCaseManager(mock_driver)
        try:
            result = manager.get_element_existance()
            assert isinstance(result, bool)
        except WebDriverException as e:
            pytest.fail(f"测试元素存在性检查失败: {str(e)}")

    def test_mark_auto_type_success(self, mock_driver):
        """测试标记自动化类型成功"""
        try:
            manager = TestCaseManager(mock_driver)
            manager.mark_auto_type("TEST-001", "是")
        except WebDriverException as e:
            pytest.fail(f"标记自动化类型失败: {str(e)}")

    def test_mark_auto_type_failure(self, mock_driver):
        """测试标记自动化类型失败"""
        try:
            manager = TestCaseManager(mock_driver)
            with pytest.raises(NoSuchElementException):
                manager.mark_auto_type("INVALID-001", "是")
        except WebDriverException as e:
            pytest.fail(f"测试标记自动化类型失败场景失败: {str(e)}")

    def test_mark_test_result_success(self, mock_driver):
        """测试标记测试结果成功"""
        try:
            manager = TestCaseManager(mock_driver)
            manager.mark_test_result("TEST-001", "PASS")
        except WebDriverException as e:
            pytest.fail(f"标记测试结果失败: {str(e)}")

    def test_mark_test_result_failure(self, mock_driver):
        """测试标记测试结果失败"""
        try:
            manager = TestCaseManager(mock_driver)
            with pytest.raises(NoSuchElementException):
                manager.mark_test_result("INVALID-001", "PASS")
        except WebDriverException as e:
            pytest.fail(f"测试标记测试结果失败场景失败: {str(e)}")

    def test_set_test_user_success(self, mock_driver):
        """测试设置测试执行人成功"""
        try:
            manager = TestCaseManager(mock_driver)
            manager._set_test_user("tester")
        except WebDriverException as e:
            pytest.fail(f"设置测试执行人失败: {str(e)}")

    def test_set_test_user_failure(self, mock_driver):
        """测试设置测试执行人失败"""
        try:
            manager = TestCaseManager(mock_driver)
            with pytest.raises(NoSuchElementException):
                manager._set_test_user("invalid_user")
        except WebDriverException as e:
            pytest.fail(f"测试设置测试执行人失败场景失败: {str(e)}")

    def test_get_element_exist(self, mock_driver):
        """测试元素存在性检查"""
        manager = TestCaseManager(mock_driver)
        test_xpath = "//test/xpath"
        
        # 模拟元素存在
        def mock_find_element(*args, **kwargs):
            if args[1] == test_xpath:
                return True
            return None
        mock_driver.find_element = mock_find_element
        
        assert manager.get_element_exist(test_xpath) is True
        
    def test_element_not_exist(self, mock_driver):
        """测试元素不存在的情况"""
        manager = TestCaseManager(mock_driver)
        test_xpath = "//nonexistent/element"
        
        def mock_find_element(*args, **kwargs):
            raise NoSuchElementException("Element not found")
        mock_driver.find_element = mock_find_element
        
        assert manager.get_element_exist(test_xpath) is False

@pytest.mark.integration
@pytest.mark.case_management
class TestCaseManagerIntegration:
    """测试用例管理器集成测试"""
    
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
    
    @pytest.mark.login
    def test_initialization_and_login(self, driver):
        """测试初始化和登录流程"""
        try:
            manager = TestCaseManager(driver)
            
            # 验证是否成功导航到测试用例页面
            assert "testcase" in driver.current_url.lower()
            
            # 验证登录状态
            def check_login():
                try:
                    # 检查是否存在用户信息元素
                    return len(driver.find_elements(By.XPATH, '//*[contains(@class, "user-info")]')) > 0
                except:
                    return False
                    
            assert wait_for_condition(check_login, timeout=10.0)
            
        except Exception as e:
            pytest.fail(f"初始化或登录失败: {str(e)}")
            
    @pytest.mark.slow
    def test_mark_auto_type_workflow(self, driver):
        """测试完整的标记自动化类型工作流"""
        manager = TestCaseManager(driver)
        test_case_id = "TEST_001"
        
        try:
            # 1. 标记为自动化用例
            manager.mark_auto_type(test_case_id, "是")
            
            # 2. 验证标记结果
            def verify_auto_type(expected_type):
                try:
                    element = driver.find_element(By.XPATH, 
                        f'//td[contains(text(), "{test_case_id}")]/following-sibling::td[contains(@class, "auto-type")]')
                    return element.text.strip() == expected_type
                except:
                    return False
                    
            assert wait_for_condition(lambda: verify_auto_type("是"), timeout=10.0)
            
            # 3. 改回非自动化用例
            manager.mark_auto_type(test_case_id, "否")
            assert wait_for_condition(lambda: verify_auto_type("否"), timeout=10.0)
            
        except Exception as e:
            pytest.fail(f"自动化类型标记工作流失败: {str(e)}")
            
    @pytest.mark.slow
    def test_mark_test_result_workflow(self, driver):
        """测试完整的标记测试结果工作流"""
        manager = TestCaseManager(driver)
        test_case_id = "TEST_001"
        test_user = "测试用户"
        
        try:
            # 1. 标记为通过
            manager.mark_test_result(test_case_id, "PASS", test_user)
            
            # 2. 验证结果状态
            def verify_test_result(expected_status):
                try:
                    element = driver.find_element(By.XPATH,
                        f'//td[contains(text(), "{test_case_id}")]/following-sibling::td[contains(@class, "status")]')
                    return expected_status in element.text.lower()
                except:
                    return False
                    
            assert wait_for_condition(lambda: verify_test_result("pass"), timeout=10.0)
            
            # 3. 验证执行人
            def verify_test_user():
                try:
                    element = driver.find_element(By.XPATH,
                        f'//td[contains(text(), "{test_case_id}")]/following-sibling::td[contains(@class, "executor")]')
                    return test_user in element.text
                except:
                    return False
                    
            assert wait_for_condition(verify_test_user, timeout=10.0)
            
            # 4. 标记为失败
            manager.mark_test_result(test_case_id, "FAIL", test_user)
            assert wait_for_condition(lambda: verify_test_result("fail"), timeout=10.0)
            
        except Exception as e:
            pytest.fail(f"测试结果标记工作流失败: {str(e)}")
            
    def test_filter_and_search(self, driver):
        """测试筛选和搜索功能"""
        manager = TestCaseManager(driver)
        search_text = "TEST_"
        
        try:
            # 1. 点击筛选按钮
            filter_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "filter-button")]'))
            )
            filter_button.click()
            
            # 2. 输入搜索文本
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@placeholder, "搜索")]'))
            )
            search_input.clear()
            search_input.send_keys(search_text)
            
            # 3. 点击搜索按钮
            search_button = driver.find_element(By.XPATH, '//*[text()="搜索"]')
            search_button.click()
            
            # 4. 验证搜索结果
            def verify_search_results():
                try:
                    elements = driver.find_elements(By.XPATH, f'//td[contains(text(), "{search_text}")]')
                    return len(elements) > 0
                except:
                    return False
                    
            assert wait_for_condition(verify_search_results, timeout=10.0)
            
        except Exception as e:
            pytest.fail(f"筛选和搜索功能测试失败: {str(e)}")
            
    @pytest.mark.parametrize("test_data", [
        {"case_id": "TEST_001", "auto_type": "是", "result": "PASS"},
        {"case_id": "TEST_002", "auto_type": "否", "result": "FAIL"},
        {"case_id": "TEST_003", "auto_type": "是", "result": "暂缓"}
    ])
    def test_batch_operations(self, driver, test_data):
        """测试批量操作功能"""
        manager = TestCaseManager(driver)
        
        try:
            # 1. 标记自动化类型
            manager.mark_auto_type(test_data["case_id"], test_data["auto_type"])
            
            # 2. 标记测试结果
            manager.mark_test_result(test_data["case_id"], test_data["result"], "测试用户")
            
            # 3. 验证操作结果
            def verify_case_status():
                try:
                    auto_type_element = driver.find_element(By.XPATH,
                        f'//td[contains(text(), "{test_data["case_id"]}")]/following-sibling::td[contains(@class, "auto-type")]')
                    result_element = driver.find_element(By.XPATH,
                        f'//td[contains(text(), "{test_data["case_id"]}")]/following-sibling::td[contains(@class, "status")]')
                        
                    return (test_data["auto_type"] in auto_type_element.text and
                            test_data["result"].lower() in result_element.text.lower())
                except:
                    return False
                    
            assert wait_for_condition(verify_case_status, timeout=10.0)
            
        except Exception as e:
            pytest.fail(f"批量操作测试失败: {str(e)}")
            
    def test_error_handling(self, driver):
        """测试错误处理"""
        manager = TestCaseManager(driver)
        
        # 1. 测试无效的用例ID
        with pytest.raises(Exception):
            manager.mark_auto_type("INVALID_ID", "是")
            
        # 2. 测试无效的自动化类型
        with pytest.raises(ValueError):
            manager.mark_auto_type("TEST_001", "无效类型")
            
        # 3. 测试无效的测试结果
        with pytest.raises(ValueError):
            manager.mark_test_result("TEST_001", "无效结果", "测试用户") 