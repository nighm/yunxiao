from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

class WebDriverConfig:
    """WebDriver配置类"""
    def __init__(self, url: str = "https://devops.aliyun.com/", chrome_path: str = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"):
        self.url = url
        self.chrome_path = chrome_path
        self.options = self._setup_options()
        
    def _setup_options(self):
        options = Options()
        options.binary_location = self.chrome_path
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        return options

class WebDriverManager:
    """浏览器驱动管理器，负责管理WebDriver实例"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver: Optional[webdriver.Chrome] = None
        
    def init_driver(self) -> webdriver.Chrome:
        """初始化Chrome WebDriver
        
        Returns:
            WebDriver实例
        """
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service("C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")
            service.creation_flags = 0x08000000  # 禁止显示命令行窗口
            
            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            
            self.logger.info('Chrome WebDriver initialized successfully')
            return self.driver
            
        except Exception as e:
            self.logger.error(f'Failed to initialize Chrome WebDriver: {str(e)}')
            raise
            
    def quit_driver(self) -> None:
        """关闭并清理WebDriver实例"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.logger.info('Chrome WebDriver closed successfully')
                
            except Exception as e:
                self.logger.error(f'Failed to close Chrome WebDriver: {str(e)}')
                
    def __enter__(self) -> webdriver.Chrome:
        """支持with语句的上下文管理"""
        return self.init_driver()
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出时自动清理资源"""
        self.quit_driver()