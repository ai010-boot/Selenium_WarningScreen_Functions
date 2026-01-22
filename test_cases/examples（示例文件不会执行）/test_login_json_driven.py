"""
JSON数据驱动登录测试用例
"""
import pytest
from pages.login_page import LoginPage
from test_data.test_data_config import get_test_data


class TestLoginJSONDriven:
    """基于JSON数据的登录功能测试类"""
    
    @pytest.mark.parametrize("test_case", get_test_data('login', 'json'))
    def test_login_with_json_data(self, driver, test_case):
        """
        使用JSON数据驱动的方式测试登录功能
        
        Args:
            driver: WebDriver 实例
            test_case: 包含测试数据的字典
        """
        login_page = LoginPage(driver)
        
        # 导航到登录页面
        login_page.navigate_to_login()
        
        # 执行登录
        login_page.login(test_case["username"], test_case["password"])
        
        # 根据预期结果进行断言
        if test_case["expected_result"] == "success":
            assert login_page.is_login_successful(), f"登录应该成功: {test_case['description']}"
        else:
            assert login_page.is_login_failed(), f"登录应该失败: {test_case['description']}"