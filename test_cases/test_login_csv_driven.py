"""
登录功能测试用例 - 数据驱动版本
使用CSV数据源进行测试
"""
import pytest
from pages.login_page import LoginPage
from test_data.test_data_config import get_test_data


class TestLoginDataDriven:
    """使用数据驱动的登录功能测试类"""
    
    @pytest.mark.parametrize("test_case", get_test_data('login', 'csv'))
    @pytest.mark.smoke
    def test_login_csv_driven(self, driver, test_case):
        """
        测试用例: 使用CSV数据驱动的登录测试
        数据源: test_data/test_type/login_test_data.csv
        
        Args:
            driver: WebDriver 实例
            test_case: 测试数据字典，包含username, password, description, expected_result
        """
        login_page = LoginPage(driver)
        
        # 导航到登录页面
        login_page.navigate_to_login()
        
        # 执行登录
        login_page.login(
            test_case.get('username', ''),
            test_case.get('password', '')
        )
        
        # 根据期望结果进行断言
        if test_case.get('expected_result') == 'success':
            assert login_page.is_login_successful(), \
                f"测试失败: {test_case.get('description')} - 应该登录成功"
        else:
            # 对于失败情况，检查是否显示错误或未成功登录
            assert login_page.is_login_failed() or not login_page.is_login_successful(), \
                f"测试失败: {test_case.get('description')} - 应该登录失败"
        
        print(f"✓ 测试通过: {test_case.get('description')}")
