"""
Excel数据驱动登录测试用例
"""
import pytest
from pages.login_page import LoginPage
from test_data.test_data_config import get_test_data


class TestLoginExcelDriven:
    """基于Excel数据的登录功能测试类"""
    
    @pytest.mark.parametrize("test_case", get_test_data('login', 'auto'))
    def test_login_with_data(self, driver, test_case):
        """
        使用数据驱动的方式测试登录功能
        
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
    
    def test_excel_data_integration(self, driver):
        """
        集成Excel数据的测试示例
        """
        test_data = get_test_data('login', 'auto')
        login_page = LoginPage(driver)
        
        # 遍历Excel数据并执行测试
        for idx, test_case in enumerate(test_data):
            # 每次测试前先回到登录页
            login_page.navigate_to_login()
            
            # 执行登录
            login_page.login(test_case["username"], test_case["password"])
            
            # 根据预期结果进行断言
            if test_case["expected_result"] == "success":
                assert login_page.is_login_successful(), f"测试用例 {idx+1} - {test_case['description']}: 登录应该成功"
            else:
                assert login_page.is_login_failed(), f"测试用例 {idx+1} - {test_case['description']}: 登录应该失败"
            
            # 简单延时，确保界面状态重置
            driver.implicitly_wait(1)


# 如果需要实际使用Excel数据，可以取消以下注释并按需修改
"""
class TestLoginWithRealExcelData:
    @pytest.mark.parametrize("username,password,description,expected_result", 
                             read_excel_data(os.path.join(Config.TEST_DATA_DIR, "login_test_data.xlsx"), "login_test_data"))
    def test_login_from_excel(self, driver, username, password, description, expected_result):
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login(username, password)
        
        if expected_result == "success":
            assert login_page.is_login_successful(), f"登录应该成功: {description}"
        else:
            assert login_page.is_login_failed(), f"登录应该失败: {description}"
"""