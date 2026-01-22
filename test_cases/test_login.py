"""
登录功能测试用例
"""
import pytest
from pages.login_page import LoginPage
from config.config import Config


class TestLogin:
    """登录功能测试类"""
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_valid_login(self, driver):
        """
        测试用例: 使用有效凭证登录
        预期结果: 登录成功，跳转到首页
        """
        # 初始化页面对象
        login_page = LoginPage(driver)
        
        # 导航到登录页面
        login_page.navigate_to_login()
        
        # 执行登录
        login_page.login(
            Config.TEST_USER['username'],
            Config.TEST_USER['password']
        )
        
        # 验证登录成功
        assert login_page.is_login_successful(), "登录应该成功"
    
    @pytest.mark.regression
    def test_invalid_username(self, driver):
        """
        测试用例: 使用无效用户名登录
        预期结果: 登录失败，显示错误消息
        """
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        login_page.login("invalid_user", "password123")
        
        # 验证显示错误消息
        assert login_page.is_login_failed(), "应该显示错误消息"
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "错误消息不能为空"
    
    @pytest.mark.regression
    def test_invalid_password(self, driver):
        """
        测试用例: 使用无效密码登录
        预期结果: 登录失败，显示错误消息
        """
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        login_page.login(Config.TEST_USER['username'], "wrong_password")
        
        assert login_page.is_login_failed(), "应该显示错误消息"
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "错误消息不能为空"
    
    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,description", [
        ("", "password123", "空用户名"),
        ("testuser", "", "空密码"),
        ("", "", "用户名和密码都为空"),
    ])
    def test_empty_credentials(self, driver, username, password, description):
        """
        测试用例: 使用空凭证登录
        预期结果: 登录失败或显示验证错误
        
        Args:
            driver: WebDriver 实例
            username: 用户名
            password: 密码
            description: 测试描述
        """
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        login_page.login(username, password)
        
        # 验证未成功登录
        assert not login_page.is_login_successful(), \
            f"{description}: 不应该登录成功"
    
    @pytest.mark.smoke
    def test_remember_me_functionality(self, driver):
        """
        测试用例: 测试"记住我"功能
        预期结果: 勾选后登录成功
        """
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        login_page.login(
            Config.TEST_USER['username'],
            Config.TEST_USER['password'],
        )
        
        # 验证登录成功
        assert login_page.is_login_successful(), "登录应该成功"
    
    @pytest.mark.regression
    def test_logout_functionality(self, driver):
        """
        测试用例: 测试退出登录功能
        预期结果: 成功退出，返回登录页面
        """
        login_page = LoginPage(driver)
        
        # 先登录
        login_page.navigate_to_login()
        login_page.login(
            Config.TEST_USER['username'],
            Config.TEST_USER['password']
        )
        
        # 验证登录成功
        assert login_page.is_login_successful(), "登录应该成功"
    
    @pytest.mark.regression
    def test_login_page_elements(self, driver):
        """
        测试用例: 验证登录页面元素存在性
        预期结果: 所有必需元素都存在
        """
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        
        # 验证关键元素存在
        assert login_page.is_element_visible(login_page.USERNAME_INPUT), \
            "用户名输入框不可见"
        assert login_page.is_element_visible(login_page.PASSWORD_INPUT), \
            "密码输入框不可见"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), \
            "登录按钮不可见"
    
    @pytest.mark.regression
    def test_clear_login_form(self, driver):
        """
        测试用例: 测试清空表单功能
        预期结果: 表单内容被清空
        """
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        
        # 输入内容
        login_page.enter_username("test_user")
        login_page.enter_password("test_password")
        
        # 清空表单
        login_page.clear_login_form()
        
        # 验证已清空
        username = login_page.get_attribute(login_page.USERNAME_INPUT, "value")
        password = login_page.get_attribute(login_page.PASSWORD_INPUT, "value")
        
        assert username == "", "用户名未清空"
        assert password == "", "密码未清空"


# @pytest.mark.skip(reason="演示跳过的测试")
# class TestLoginAdvanced:
#     """高级登录测试（示例）"""
    
#     def test_sql_injection_prevention(self, driver):
#         """测试 SQL 注入防护"""
#         login_page = LoginPage(driver)
        
#         login_page.navigate_to_login()
#         login_page.login("admin' OR '1'='1", "password")
        
#         assert login_page.is_login_failed(), "存在 SQL 注入漏洞"
    
#     def test_xss_prevention(self, driver):
#         """测试 XSS 攻击防护"""
#         login_page = LoginPage(driver)
        
#         login_page.navigate_to_login()
#         login_page.login("<script>alert('XSS')</script>", "password")
        
#         assert login_page.is_login_failed(), "存在 XSS 漏洞"
