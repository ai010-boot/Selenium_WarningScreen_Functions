"""
CSV数据驱动登录测试用例
"""
import pytest
from pages.login_page import LoginPage
from test_data.test_data_config import get_test_data


class TestLoginCSVDirected:
    """基于CSV数据的登录功能测试类"""
    
    _TEST_CATEGORY = 'login'
    _DATA_TYPE = 'csv'

    @pytest.mark.parametrize("test_case", get_test_data(_TEST_CATEGORY, _DATA_TYPE))
    def test_login_with_csv_data(self, driver, test_case):
        """
        使用CSV数据驱动的方式测试登录功能
        
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
    
    def test_csv_data_summary(self, driver):
        """测试CSV数据的整体概览"""
        test_data = get_test_data(self._TEST_CATEGORY, self._DATA_TYPE)
        print(f"总共加载了 {len(test_data)} 条测试数据")
        
        successful_logins = 0
        failed_logins = 0
        
        for test_case in test_data:
            login_page = LoginPage(driver)
            
            # 导航到登录页面
            login_page.navigate_to_login()
            
            # 执行登录
            login_page.login(test_case["username"], test_case["password"])
            
            # 根据预期结果进行断言
            if test_case["expected_result"] == "success":
                assert login_page.is_login_successful(), f"登录应该成功: {test_case['description']}"
                successful_logins += 1
            else:
                assert login_page.is_login_failed(), f"登录应该失败: {test_case['description']}"
                failed_logins += 1
        
        print(f"预期成功登录: {successful_logins} 次")
        print(f"预期失败登录: {failed_logins} 次")