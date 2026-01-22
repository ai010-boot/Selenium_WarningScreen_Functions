"""
数据驱动的登录功能测试用例
演示如何使用CSV、JSON、Excel等多种数据源进行测试
"""
import pytest
from pages.login_page import LoginPage
from config.config import Config
from test_data.test_data_config import get_test_data


class TestLoginDataDriven:
    """使用数据驱动的登录功能测试类"""
    
    @pytest.mark.parametrize("test_case", get_test_data('login', 'auto'))
    def test_login_with_auto_data(self, driver, test_case):
        """
        测试用例: 使用自动检测格式的数据驱动测试
        数据源: 自动选择可用的数据文件（CSV/JSON/Excel）
        
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
            assert login_page.is_login_failed() or not login_page.is_login_successful(), \
                f"测试失败: {test_case.get('description')} - 应该登录失败"
        
        print(f"✓ 测试通过: {test_case.get('description')}")
    
    @pytest.mark.parametrize("test_case", get_test_data('login', 'csv'))
    def test_login_with_csv_data(self, driver, test_case):
        """
        测试用例: 使用CSV数据源的数据驱动测试
        数据源: test_data/test_type/login_test_data.csv
        
        Args:
            driver: WebDriver 实例
            test_case: 从CSV文件读取的测试数据
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        login_page.login(
            test_case.get('username', ''),
            test_case.get('password', '')
        )
        
        # 验证结果
        if test_case.get('expected_result') == 'success':
            assert login_page.is_login_successful(), \
                f"CSV测试: {test_case.get('description')} - 登录应该成功"
        else:
            assert login_page.is_login_failed() or not login_page.is_login_successful(), \
                f"CSV测试: {test_case.get('description')} - 登录应该失败"
    
    @pytest.mark.parametrize("test_case", get_test_data('login', 'json'))
    def test_login_with_json_data(self, driver, test_case):
        """
        测试用例: 使用JSON数据源的数据驱动测试
        数据源: test_data/test_type/login_test_data.json
        
        Args:
            driver: WebDriver 实例
            test_case: 从JSON文件读取的测试数据
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        login_page.login(
            test_case.get('username', ''),
            test_case.get('password', '')
        )
        
        # 验证结果
        if test_case.get('expected_result') == 'success':
            assert login_page.is_login_successful(), \
                f"JSON测试: {test_case.get('description')} - 登录应该成功"
        else:
            assert login_page.is_login_failed() or not login_page.is_login_successful(), \
                f"JSON测试: {test_case.get('description')} - 登录应该失败"
    
    @pytest.mark.parametrize("test_case", get_test_data('login', 'xlsx'))
    def test_login_with_excel_data(self, driver, test_case):
        """
        测试用例: 使用Excel数据源的数据驱动测试
        数据源: test_data/test_type/login_test_data.xlsx
        
        Args:
            driver: WebDriver 实例
            test_case: 从Excel文件读取的测试数据
        """
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        login_page.login(
            test_case.get('username', ''),
            test_case.get('password', '')
        )
        
        # 验证结果
        if test_case.get('expected_result') == 'success':
            assert login_page.is_login_successful(), \
                f"Excel测试: {test_case.get('description')} - 登录应该成功"
        else:
            assert login_page.is_login_failed() or not login_page.is_login_successful(), \
                f"Excel测试: {test_case.get('description')} - 登录应该失败"


class TestDataSourceComparison:
    """对比测试：验证不同数据源的一致性"""
    
    def test_data_source_consistency(self):
        """
        验证CSV、JSON、Excel三种数据源的数据一致性
        """
        csv_data = get_test_data('login', 'csv')
        json_data = get_test_data('login', 'json')
        xlsx_data = get_test_data('login', 'xlsx')
        
        # 验证数据量一致
        assert len(csv_data) == len(json_data) == len(xlsx_data), \
            f"数据源数量不一致: CSV={len(csv_data)}, JSON={len(json_data)}, Excel={len(xlsx_data)}"
        
        print(f"✓ 数据一致性检查通过: 所有数据源包含 {len(csv_data)} 条测试数据")
        
        # 验证关键字段存在
        for data_source, data_name in [(csv_data, 'CSV'), (json_data, 'JSON'), (xlsx_data, 'Excel')]:
            for i, test_case in enumerate(data_source):
                assert 'username' in test_case, f"{data_name}数据第{i+1}条缺少username字段"
                assert 'password' in test_case, f"{data_name}数据第{i+1}条缺少password字段"
                assert 'expected_result' in test_case, f"{data_name}数据第{i+1}条缺少expected_result字段"
        
        print("✓ 所有数据源字段完整性检查通过")
