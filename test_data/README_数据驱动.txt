"""
数据驱动测试 - 使用说明

## 快速使用（3步）

### 1. 导入函数
from test_data.test_data_config import get_test_data

### 2. 在测试中使用
@pytest.mark.parametrize("test_case", get_test_data('login'))
def test_example(self, driver, test_case):
    username = test_case['username']
    password = test_case['password']
    # ... 测试逻辑

### 3. 完成！

## 支持的格式
- CSV:   get_test_data('login', 'csv')
- JSON:  get_test_data('login', 'json')
- Excel: get_test_data('login', 'xlsx')
- 自动:  get_test_data('login')  # 推荐

## 参考示例
查看完整示例: test_cases/test_login_data_driven.py
"""
