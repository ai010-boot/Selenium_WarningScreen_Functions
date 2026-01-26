# 数据驱动框架使用指南

本项目采用 **"约定优于配置"** 的设计模式，让数据驱动测试变得极其简单。
你**不需要**修改任何代码，只需要添加一个文件，就可以为新模块添加测试数据。

## 1. 核心原则

*   **无需配置**：不用去改 `test_data_config.py` 中的字典或列表。
*   **自动查找**：系统会根据文件名自动发现并加载数据。

## 2. 如何添加测试数据（3步走）

### 步骤 1：创建数据文件
在 `test_data/test_type/` 目录下创建一个新文件。

*   **命名规则**（必须严格遵守）：
    `{模块名}_test_data.{后缀}`

*   **支持的格式**（推荐 CSV）：
    *   `login_test_data.csv`  (推荐)
    *   `login_test_data.json`
    *   `login_test_data.xlsx`

### 步骤 2：填充数据 (CSV示例)
用 Excel 或文本编辑器打开 CSV 文件，第一行必须是字段名。

```csv
test_case_id,username,password,expected,description
case_01,admin,123456,success,正常登录
case_02,user_err,123456,fail,用户名错误
```

### 步骤 3：在代码中使用
使用 `get_test_data('模块名')` 即可直接获取数据列表。

```python
import pytest
from test_data.test_data_config import get_test_data

# 只需要填 'login'，系统会自动去找 login_test_data.csv
@pytest.mark.parametrize("data", get_test_data('login'))
def test_login(self, driver, data):
    print(f"正在测试: {data['description']}")
    # 像字典一样使用数据
    user = data['username']
```

## 3. 支持的数据格式

| 格式 | 优先级 | 说明 |
| :--- | :--- | :--- |
| **CSV** | 1 (最高) | **最推荐**。编辑方便，Git 友好，体积小。请务必使用 **UTF-8** 编码。 |
| **JSON** | 2 | 适合通过程序生成或结构非常复杂的数据。 |
| **Excel** | 3 | 适合业务人员维护的大量数据，但读取速度稍慢。 |

## 4. 常见问题

*   **Q: 文件名必须是 `_test_data` 结尾吗？**
    *   A: 是的。系统通过这个后缀来识别这是测试数据文件。

*   **Q: 如果我同时放了 .csv 和 .json 怎么办？**
    *   A: 系统会按照优先级 (CSV > JSON > Excel) 只加载其中一个。

*   **Q: 使用 CSV 中文乱码？**
    *   A: 请确保文件保存为 `UTF-8` 编码。Excel 另存为时选择 "CSV UTF-8 (逗号分隔)"。
