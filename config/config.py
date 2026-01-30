"""
配置管理模块
统一管理项目配置信息
"""
# 全局配置类（URL、超时、路径、测试账号等）
import os
from pathlib import Path


class Config:
    """全局配置类"""
    
    # 项目根目录
    BASE_DIR = Path(__file__).parent.parent
    
    # 浏览器配置
    BROWSER = os.getenv('BROWSER', 'chrome')  # chrome, firefox, edge
    # HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'true'  # 启用无头模式，提升测试速度
    HEADLESS = os.getenv('HEADLESS', 'True').lower() == 'False'  # 启用有头模式，实时预览
    
    # 超时配置（优化后）
    IMPLICIT_WAIT = 5  # 隐式等待（秒）
    EXPLICIT_WAIT = 10  # 显式等待（秒）
    PAGE_LOAD_TIMEOUT = 30  # 页面加载超时（秒）- 恢复为30秒
    
    # 测试环境配置
    ENV = os.getenv('ENV', 'test')  # dev, test, prod
    
    # URL配置
    BASE_URL = 'https://aiot.aiysyd.cn/screen/login'
    
    # 路径配置
    DRIVERS_DIR = BASE_DIR / 'drivers'
    REPORTS_DIR = BASE_DIR / 'reports'
    SCREENSHOTS_DIR = REPORTS_DIR / 'screenshots'
    LOGS_DIR = REPORTS_DIR / 'logs'
    TEST_DATA_DIR = BASE_DIR / 'test_data'
    
    # 报告输出路径（三种格式）
    ALLURE_DIR = REPORTS_DIR / 'allure-results'
    HTMLREPORT_DIR = REPORTS_DIR / 'html_report'
    
    # 截图配置
    SCREENSHOT_ON_FAILURE = True
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


# 确保必要目录存在
for _p in [
    Config.REPORTS_DIR,
    Config.SCREENSHOTS_DIR,
    Config.LOGS_DIR,
    Config.REPORTS_DIR / 'html',
    Config.ALLURE_DIR,
    Config.HTMLREPORT_DIR,
]:
    _p.mkdir(parents=True, exist_ok=True)