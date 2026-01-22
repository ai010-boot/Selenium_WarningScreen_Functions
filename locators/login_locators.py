"""
登录页面元素定位器
将元素定位器集中管理（可选方案）
"""
from selenium.webdriver.common.by import By


class LoginPageLocators:
    """登录页面元素定位器"""
    
    # 登录选项
    LOGIN_OPTIONS = (By.ID, "tab-password")
    
    # 输入框
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='账号']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='密码']")
    
    # 按钮
    LOGIN_BUTTON = (By.XPATH, "//button[@type='button']//span[1]")
    
    # 消息提示
    PROMPT_MESSAGE = (By.XPATH, "//p[@class='el-message__content']")
