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
        'dev': 'https://aiot.aiysyd.cn/screen/login',
        'test': 'https://aiot.aiysyd.cn/screen/login',
        'prod': 'https://aiot.aiysyd.cn/screen/login'
    }
    BASE_URL = URLS.get(ENV, URLS['test'])
    
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

# 确保必要目录存在
for _p in [
    Config.REPORTS_DIR,
    Config.SCREENSHOTS_DIR,
    Config.LOGS_DIR,
    Config.REPORTS_DIR / 'html',
]:
    _p.mkdir(parents=True, exist_ok=True)
