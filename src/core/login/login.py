from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from src.utils.driver.webdriver_manager import WebDriverManager, WebDriverConfig
import time
import random
import logging

class LoginManager:
    """登录管理器，负责处理云效平台的登录相关操作"""
    
    def __init__(self, username, password):
        self.logger = logging.getLogger(__name__)
        self.username = username
        self.password = password
        self.config = WebDriverConfig('https://devops.aliyun.com/workbench?orgId=63e607799dee9309492bc382')
        self.driver_manager = WebDriverManager(self.config)
        self.driver = None
        
    def initialize_driver(self):
        """初始化WebDriver"""
        try:
            self.driver = self.driver_manager.init_driver()
            self.driver.implicitly_wait(1.5)
            return True
        except Exception as e:
            self.logger.error(f'初始化WebDriver失败: {str(e)}')
            return False
            
    def login(self):
        """执行登录操作"""
        try:
            if not self.driver:
                if not self.initialize_driver():
                    return False
                    
            self.driver.get(self.config.url)
            self.driver.maximize_window()
            
            # 防检测
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
            })
            
            # 等待并切换到登录框架
            time.sleep(2)
            self.driver.switch_to.frame("alibaba-login-box")
            
            # 输入登录信息
            self.driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(self.username)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(self.password)
            time.sleep(1)
            
            # 点击登录按钮
            try:
                self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[5]/button').click()
            except:
                self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[6]/button').click()
            
            # 处理滑块验证
            if self.handle_slide_verification():
                return self.wait_for_login_success()
            return False
            
        except Exception as e:
            self.logger.error(f'登录失败: {str(e)}')
            return False
            
    def handle_slide_verification(self):
        """处理滑块验证"""
        try:
            time.sleep(2)
            # 检查是否存在滑块
            try:
                self.driver.find_element(By.ID, 'baxia-dialog-content')
                self.logger.info('检测到滑块验证')
            except:
                self.logger.info('无需滑块验证')
                return True
                
            # 切换到滑块框架
            self.driver.switch_to.frame("baxia-dialog-content")
            
            # 处理滑块
            for _ in range(5):
                try:
                    button = self.driver.find_element(By.XPATH, '//*[@aria-label="滑块"]')
                    action = ActionChains(self.driver)
                    action.click_and_hold(button)
                    
                    # 随机滑动距离
                    count = random.randint(110, 120)
                    for _ in range(5):
                        action.move_by_offset(count, 0).perform()
                        time.sleep(0.3)
                    action.release()
                    time.sleep(2)
                    
                    # 检查是否需要重试
                    try:
                        self.driver.find_element(By.XPATH, '//*[contains(text(),"验证失败，点击框体重试")]')
                        continue
                    except:
                        return True
                        
                except Exception as e:
                    self.logger.error(f'滑块验证失败: {str(e)}')
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f'处理滑块验证失败: {str(e)}')
            return False
            
    def wait_for_login_success(self):
        """等待登录成功"""
        for i in range(15):
            try:
                self.driver.find_element(By.XPATH, '//*[text()="云效 工作台"]')
                self.logger.info('登录成功')
                return True
            except:
                if i == 14:
                    self.logger.error('登录超时')
                    return False
                time.sleep(1)
                
    def quit(self):
        """退出浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info('浏览器已关闭')
            except Exception as e:
                self.logger.error(f'关闭浏览器失败: {str(e)}')