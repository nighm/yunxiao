import pytest
import time
from src.utils.helpers import retry, wait_for_condition, safe_get_attribute, format_error

@pytest.mark.unit
class TestHelpers:
    """工具函数测试"""
    
    def test_retry_success(self):
        """测试重试装饰器 - 成功场景"""
        counter = 0
        
        @retry(max_attempts=3, delay=0.1)
        def test_function():
            nonlocal counter
            counter += 1
            if counter < 2:
                raise ValueError("测试错误")
            return "success"
            
        result = test_function()
        assert result == "success"
        assert counter == 2
        
    def test_retry_failure(self):
        """测试重试装饰器 - 失败场景"""
        @retry(max_attempts=2, delay=0.1)
        def test_function():
            raise ValueError("测试错误")
            
        with pytest.raises(ValueError):
            test_function()
            
    def test_wait_for_condition_success(self):
        """测试条件等待 - 成功场景"""
        counter = 0
        
        def condition():
            nonlocal counter
            counter += 1
            return counter >= 3
            
        result = wait_for_condition(condition, timeout=1.0, interval=0.1)
        assert result is True
        assert counter >= 3
        
    def test_wait_for_condition_timeout(self):
        """测试条件等待 - 超时场景"""
        def condition():
            return False
            
        result = wait_for_condition(condition, timeout=0.5, interval=0.1)
        assert result is False
        
    def test_safe_get_attribute_exists(self):
        """测试安全获取属性 - 属性存在"""
        class TestClass:
            def __init__(self):
                self.test_attr = "test"
                
        obj = TestClass()
        result = safe_get_attribute(obj, "test_attr", "default")
        assert result == "test"
        
    def test_safe_get_attribute_not_exists(self):
        """测试安全获取属性 - 属性不存在"""
        class TestClass:
            pass
            
        obj = TestClass()
        result = safe_get_attribute(obj, "non_existent", "default")
        assert result == "default"
        
    def test_format_error(self):
        """测试错误信息格式化"""
        try:
            raise ValueError("测试错误")
        except Exception as e:
            result = format_error(e)
            assert result == "ValueError: 测试错误" 