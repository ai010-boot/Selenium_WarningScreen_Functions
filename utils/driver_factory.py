"""
浏览器驱动工厂模块
负责创建和配置不同浏览器的 WebDriver 实例
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import Config
from utils.logger import Logger


class DriverFactory:
    """浏览器驱动工厂类"""
    
    logger = Logger().get_logger()
    
    @classmethod
    def get_chrome_driver(cls):
        """创建 Chrome 浏览器驱动"""
        options = ChromeOptions()
        
        if Config.HEADLESS:
            options.add_argument('--headless')
        
        # 常用配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--start-maximized')
        
        # 禁用自动化提示
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 直接使用 ChromeDriverManager 自动管理驱动，避免本地驱动版本不匹配导致的重试延迟
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        cls.logger.info("Chrome 浏览器启动成功")
        return driver
    
    @classmethod
    def get_firefox_driver(cls):
        """创建 Firefox 浏览器驱动"""
        options = FirefoxOptions()
        
        if Config.HEADLESS:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        cls.logger.info("Firefox 浏览器启动成功")
        return driver
    
    @classmethod
    def get_edge_driver(cls):
        """创建 Edge 浏览器驱动"""
        options = EdgeOptions()
        
        if Config.HEADLESS:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        cls.logger.info("Edge 浏览器启动成功")
        return driver
    
    @classmethod
    def get_driver(cls, browser_name=None):
        """
        根据浏览器名称获取对应的驱动
        
        Args:
            browser_name: 浏览器名称 (chrome/firefox/edge)
        
        Returns:
            WebDriver 实例
        """
        browser = (browser_name or Config.BROWSER).lower()
        
        drivers = {
            'chrome': cls.get_chrome_driver,
            'firefox': cls.get_firefox_driver,
            'edge': cls.get_edge_driver
        }
        
        if browser not in drivers:
            raise ValueError(f"不支持的浏览器类型: {browser}")
        
        driver = drivers[browser]()
        
        # 设置超时
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        return driver
