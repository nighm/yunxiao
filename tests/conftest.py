import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.utils.driver.webdriver_manager import WebDriverManager
from src.config.yx_config import YxConfig

@pytest.fixture(scope="session")
def config():
    """返回配置对象"""
    return YxConfig

@pytest.fixture(scope="function")
def driver():
    """提供WebDriver实例"""
    manager = WebDriverManager()
    driver = manager.init_driver()
    yield driver
    manager.quit_driver()

@pytest.fixture(scope="function")
def mock_driver():
    """提供模拟的WebDriver实例，用于单元测试"""
    class MockDriver:
        def __init__(self):
            self.current_url = None
            self.page_source = ""
            
        def get(self, url):
            self.current_url = url
            
        def quit(self):
            pass
            
        def find_element(self, by, value):
            return None
            
        def implicitly_wait(self, time):
            pass
    
    return MockDriver() 