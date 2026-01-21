"""
首页元素定位器
"""
from selenium.webdriver.common.by import By


class HomePageLocators:
    """首页元素定位器"""
    
    # 顶部导航
    LOGO = (By.CLASS_NAME, "logo")
    NAVIGATION_MENU = (By.CLASS_NAME, "nav-menu")
    USER_PROFILE = (By.ID, "user-profile")
    LOGOUT_BUTTON = (By.ID, "logout-btn")
    
    # 搜索
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.ID, "search-btn")
    
    # 主要内容
    WELCOME_MESSAGE = (By.XPATH, "//h1[@class='welcome']")
    MAIN_CONTENT = (By.ID, "main-content")
    
    # 导航链接
    HOME_LINK = (By.LINK_TEXT, "Home")
    PRODUCTS_LINK = (By.LINK_TEXT, "Products")
    ORDERS_LINK = (By.LINK_TEXT, "Orders")
    SETTINGS_LINK = (By.LINK_TEXT, "Settings")
    ABOUT_LINK = (By.LINK_TEXT, "About")
    CONTACT_LINK = (By.LINK_TEXT, "Contact")
    
    # 侧边栏
    SIDEBAR = (By.ID, "sidebar")
    CATEGORIES_LIST = (By.CLASS_NAME, "categories")
    
    # 页脚
    FOOTER = (By.TAG_NAME, "footer")
    COPYRIGHT = (By.CLASS_NAME, "copyright")
