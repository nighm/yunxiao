# 云效自动化测试项目 - 测试用例管理模块实现

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
        
        # 导航到登录页面
        try:
            self.logger.info("正在导航到云效登录页面...")
            self.driver.get("https://devops.aliyun.com/")  # 直接访问云效
            
            # 设置隐式等待
            self.driver.implicitly_wait(20)
            
            # 等待页面加载完成
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 等待登录按钮出现并点击
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '登录')]"))
            )
            login_button.click()
            
            # 等待登录表单加载
            self.logger.info("等待登录表单加载...")
            time.sleep(3)
            
            # 检查并切换到登录 iframe
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                for iframe in iframes:
                    try:
                        self.driver.switch_to.frame(iframe)
                        # 尝试在 iframe 中找到登录元素
                        if len(self.driver.find_elements(By.ID, "alibaba-login-box")) > 0:
                            self.logger.info("找到登录框 iframe")
                            break
                        self.driver.switch_to.default_content()
                    except:
                        self.driver.switch_to.default_content()
                        continue
            
            # 等待用户名输入框
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "fm-login-id"))
            )
            
            # 等待密码输入框
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "fm-login-password"))
            )
            
            # 输入登录信息
            self.logger.info("输入登录信息...")
            username_input.clear()
            username_input.send_keys(YxConfig.userName)
            time.sleep(1)
            password_input.clear()
            password_input.send_keys(YxConfig.password)
            time.sleep(1)
            
            # 点击登录按钮
            self.logger.info("点击登录按钮...")
            login_submit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "password-login"))
            )
            login_submit.click()
            
            # 等待登录完成
            time.sleep(5)
            
            # 导航到测试用例页面
            self.logger.info("正在导航到测试用例页面...")
            self.driver.get("https://devops.aliyun.com/testcase")
            
            # 等待测试用例页面加载
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 等待页面完全渲染
            time.sleep(3)
            
            self.logger.info("页面加载完成")
            
        except Exception as e:
            self.logger.error(f"登录或导航失败: {str(e)}")
            raise

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

    def mark_auto_type(self, case_id, case_type):
        """标记用例自动化类型
        
        Args:
            case_id: 用例ID
            case_type: 自动化类型（'是'或'否'）
        """
        # 等待页面加载完成
        self.driver.implicitly_wait(20)  # 增加隐式等待时间
        
        # 等待页面主要元素加载
        try:
            # 首先等待 main 元素
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "main"))
            )
            
            # 然后等待更具体的元素
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container"]//table | //*[contains(@class, "filter-button")]'))
            )
            
            # 确保页面完全加载
            time.sleep(2)
            
        except Exception as e:
            self.logger.error(f"页面加载超时: {str(e)}")
            raise
            
        # 尝试多种方式定位筛选按钮
        filter_button = None
        for selector in [
            '//button[contains(., "筛选")]',
            '//button[contains(., "过滤")]',
            '//button[contains(@class, "filter")]',
            '//*[@id="container"]//button[contains(@class, "filter")]',
            '//main//button[contains(@class, "filter")]',
            '/html/body/div[2]/main/header/section/section/section/span[2]/button',
            '/html/body/div[3]/main/header/section/section/section/span[2]/button'
        ]:
            try:
                filter_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                self.logger.info(f"找到筛选按钮: {selector}")
                break
            except:
                continue
                
        if not filter_button:
            self.logger.error("无法找到筛选按钮")
            raise Exception("无法找到筛选按钮")
            
        # 点击筛选按钮
        try:
            filter_button.click()
            self.logger.info("成功点击筛选按钮")
        except Exception as e:
            self.logger.error(f"点击筛选按钮失败: {str(e)}")
            # 尝试使用JavaScript点击
            self.driver.execute_script("arguments[0].click();", filter_button)
            self.logger.info("使用JavaScript成功点击筛选按钮")
            
        time.sleep(1)

        # 等待输入框出现
        try:
            case_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "测试用例编号")]/../../..//input'))
            )
            self.logger.info("找到用例编号输入框")
        except Exception as e:
            self.logger.error("无法找到用例编号输入框")
            raise

        # 输入用例ID
        case_input.send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        case_input.send_keys(Keys.DELETE)
        time.sleep(0.5)
        case_input.send_keys(case_id)
        time.sleep(0.5)
        self.logger.info(f"输入用例编号: {case_id}")

        # 点击过滤
        try:
            filter_submit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[text()="过滤"]/./.. | //*[contains(@class, "filter-submit")]'))
            )
            filter_submit.click()
            self.logger.info("点击过滤按钮")
        except Exception as e:
            self.logger.error(f"点击过滤按钮失败: {str(e)}")
            raise
            
        time.sleep(2)

        if not self.get_element_existance():
            # 等待并点击选择用例
            try:
                case_row = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]//table//tbody/tr[1]'))
                )
                case_row.click()
                self.logger.info("选择用例成功")
            except Exception as e:
                self.logger.error("选择用例失败")
                raise
                
            time.sleep(1.5)

            # 等待并点击自动化类型下拉菜单
            try:
                auto_type = WebDriverWait(self.driver, 10).until(
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

    def mark_test_result(self, case_id, result, test_user=None):
        """标记测试结果
        
        Args:
            case_id: 用例ID
            result: 测试结果（'PASS'/'FAIL'/'暂缓'）
            test_user: 测试执行人
        """
        # 等待页面加载完成
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "filter-button") or contains(@class, "filter")]'))
        )
        
        # 点击筛选
        try:
            # 首先尝试通过文本内容定位
            filter_button = WebDriverWait(self.driver, 5).until(
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
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="过滤"]')))

        # 等待并定位用例ID输入框
        case_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="测试用例编号"]/./../../span/input'))
        )

        # 输入用例ID
        case_input.send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        case_input.send_keys(Keys.DELETE)
        time.sleep(0.5)
        case_input.send_keys(case_id)
        time.sleep(0.5)

        # 点击过滤
        filter_submit = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="过滤"]/./.. | //*[contains(@class, "filter-submit")]'))
        )
        filter_submit.click()

        # 等待结果列表加载
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, 
                '//*[@id="container"]/main/section/section[2]/section/div/div[2]/div[2]/div/div/div[2]/div')))

        if not self.get_element_existance():
            # 等待并获取当前状态
            status_cell = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                    '//*[@id="container"]//table//tbody/tr[1]/td[7]'))
            )
            status = status_cell.text

            if status == '待测试':
                # 点击状态下拉菜单
                status_dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                        '//*[@id="container"]//table//tbody/tr[1]/td[7]//button'))
                )
                status_dropdown.click()

                # 等待选项出现
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[text()="已通过"]')))

                # 选择测试结果
                if result.strip() == 'PASS':
                    self.driver.find_element(By.XPATH, '//*[text()="已通过"]').click()
                elif result.strip() == 'FAIL':
                    self.driver.find_element(By.XPATH, '//*[text()="未通过"]').click()
                else:
                    self.driver.find_element(By.XPATH, '//*[text()="暂缓"]').click()
                time.sleep(0.5)

                # 设置执行人
                if test_user:
                    self._set_test_user(test_user)

    def _set_test_user(self, test_user):
        """设置测试执行人
        
        Args:
            test_user: 测试执行人姓名
        """
        try:
            # 等待并点击选择用例
            case_row = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="container"]//table//tbody/tr[1]'))
            )
            case_row.click()
        except:
            # 如果第一种方式失败，尝试备用方式
            case_row = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    '//table//tbody/tr[1]'))
            )
            case_row.click()

        # 等待页面元素加载
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="前置条件"]')))

        # 等待并获取当前执行人
        current_user_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                '//*[@id="workitemAttachment"]/../div[2]/div[2]/div[2]/div/div/span/span[1]/span[1]/em'))
        )
        current_user = current_user_elem.text

        # 如果当前执行人不是目标执行人，则修改
        if current_user != test_user:
            # 点击修改执行人按钮
            change_user_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="workitemAttachment"]/../div[2]/div[2]/div[2]/div/div/span/span[1]/span[2]'))
            )
            change_user_btn.click()

            # 等待搜索框出现
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@placeholder="请输入关键字"]'))
            )

            # 输入执行人姓名
            search_input.send_keys(test_user)

            # 等待用户列表加载
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="uiless-member-mini-v2-members"]'))
            )
            time.sleep(1)

            # 获取用户列表
            user_list_elem = self.driver.find_element(By.XPATH, '//*[@class="uiless-member-mini-v2-members"]')
            user_list = user_list_elem.text

            # 选择执行人
            if test_user in user_list:
                user_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                        f'//*[contains(@class, "uiless-member-mini-v2-members")]//div[contains(text(), "{test_user}")]'))
                )
                user_option.click()
            else:
                # 如果找不到用户，关闭选择框
                close_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                        '//*[@id="workitemAttachment"]/../div[2]/div[2]/div[2]/div/div/span/span[1]/span[2]'))
                )
                close_btn.click()

        # 等待并点击收起用例详情
        close_detail = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="drawer-sidebar-workitemDetail"]/../div'))
        )
        close_detail.click()
        time.sleep(1)