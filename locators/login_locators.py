"""
登录页面元素定位器
将元素定位器集中管理（可选方案）
"""
from selenium.webdriver.common.by import By


class LoginPageLocators:
    """登录页面元素定位器"""
    
    # 输入框
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    EMAIL_INPUT = (By.NAME, "email")
    
    # 按钮
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    SIGNUP_BUTTON = (By.LINK_TEXT, "Sign Up")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    
    # 复选框
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    TERMS_CHECKBOX = (By.NAME, "terms")
    
    # 消息提示
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    WARNING_MESSAGE = (By.CSS_SELECTOR, ".warning-message")
    
    # 加载状态
    LOADING_SPINNER = (By.CLASS_NAME, "loading-spinner")
    
    # 表单
    LOGIN_FORM = (By.ID, "login-form")
    
    # 其他元素
    LOGO = (By.CLASS_NAME, "brand-logo")
    FOOTER = (By.TAG_NAME, "footer")
