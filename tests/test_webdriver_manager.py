import pytest
from selenium import webdriver
from src.utils.driver.webdriver_manager import WebDriverManager, WebDriverConfig

@pytest.mark.unit
@pytest.mark.webdriver
class TestWebDriverConfig:
    """测试WebDriver配置类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = WebDriverConfig()
        assert config.url == "https://devops.aliyun.com/"
        assert "chrome.exe" in config.chrome_path.lower()
        
    def test_custom_config(self):
        """测试自定义配置"""
        custom_url = "https://custom.url"
        custom_path = "custom/path/chrome.exe"
        config = WebDriverConfig(url=custom_url, chrome_path=custom_path)
        assert config.url == custom_url
        assert config.chrome_path == custom_path
        
    def test_options_setup(self):
        """测试Chrome选项设置"""
        config = WebDriverConfig()
        options = config._setup_options()
        
        # 验证必要的选项是否设置
        arguments = options.arguments
        assert "--disable-gpu" in arguments
        assert "--no-sandbox" in arguments
        assert "--disable-dev-shm-usage" in arguments
        
        # 验证实验性选项
        experimental = options.experimental_options
        assert "excludeSwitches" in experimental
        assert "useAutomationExtension" in experimental
        assert experimental["useAutomationExtension"] is False

@pytest.mark.integration
@pytest.mark.webdriver
class TestWebDriverManager:
    """测试WebDriver管理器"""
    
    def test_init_driver(self):
        """测试初始化WebDriver"""
        manager = WebDriverManager()
        driver = None
        try:
            driver = manager.init_driver()
            assert isinstance(driver, webdriver.Chrome)
            assert driver.current_url == "data:,"  # 新Chrome窗口的默认URL
        finally:
            if driver:
                driver.quit()
                
    def test_quit_driver(self):
        """测试关闭WebDriver"""
        manager = WebDriverManager()
        driver = manager.init_driver()
        assert manager.driver is not None
        
        manager.quit_driver()
        assert manager.driver is None
        
    def test_context_manager(self):
        """测试上下文管理器功能"""
        with WebDriverManager() as driver:
            assert isinstance(driver, webdriver.Chrome)
            assert driver.current_url == "data:," 