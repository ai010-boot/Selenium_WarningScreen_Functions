"""
pytest配置文件
定义共享的fixture和其他配置
"""
import pytest
from utils.driver_factory import DriverFactory
from utils.screenshot import Screenshot


@pytest.fixture(scope="function")
def driver(request):
    """
    创建WebDriver实例的fixture
    每个测试函数使用独立的浏览器实例，避免测试间相互影响
    """
    # 创建浏览器驱动
    driver = DriverFactory.get_driver()
    
    yield driver  # 提供给测试用例使用
    
    # 测试失败时自动截图
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        test_name = request.node.name
        Screenshot.take_screenshot(driver, f"failed_{test_name}")
    
    # 测试完成后清理资源
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest hook，用于获取测试结果
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)