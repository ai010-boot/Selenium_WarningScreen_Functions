"""
测试数据配置使用示例
展示如何为新模块添加测试数据支持
"""
import pytest
from test_data.test_data_config import TestDataConfig, get_test_data


def test_using_universal_config_for_login():
    """
    测试使用通用配置获取登录测试数据
    """
    # 使用便捷函数获取登录测试数据
    login_data = get_test_data('login')
    
    # 验证获取到了数据
    assert len(login_data) > 0, "应该能获取到至少一条测试数据"
    
    # 验证数据结构
    sample_data = login_data[0]
    assert 'username' in sample_data
    assert 'password' in sample_data
    assert 'description' in sample_data
    assert 'expected_result' in sample_data
    
    print(f"成功获取到 {len(login_data)} 条登录测试数据")
    print(f"第一条数据: {sample_data}")


def test_loading_different_formats():
    """
    测试加载不同格式的数据
    """
    # 测试加载CSV格式数据
    csv_data = get_test_data('login', 'csv')
    print(f"CSV格式数据: {len(csv_data)} 条")
    
    # 测试加载JSON格式数据
    json_data = get_test_data('login', 'json')
    print(f"JSON格式数据: {len(json_data)} 条")
    
    # 测试自动检测格式
    auto_data = get_test_data('login', 'auto')
    print(f"自动检测格式数据: {len(auto_data)} 条")
    
    # 验证所有格式的数据量一致
    assert len(csv_data) == len(json_data) == len(auto_data), "不同格式的数据量应该一致"


def test_adding_new_module_data():
    """
    演示如何为新模块添加测试数据支持
    """
    # 假设我们要添加一个新的 'home' 模块
    # 首先需要在 TestDataConfig.TEST_DATA_PATHS 中添加配置
    TestDataConfig.TEST_DATA_PATHS['home'] = {
        'csv': TestDataConfig.PROJECT_ROOT / 'test_data' / 'home_test_data.csv',
        'json': TestDataConfig.PROJECT_ROOT / 'test_data' / 'home_test_data.json',
        'xlsx': TestDataConfig.PROJECT_ROOT / 'test_data' / 'home_test_data.xlsx'
    }
    
    # 然后我们就可以使用相同的方式获取新模块的数据
    # 注意：由于文件不存在，这将返回默认数据
    home_data = get_test_data('home')
    print(f"Home模块测试数据（默认）: {len(home_data)} 条")
    
    # 验证默认数据结构
    if home_data:
        assert 'username' in home_data[0] or 'description' in home_data[0], "默认数据应该有基本字段"
    
    print("成功演示如何为新模块添加测试数据支持")


class TestUniversalDataUsage:
    """
    使用通用数据配置的测试示例
    """
    
    @pytest.mark.parametrize("test_case", get_test_data('login'))
    def test_login_with_universal_data(self, driver, test_case):
        """
        使用通用数据配置进行登录测试
        
        Args:
            driver: WebDriver 实例
            test_case: 从通用配置获取的测试数据
        """
        # 这里可以实现实际的测试逻辑
        # 为了演示目的，我们只是验证数据结构
        assert 'username' in test_case
        assert 'password' in test_case
        assert 'description' in test_case
        assert 'expected_result' in test_case
        
        print(f"测试用例: {test_case['description']}")
        
        # 实际的测试逻辑会在这里
        # login_page = LoginPage(driver)
        # login_page.navigate_to_login()
        # login_page.login(test_case["username"], test_case["password"])
        # if test_case["expected_result"] == "success":
        #     assert login_page.is_login_successful()
        # else:
        #     assert login_page.is_login_failed()