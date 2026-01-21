"""
配置管理模块
统一管理项目配置信息
"""
import os
from pathlib import Path


class Config:
    """全局配置类"""
    
    # 项目根目录
    BASE_DIR = Path(__file__).parent.parent
    
    # 浏览器配置
    BROWSER = os.getenv('BROWSER', 'chrome')  # chrome, firefox, edge
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    
    # 超时配置
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # 测试环境配置
    ENV = os.getenv('ENV', 'test')  # dev, test, prod
    
    # URL配置
    URLS = {
        'dev': 'https://dev.example.com',      # 开发环境
        'test': 'https://test.example.com',    # 测试环境
        'prod': 'https://aiot.aiysyd.cn/screen',     # 生产环境
    }
    BASE_URL = URLS.get(ENV, URLS['prod'])  # 默认使用新添加的本地URL
    
    # 路径配置
    DRIVERS_DIR = BASE_DIR / 'drivers'
    REPORTS_DIR = BASE_DIR / 'reports'
    SCREENSHOTS_DIR = REPORTS_DIR / 'screenshots'
    LOGS_DIR = REPORTS_DIR / 'logs'
    TEST_DATA_DIR = BASE_DIR / 'test_data'
    
    # 截图配置
    SCREENSHOT_ON_FAILURE = True
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 测试数据
    TEST_USER = {
        'username': 'jkcsdw',
        'password': '123456'
    }
    
    # 数据库配置（如需要）
    DATABASE = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'test_db'
    }
    
    @classmethod
    def get_driver_path(cls, browser_name):
        """获取浏览器驱动路径"""
        drivers = {
            'chrome': 'chromedriver.exe',
            'firefox': 'geckodriver.exe',
            'edge': 'msedgedriver.exe'
        }
        driver_file = drivers.get(browser_name.lower())
        if not driver_file:
            raise ValueError(f"不支持的浏览器: {browser_name}")
        
        return str(cls.DRIVERS_DIR / driver_file)
    
    @classmethod
    def ensure_dirs(cls):
        """确保必要的目录存在"""
        cls.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)


# 确保目录存在
Config.ensure_dirs()