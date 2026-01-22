"""
示例：如何为新模块添加测试数据支持
"""
import pytest
from test_data.test_data_config import get_test_data


def test_example_how_to_use_for_new_module():
    """
    示例：展示如何使用通用配置为新模块添加测试数据支持
    """
    # 假设我们有一个新的模块叫 'dashboard'
    # 只需要在 test_data_config.py 中添加 dashboard 的路径配置
    # 然后就可以直接使用 get_test_data('dashboard') 来获取数据
    
    # 这里我们使用现有的 login 数据作为示例
    login_data = get_test_data('login')
    
    # 验证获取到了数据
    assert len(login_data) > 0, "应该能获取到至少一条测试数据"
    
    # 验证数据结构
    sample_data = login_data[0]
    assert 'username' in sample_data
    assert 'password' in sample_data
    assert 'description' in sample_data
    assert 'expected_result' in sample_data
    
    print(f"成功获取到 {len(login_data)} 条测试数据")
    print(f"第一条数据: {sample_data}")