"""
浏览器驱动工厂模块
负责创建和配置不同浏览器的 WebDriver 实例
"""
import os
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
    def _get_chrome_options(cls) -> ChromeOptions:
        """获取 Chrome 浏览器配置"""
        options = ChromeOptions()
        
        if Config.HEADLESS:
            options.add_argument('--headless=new')
        
        # 通用优化配置
        for arg in [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-notifications',
            '--start-maximized',
            '--disable-extensions'
        ]:
            options.add_argument(arg)
        
        # 禁用自动化提示和日志
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        return options
    
    @classmethod
    def _get_firefox_options(cls) -> FirefoxOptions:
        """获取 Firefox 浏览器配置"""
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument('--headless')
        return options
    
    @classmethod
    def _get_edge_options(cls) -> EdgeOptions:
        """获取 Edge 浏览器配置"""
        options = EdgeOptions()
        if Config.HEADLESS:
            options.add_argument('--headless')
        
        for arg in ['--no-sandbox', '--disable-dev-shm-usage', '--start-maximized']:
            options.add_argument(arg)
        
        return options
    
    @classmethod
    def get_chrome_driver(cls):
        """创建 Chrome 浏览器驱动"""
        try:
            driver_path = ChromeDriverManager().install()
            # 确保路径指向 chromedriver.exe
            if not driver_path.endswith('chromedriver.exe'):
                driver_dir = os.path.dirname(driver_path)
                for file in os.listdir(driver_dir):
                    if file == 'chromedriver.exe':
                        driver_path = os.path.join(driver_dir, file)
                        break
            
            service = ChromeService(driver_path)
            driver = webdriver.Chrome(service=service, options=cls._get_chrome_options())
            cls.logger.info("Chrome 浏览器启动成功")
            return driver
        except Exception as e:
            cls.logger.error(f"Chrome 驱动初始化失败: {e}")
            raise
    
    @classmethod
    def get_firefox_driver(cls):
        """创建 Firefox 浏览器驱动"""
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=cls._get_firefox_options())
        cls.logger.info("Firefox 浏览器启动成功")
        return driver
    
    @classmethod
    def get_edge_driver(cls):
        """创建 Edge 浏览器驱动"""
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=cls._get_edge_options())
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
