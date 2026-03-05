"""
pytest配置文件
定义共享的fixture和其他配置
"""
import pytest
from utils.driver_factory import DriverFactory
from utils.screenshot import Screenshot
import os
import time
from pages.login_page import LoginPage
from config.config import Config
from pages.main_page import MainPage


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


@pytest.fixture(scope='session')
def authenticated_driver(request):
    """
    Session-scoped WebDriver that is already logged in.
    使用环境变量 `TEST_USERNAME` / `TEST_PASSWORD`，若不存在则使用默认值。
    """
    username = os.getenv('TEST_USERNAME', 'admin')
    password = os.getenv('TEST_PASSWORD', 'Admin@123')

    driver = DriverFactory.get_driver()
    login_page = LoginPage(driver)
    # 导航并登录
    try:
        login_page.navigate_to_login()
        login_page.login(username, password)
        # 等待页面稳定或登录成功
        timeout = 20
        start = time.time()
        while time.time() - start < timeout:
            if login_page.is_login_successful():
                break
            time.sleep(0.5)
        # 登录成功后尝试进入后台管理入口（若页面中存在），封装到 MainPage.enter_backend_management()
        main_page = MainPage(driver)
        try:
            entered = main_page.enter_backend_management()
            if not entered:
                Screenshot.take_screenshot(driver, 'enter_backend_failed')
        except Exception:
            Screenshot.take_screenshot(driver, 'enter_backend_failed')
    except Exception:
        # 若登录流程发生异常，截图并继续抛出
        Screenshot.take_screenshot(driver, 'authenticated_driver_error')
        driver.quit()
        raise

    yield driver

    # 会话结束时关闭浏览器
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest hook，用于获取测试结果
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)