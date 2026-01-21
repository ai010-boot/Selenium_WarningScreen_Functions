"""
pytest配置文件
定义共享的fixture和其他配置
"""
import pytest
from utils.driver_factory import DriverFactory


@pytest.fixture(scope="session")
def driver():
    """
    创建WebDriver实例的fixture
    在整个测试会话期间保持浏览器实例
    """
    # 创建浏览器驱动
    driver = DriverFactory.get_driver()
    
    yield driver  # 提供给测试用例使用
    
    # 测试完成后清理资源
    driver.quit()