import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)
from src.utils.driver.webdriver_manager import WebDriverManager, WebDriverConfig

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
            self.logger.info('浏览器初始化成功')
            return True
        except WebDriverException as e:
            self.logger.error(f'浏览器初始化失败: {str(e)}')
            return False
            
    def login(self):
        """执行登录操作
        
        Returns:
            bool: 登录是否成功
        """
        try:
            if not self.driver:
                self.logger.info("WebDriver未初始化，正在初始化...")
                if not self.initialize_driver():
                    return False
                    
            self.logger.info("正在导航到登录页面...")
            self.driver.get(self.config.url)
            self.driver.maximize_window()
            
            # 防检测
            try:
                self.logger.debug("正在设置防检测脚本...")
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
                })
            except WebDriverException as e:
                self.logger.warning(f"设置防检测脚本失败，但将继续尝试登录: {str(e)}")
            
            # 等待并切换到登录框架
            self.logger.info("等待登录框架加载...")
            time.sleep(2)
            try:
                self.driver.switch_to.frame("alibaba-login-box")
                self.logger.info("成功切换到登录框架")
            except WebDriverException as e:
                self.logger.error(f"切换到登录框架失败: {str(e)}")
                return False
            
            # 输入登录信息
            try:
                self.logger.info("正在输入用户名...")
                username_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="fm-login-id"]'))
                )
                username_input.clear()
                username_input.send_keys(self.username)
                time.sleep(1)
                
                self.logger.info("正在输入密码...")
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="fm-login-password"]'))
                )
                password_input.clear()
                password_input.send_keys(self.password)
                time.sleep(1)
            except TimeoutException as e:
                self.logger.error(f"等待登录输入框超时: {str(e)}")
                return False
            except WebDriverException as e:
                self.logger.error(f"输入登录信息失败: {str(e)}")
                return False
            
            # 点击登录按钮
            self.logger.info("正在点击登录按钮...")
            try:
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div[5]/button'))
                )
                login_button.click()
            except TimeoutException:
                try:
                    # 尝试备用登录按钮
                    self.logger.info("尝试备用登录按钮...")
                    login_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div[6]/button'))
                    )
                    login_button.click()
                except TimeoutException as e:
                    self.logger.error(f"无法找到登录按钮: {str(e)}")
                    return False
                except WebDriverException as e:
                    self.logger.error(f"点击登录按钮失败: {str(e)}")
                    return False
            
            # 处理滑块验证
            self.logger.info("检查是否需要滑块验证...")
            if self.handle_slide_verification():
                self.logger.info("滑块验证通过，等待登录完成...")
                return self.wait_for_login_success()
            else:
                self.logger.error("滑块验证失败")
                return False
            
        except TimeoutException as e:
            self.logger.error(f"登录过程超时: {str(e)}")
            return False
        except WebDriverException as e:
            self.logger.error(f"登录过程发生错误: {str(e)}")
            return False
        finally:
            try:
                # 确保切回主框架
                self.driver.switch_to.default_content()
            except WebDriverException:
                pass
            
    def _check_slide_verification_exists(self):
        """检查是否存在滑块验证"""
        try:
            self.driver.find_element(By.ID, 'baxia-dialog-content')
            self.logger.info('检测到滑块验证')
            return True
        except NoSuchElementException:
            self.logger.info('无需滑块验证')
            return False

    def _perform_slide_action(self):
        """执行滑块动作"""
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
            return True
        except (NoSuchElementException, ElementNotInteractableException) as e:
            self.logger.error(f'滑块验证失败: {str(e)}')
            return False

    def _check_verification_result(self):
        """检查验证结果"""
        try:
            self.driver.find_element(By.XPATH, '//*[contains(text(),"验证失败，点击框体重试")]')
            return False
        except NoSuchElementException:
            return True

    def handle_slide_verification(self):
        """处理滑块验证
        
        Returns:
            bool: 验证是否成功
        """
        try:
            time.sleep(2)
            if not self._check_slide_verification_exists():
                return True
                
            # 切换到滑块框架
            try:
                self.driver.switch_to.frame("baxia-dialog-content")
                self.logger.info("成功切换到滑块验证框架")
            except WebDriverException as e:
                self.logger.error(f"切换到滑块验证框架失败: {str(e)}")
                return False
            
            # 尝试5次滑块验证
            max_attempts = 5
            for attempt in range(max_attempts):
                self.logger.info(f"开始第 {attempt + 1} 次滑块验证尝试")
                
                if self._perform_slide_action():
                    # 等待验证结果
                    time.sleep(1.5)
                    if self._check_verification_result():
                        self.logger.info(f"第 {attempt + 1} 次滑块验证成功")
                        
                        # 切回主框架
                        try:
                            self.driver.switch_to.default_content()
                        except WebDriverException as e:
                            self.logger.warning(f"切回主框架失败，但验证可能已成功: {str(e)}")
                            
                        return True
                    else:
                        self.logger.warning(f"第 {attempt + 1} 次滑块验证失败，验证结果不通过")
                else:
                    self.logger.warning(f"第 {attempt + 1} 次滑块验证失败，无法执行滑动操作")
                
                # 如果不是最后一次尝试，等待一段时间再重试
                if attempt < max_attempts - 1:
                    time.sleep(2)
            
            self.logger.error(f"滑块验证失败，已尝试 {max_attempts} 次")
            return False
            
        except WebDriverException as e:
            self.logger.error(f"处理滑块验证过程中发生错误: {str(e)}")
            return False
        finally:
            try:
                # 确保最后切回主框架
                self.driver.switch_to.default_content()
            except WebDriverException:
                pass
            
    def wait_for_login_success(self):
        """等待登录成功"""
        for i in range(15):
            try:
                self.driver.find_element(By.XPATH, '//*[text()="云效 工作台"]')
                self.logger.info('登录成功')
                return True
            except NoSuchElementException:
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
            except WebDriverException as e:
                self.logger.error(f'关闭浏览器失败: {str(e)}')