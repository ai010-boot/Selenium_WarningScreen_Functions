"""
# 登录页面对象类
 登录页面的业务封装（登录方法、元素定位、状态验证）

"""
from pages.base_page import BasePage
from config.config import Config
from locators.login_locators import LoginPageLocators


class LoginPage(BasePage):
    """登录页面对象类"""
    
    # 从 LoginPageLocators 引用元素定位器
    LOGIN_OPTIONS = LoginPageLocators.LOGIN_OPTIONS
    USERNAME_INPUT = LoginPageLocators.USERNAME_INPUT
    PASSWORD_INPUT = LoginPageLocators.PASSWORD_INPUT
    LOGIN_BUTTON = LoginPageLocators.LOGIN_BUTTON
    PROMPT_MESSAGE = LoginPageLocators.PROMPT_MESSAGE
    
    def __init__(self, driver):
        """
        初始化登录页面
        """
        super().__init__(driver)
        self.url = Config.BASE_URL
    
    def navigate_to_login(self):
        """导航到登录页面"""
        self.driver.get(self.url)
        self.logger.info(f"导航到登录页面: {self.url}")

    def select_login_option(self, option=None):
        """
        选择登录选项（点击切换到账号密码登录）
        """
        # 查找并点击登录选项元素
        self.find_element(self.LOGIN_OPTIONS).click()
    
    def enter_username(self, username):
        """
        输入用户名
        """
        self.input_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """
        输入密码
        """
        self.input_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        
    def login(self, username, password):
        """
        执行登录操作
        Args:
            username: 用户名
            password: 密码
        """
        self.logger.info(f"尝试登录，用户名: {username}")
        
        # 首先尝试选择登录选项
        self.select_login_option()       
        # 输入用户名和密码
        self.enter_username(username)
        self.enter_password(password)       
        self.click_login_button()       
        # 等待加载完成
        if self.is_element_visible(self.PROMPT_MESSAGE, timeout=2):
            self.wait_for_element_to_disappear(self.PROMPT_MESSAGE, timeout=10)
    
    def get_error_message(self):
        """
        获取错误消息
        
        Returns:
            错误消息文本
        """
        if self.is_element_visible(self.PROMPT_MESSAGE, timeout=5):
            message_text = self.get_text(self.PROMPT_MESSAGE)
            if any(keyword in message_text.lower() for keyword in ['账号不存在或账号状态异常，请联系管理员', '账号或密码错误']):
                return message_text
        return None
    
    def get_success_message(self):
        """
        获取成功消息
        
        Returns:
            成功消息文本
        """
        if self.is_element_visible(self.PROMPT_MESSAGE, timeout=5):
            message_text = self.get_text(self.PROMPT_MESSAGE)
            if any(keyword in message_text.lower() for keyword in ['登录成功']):
                return message_text
        return None
    
    def is_login_successful(self):
        """
        检查是否登录成功
        Returns:
            bool: 登录是否成功
        """
        # 检查是否跳转到主页或显示成功消息
        try:
            # 检查URL是否改变（表明已登录并跳转）
            url_changed = self.get_current_url() != self.url
            # 检查是否有成功消息
            has_success_message = self.get_success_message() is not None
            # 如果URL改变了或者有成功提示，则认为登录成功
            return url_changed or has_success_message
        except Exception:
            return False
    
    def is_login_failed(self):
        """
        检查登录是否失败
        
        Returns:
            bool: 是否显示错误消息
        """
        return self.get_error_message() is not None
    
    def clear_login_form(self):
        """清空登录表单"""
        username_input = self.find_element(self.USERNAME_INPUT)
        password_input = self.find_element(self.PASSWORD_INPUT)
        
        username_input.clear()
        password_input.clear()
        
        self.logger.info("已清空登录表单")