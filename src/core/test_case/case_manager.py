# 云效自动化测试项目 - 测试用例管理模块实现

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException,
    NoSuchWindowException,
    WebDriverException
)
import time
import re
import openpyxl
from openpyxl import Workbook
import logging
from src.config.yx_config import YxConfig

class TestCaseManager:
    """测试用例管理类，处理用例相关的所有功能"""

    def __init__(self, driver):
        """初始化测试用例管理类
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.element_existance = False
        self.element_exist = False
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(self.driver, 30)  # 创建一个全局的WebDriverWait对象
        self.max_retries = 3  # 最大重试次数
        
        # 导航到登录页面
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self._perform_login()
                break
            except NoSuchWindowException as e:
                retry_count += 1
                self.logger.warning(f"浏览器窗口已关闭，正在重试 ({retry_count}/{self.max_retries})")
                if retry_count >= self.max_retries:
                    raise Exception(f"登录失败，超过最大重试次数: {str(e)}")
                # 重新创建浏览器窗口
                self.driver.quit()
                from src.utils.driver.webdriver_manager import WebDriverManager
                self.driver = WebDriverManager().get_driver()
                self.wait = WebDriverWait(self.driver, 30)
            except WebDriverException as e:
                retry_count += 1
                self.logger.warning(f"WebDriver异常，正在重试 ({retry_count}/{self.max_retries})")
                if retry_count >= self.max_retries:
                    raise Exception(f"登录失败，超过最大重试次数: {str(e)}")
                time.sleep(2)  # 短暂等待后重试
                
    def _perform_login(self):
        """执行登录操作"""
        self.logger.info("正在导航到云效登录页面...")
        self.driver.get("https://devops.aliyun.com/")
        
        # 等待页面加载完成
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.logger.info("页面加载完成")
        
        # 确保窗口最大化
        self.driver.maximize_window()
        
        # 等待并点击登录按钮
        login_button = None
        login_button_selectors = [
            (By.XPATH, "//a[contains(text(), '登录')]"),
            (By.XPATH, "//button[contains(text(), '登录')]"),
            (By.XPATH, "//*[contains(@class, 'login')]"),
            (By.XPATH, "//*[contains(@href, 'login')]"),
            (By.CSS_SELECTOR, "[data-spm-click*='login']")
        ]
        
        for selector in login_button_selectors:
            try:
                login_button = self.wait.until(
                    EC.element_to_be_clickable(selector)
                )
                self.logger.info(f"找到登录按钮: {selector}")
                break
            except TimeoutException:
                continue
                
        if not login_button:
            raise Exception("无法找到登录按钮")
            
        # 点击登录按钮
        try:
            login_button.click()
            self.logger.info("点击登录按钮成功")
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", login_button)
            self.logger.info("通过JavaScript点击登录按钮成功")
        
        # 等待登录框出现
        self.logger.info("等待登录框加载...")
        login_frame = None
        try:
            # 等待iframe出现
            login_frame = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[id^='alibaba-login-box']"))
            )
            self.driver.switch_to.frame(login_frame)
            self.logger.info("成功切换到登录框iframe")
        except TimeoutException:
            self.logger.warning("未找到登录iframe，尝试直接定位登录表单")
        
        # 等待用户名输入框
        username_selectors = [
            (By.ID, "fm-login-id"),
            (By.NAME, "fm-login-id"),
            (By.CSS_SELECTOR, "input[type='text']"),
            (By.XPATH, "//input[@placeholder='账号']"),
            (By.XPATH, "//input[contains(@placeholder, '用户名')]")
        ]
        
        username_input = None
        for selector in username_selectors:
            try:
                username_input = self.wait.until(
                    EC.presence_of_element_located(selector)
                )
                self.logger.info(f"找到用户名输入框: {selector}")
                break
            except TimeoutException:
                continue
                
        if not username_input:
            raise Exception("无法找到用户名输入框")
        
        # 等待密码输入框
        password_selectors = [
            (By.ID, "fm-login-password"),
            (By.NAME, "fm-login-password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.XPATH, "//input[@placeholder='密码']")
        ]
        
        password_input = None
        for selector in password_selectors:
            try:
                password_input = self.wait.until(
                    EC.presence_of_element_located(selector)
                )
                self.logger.info(f"找到密码输入框: {selector}")
                break
            except TimeoutException:
                continue
                
        if not password_input:
            raise Exception("无法找到密码输入框")
        
        # 输入登录信息
        self.logger.info("输入登录信息...")
        username_input.clear()
        username_input.send_keys(YxConfig.userName)
        password_input.clear()
        password_input.send_keys(YxConfig.password)
        
        # 点击登录按钮
        self.logger.info("点击登录提交按钮...")
        login_submit_selectors = [
            (By.CLASS_NAME, "password-login"),
            (By.XPATH, "//button[contains(text(), '登录')]"),
            (By.XPATH, "//input[@type='submit']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "[data-spm-click*='submit']")
        ]
        
        login_submit = None
        for selector in login_submit_selectors:
            try:
                login_submit = self.wait.until(
                    EC.element_to_be_clickable(selector)
                )
                self.logger.info(f"找到登录提交按钮: {selector}")
                break
            except TimeoutException:
                continue
                
        if not login_submit:
            raise Exception("无法找到登录提交按钮")
            
        login_submit.click()
        
        # 等待登录成功
        self.logger.info("等待登录完成...")
        try:
            # 等待用户头像或个人信息元素出现
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info, .avatar, [data-spm-click*='profile']"))
            )
            self.logger.info("登录成功")
        except TimeoutException:
            raise Exception("登录可能失败，未检测到用户信息元素")
        
        # 如果在iframe中，切回主文档
        try:
            self.driver.switch_to.default_content()
        except:
            pass
        
        # 导航到测试用例页面
        self.logger.info("正在导航到测试用例页面...")
        self.driver.get("https://devops.aliyun.com/testcase")
        
        # 等待测试用例页面加载
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "main, .test-case-list, [data-spm-click*='testcase']"))
        )
        
        self.logger.info("测试用例页面加载完成")

    def get_element_existance(self):
        """判断用例是否存在
        
        Returns:
            bool: 是否存在用例
        """
        try:
            self.driver.find_element(By.XPATH, '//*[text()="暂无内容"]')
            print('未找到用例')
            self.element_existance = True
        except:
            print('有用例')
            self.element_existance = False
        return self.element_existance

    def get_element_exist(self, xpath):
        """判断元素是否存在
        
        Args:
            xpath: 要检查的元素的xpath
            
        Returns:
            bool: 元素是否存在
        """
        try:
            self.driver.find_element(By.XPATH, xpath)
            print('有元素')
            self.element_exist = True
        except:
            print('无元素')
            self.element_exist = False
        return self.element_exist

    def _wait_for_page_load(self):
        """等待页面加载完成"""
        self.driver.implicitly_wait(20)  # 增加隐式等待时间
        
        try:
            # 首先等待 main 元素
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
            )
            
            # 然后等待更具体的元素
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container"]//table | //*[contains(@class, "filter-button")]'))
            )
            
            # 确保页面完全加载
            time.sleep(2)
            
        except Exception as e:
            self.logger.error(f"页面加载超时: {str(e)}")
            raise

    def _find_and_click_filter_button(self):
        """查找并点击筛选按钮"""
        filter_button = None
        selectors = [
            '//button[contains(., "筛选")]',
            '//button[contains(., "过滤")]',
            '//button[contains(@class, "filter")]',
            '//*[@id="container"]//button[contains(@class, "filter")]',
            '//main//button[contains(@class, "filter")]',
            '/html/body/div[2]/main/header/section/section/section/span[2]/button',
            '/html/body/div[3]/main/header/section/section/section/span[2]/button'
        ]
        
        for selector in selectors:
            try:
                filter_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                self.logger.info(f"找到筛选按钮: {selector}")
                break
            except:
                continue
                
        if not filter_button:
            self.logger.error("无法找到筛选按钮")
            raise Exception("无法找到筛选按钮")
            
        try:
            filter_button.click()
            self.logger.info("成功点击筛选按钮")
        except Exception as e:
            self.logger.error(f"点击筛选按钮失败: {str(e)}")
            # 尝试使用JavaScript点击
            self.driver.execute_script("arguments[0].click();", filter_button)
            self.logger.info("使用JavaScript成功点击筛选按钮")
        
        time.sleep(1)

    def _input_case_id(self, case_id):
        """输入用例ID"""
        try:
            case_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "测试用例编号")]/../../..//input'))
            )
            self.logger.info("找到用例编号输入框")
        except Exception as e:
            self.logger.error("无法找到用例编号输入框")
            raise

        case_input.send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        case_input.send_keys(Keys.DELETE)
        time.sleep(0.5)
        case_input.send_keys(case_id)
        time.sleep(0.5)

    def _click_filter_submit(self):
        """点击过滤按钮"""
        try:
            filter_submit = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[text()="过滤"]/./.. | //*[contains(@class, "filter-submit")]'))
            )
            filter_submit.click()
            self.logger.info("点击过滤按钮")
        except Exception as e:
            self.logger.error(f"点击过滤按钮失败: {str(e)}")
            raise
            
        time.sleep(2)

    def _select_case_and_set_type(self, case_type):
        """选择用例并设置自动化类型"""
        if not self.get_element_existance():
            # 选择用例
            try:
                case_row = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]//table//tbody/tr[1]'))
                )
                case_row.click()
                self.logger.info("选择用例成功")
            except Exception as e:
                self.logger.error("选择用例失败")
                raise
                
            time.sleep(1.5)

            # 点击自动化类型下拉菜单
            try:
                auto_type = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="workitemAttachment"]/../div[1]/div/div[8]/div[2]'))
                )
                auto_type.click()
                self.logger.info("点击自动化类型下拉菜单")
            except Exception as e:
                self.logger.error("点击自动化类型下拉菜单失败")
                raise
                
            time.sleep(1)

            # 选择自动化类型
            try:
                if case_type.strip() == '是':
                    self.driver.find_element(By.XPATH, '//span[text()="是"]/./..').click()
                elif case_type.strip() == '否':
                    self.driver.find_element(By.XPATH, '//span[text()="否"]/./..').click()
                self.logger.info(f"选择自动化类型: {case_type}")
            except Exception as e:
                self.logger.error(f"选择自动化类型失败: {case_type}")
                raise
                
            time.sleep(1.5)

    def mark_auto_type(self, case_id, case_type):
        """标记用例自动化类型
        
        Args:
            case_id: 用例ID
            case_type: 自动化类型（'是'或'否'）
        """
        self._wait_for_page_load()
        self._find_and_click_filter_button()
        self._input_case_id(case_id)
        self._click_filter_submit()
        self._select_case_and_set_type(case_type)

    def _wait_for_filter_button(self):
        """等待并点击筛选按钮"""
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "filter-button") or contains(@class, "filter")]'))
        )
        
        try:
            # 首先尝试通过文本内容定位
            filter_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "筛选") or contains(text(), "过滤")]'))
            )
            filter_button.click()
        except:
            # 如果找不到，尝试其他可能的定位方式
            try:
                filter_button = self.driver.find_element(By.XPATH,
                    '/html/body/div[2]/main/header/section/section/section/span[2]/button')
            except:
                filter_button = self.driver.find_element(By.XPATH,
                    '/html/body/div[3]/main/header/section/section/section/span[2]/button')
            filter_button.click()

        # 等待过滤按钮出现
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="过滤"]')))

    def _input_case_id_for_result(self, case_id):
        """输入用例ID进行结果标记"""
        case_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="测试用例编号"]/./../../span/input'))
        )

        case_input.send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        case_input.send_keys(Keys.DELETE)
        time.sleep(0.5)
        case_input.send_keys(case_id)
        time.sleep(0.5)

    def _wait_for_results_list(self):
        """等待结果列表加载"""
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, 
                '//*[@id="container"]/main/section/section[2]/section/div/div[2]/div[2]/div/div/div[2]/div')))

    def _select_test_result(self, result):
        """选择测试结果"""
        # 等待并获取当前状态
        status_cell = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                '//*[@id="container"]//table//tbody/tr[1]/td[7]'))
        )
        status = status_cell.text

        if status == '待测试':
            # 点击状态下拉菜单
            status_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="container"]//table//tbody/tr[1]/td[7]//button'))
            )
            status_dropdown.click()

            # 等待选项出现
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[text()="已通过"]')))

            # 选择测试结果
            if result.strip() == 'PASS':
                self.driver.find_element(By.XPATH, '//*[text()="已通过"]').click()
            elif result.strip() == 'FAIL':
                self.driver.find_element(By.XPATH, '//*[text()="未通过"]').click()
            else:
                self.driver.find_element(By.XPATH, '//*[text()="暂缓"]').click()
            time.sleep(0.5)

    def mark_test_result(self, case_id, result, test_user=None):
        """标记测试结果
        
        Args:
            case_id: 用例ID
            result: 测试结果（'PASS'/'FAIL'/'暂缓'）
            test_user: 测试执行人
        """
        self._wait_for_filter_button()
        self._input_case_id_for_result(case_id)
        self._click_filter_submit()
        self._wait_for_results_list()

        if not self.get_element_existance():
            self._select_test_result(result)
            if test_user:
                self._set_test_user(test_user)

    def _set_test_user(self, test_user):
        """设置测试执行人
        
        Args:
            test_user: 测试执行人姓名
        """
        try:
            # 等待并点击选择用例
            case_row = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="container"]//table//tbody/tr[1]'))
            )
            case_row.click()
        except:
            # 如果第一种方式失败，尝试备用方式
            case_row = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    '//table//tbody/tr[1]'))
            )
            case_row.click()

        # 等待页面元素加载
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="前置条件"]')))

        # 等待并获取当前执行人
        current_user_elem = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                '//*[@id="workitemAttachment"]/../div[2]/div[2]/div[2]/div/div/span/span[1]/span[1]/em'))
        )
        current_user = current_user_elem.text

        # 如果当前执行人不是目标执行人，则修改
        if current_user != test_user:
            # 点击修改执行人按钮
            change_user_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="workitemAttachment"]/../div[2]/div[2]/div[2]/div/div/span/span[1]/span[2]'))
            )
            change_user_btn.click()

            # 等待搜索框出现
            search_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@placeholder="请输入关键字"]'))
            )

            # 输入执行人姓名
            search_input.send_keys(test_user)

            # 等待用户列表加载
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="uiless-member-mini-v2-members"]'))
            )
            time.sleep(1)

            # 获取用户列表
            user_list_elem = self.driver.find_element(By.XPATH, '//*[@class="uiless-member-mini-v2-members"]')
            user_list = user_list_elem.text

            # 选择执行人
            if test_user in user_list:
                user_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH,
                        f'//*[contains(@class, "uiless-member-mini-v2-members")]//div[contains(text(), "{test_user}")]'))
                )
                user_option.click()
            else:
                # 如果找不到用户，关闭选择框
                close_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH,
                        '//*[@id="workitemAttachment"]/../div[2]/div[2]/div[2]/div/div/span/span[1]/span[2]'))
                )
                close_btn.click()

        # 等待并点击收起用例详情
        close_detail = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="drawer-sidebar-workitemDetail"]/../div'))
        )
        close_detail.click()
        time.sleep(1)