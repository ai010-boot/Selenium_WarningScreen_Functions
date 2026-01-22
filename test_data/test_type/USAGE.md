# 通用测试数据配置使用说明

## 概述

本项目提供了一个通用的测试数据配置系统，用于统一管理所有模块的测试数据。通过 `test_data_config.py` 文件，可以方便地从不同格式（CSV、JSON、Excel）加载测试数据。

## 主要功能

- 统一管理所有模块的测试数据路径
- 支持多种数据格式：CSV、JSON、Excel
- 自动检测可用的数据格式
- 提供便捷的访问函数
- 当数据文件不存在时提供默认数据

## 使用方法

### 1. 基本使用

```python
from test_data.test_data_config import get_test_data

# 获取登录模块的测试数据（自动检测格式）
login_data = get_test_data('login')

# 指定数据格式
csv_data = get_test_data('login', 'csv')
json_data = get_test_data('login', 'json')
excel_data = get_test_data('login', 'xlsx')
```

### 2. 在测试用例中使用

```python
import pytest
from test_data.test_data_config import get_test_data

class TestLogin:
    @pytest.mark.parametrize("test_case", get_test_data('login'))
    def test_login_function(self, driver, test_case):
        # 使用测试数据进行测试
        username = test_case['username']
        password = test_case['password']
        expected_result = test_case['expected_result']
        
        # 实际的测试逻辑...
```

### 3. 为新模块添加支持

要为新模块添加测试数据支持，需要修改 `TestDataConfig` 类中的 `TEST_DATA_PATHS` 配置：

```python
# 在 TestDataConfig 类中
TEST_DATA_PATHS = {
    'login': {
        'csv': PROJECT_ROOT / 'test_data' / 'login_test_data.csv',
        'json': PROJECT_ROOT / 'test_data' / 'login_test_data.json',
        'xlsx': PROJECT_ROOT / 'test_data' / 'login_test_data.xlsx'
    },
    'new_module': {  # 新增模块
        'csv': PROJECT_ROOT / 'test_data' / 'new_module_test_data.csv',
        'json': PROJECT_ROOT / 'test_data' / 'new_module_test_data.json',
        'xlsx': PROJECT_ROOT / 'test_data' / 'new_module_test_data.xlsx'
    },
}
```

然后就可以使用：

```python
new_module_data = get_test_data('new_module')
```

## 支持的模块

目前支持以下模块：

- `login`: 登录模块测试数据

## 支持的格式

- `csv`: CSV格式的测试数据
- `json`: JSON格式的测试数据
- `xlsx`: Excel格式的测试数据
- `auto`: 自动检测可用的数据格式（按CSV、JSON、Excel的顺序）

## 注意事项

1. 数据文件应按照约定的格式准备，包含必需的字段
2. 当指定格式的数据文件不存在时，系统会返回默认数据
3. CSV文件应包含表头行，JSON文件应使用特定的键名格式
4. Excel文件的第一个工作表会被作为数据源

## 文件格式要求

### CSV格式
```
username,password,description,expected_result
user1,pass1,描述1,success
user2,pass2,描述2,failure
```

### JSON格式
```json
{
  "login_test_data": [
    {
      "username": "user1",
      "password": "pass1",
      "description": "描述1",
      "expected_result": "success"
    },
    {
      "username": "user2",
      "password": "pass2",
      "description": "描述2",
      "expected_result": "failure"
    }
  ]
}
```

### Excel格式
第一行应为列标题，后续行为数据，列标题应与CSV格式一致。