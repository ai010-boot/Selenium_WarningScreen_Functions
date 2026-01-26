# 通用测试数据配置使用说明 (Usage Guide)

## 核心设计：约定优于配置

本项目采用自动化查找机制，旨在简化测试数据的管理。
**原则：你只需创建数据文件，无需编写任何配置代码。**

---

## 1. 快速上手

### 添加新数据（无需修改代码）
假设你要测试一个名为 "warning" (预警) 的新模块：

1.  **创建文件**：在当前目录下 (`test_data/test_type/`) 创建文件。
2.  **命名**：必须命名为 `warning_test_data.csv`。
3.  **调用**：在代码中直接调用 `get_test_data('warning')`。

系统会自动找到该文件并加载数据。

---

## 2. 详细使用方法

### 基础调用 (最常用)
自动按照 CSV > JSON > Xlsx 的优先级查找数据。
```python
from test_data.test_data_config import get_test_data

# 自动查找 warning_test_data.*
data = get_test_data('warning')
```

### 指定格式调用 (可选)
如果你明确知道要用哪种格式：
```python
# 强制读取 warning_test_data.json
json_data = get_test_data('warning', 'json')
```

### 在 pytest 中使用
```python
import pytest
from test_data.test_data_config import get_test_data

class TestWarning:
    # 参数化测试：有多少行数据，就运行多少次测试
    @pytest.mark.parametrize("case_data", get_test_data('warning'))
    def test_warning_alert(self, driver, case_data):
        # 像字典一样使用
        title = case_data.get('title')
        print(f"当前测试标题: {title}")
```

---

## 3. 详细文件格式规范

为了确保数据能被正确读取，请严格遵守以下格式。

### CSV 格式 (推荐 ★★★★★)
*   **优点**：Git 友好，轻量级，编辑方便。
*   **要求**：
    1.  第一行必须是表头（字段名）。
    2.  必须使用 **UTF-8** 编码（防止中文乱码）。

**示例 (`warning_test_data.csv`)**:
```csv
id,title,level,expected
1,高温预警,high,show_red_alert
2,低温预警,low,show_blue_alert
```

### JSON 格式
*   **优点**：支持复杂嵌套结构。
*   **要求**：根对象通常包含一个以 `{模块名}_test_data` 命名的键，或者直接是一个数组。

**示例 (`warning_test_data.json`)**:
```json
{
  "warning_test_data": [
    {
      "id": "1",
      "title": "高温预警",
      "level": "high"
    },
    {
      "id": "2",
      "title": "低温预警",
      "level": "low"
    }
  ]
}
```

### Excel 格式
*   **优点**：适合非技术人员编辑。
*   **要求**：数据必须在 **第 1 个 Sheet** 页中；第一行为表头。

---

## 4. 常见问题解答

**Q: 我创建了文件，但报错 `FileNotFoundError: 未找到模块 xxx 的测试数据文件`？**
A: 请检查以下几点：
1.  文件名拼写是否正确？必须是 `xxx_test_data.csv` (注意是下划线)。
2.  文件扩展名是否隐藏了？（例如变成了 `file.csv.txt`）。
3.  路径是否正确？文件必须放在 `test_data/test_type/` 目录下。

**Q: CSV 读取出来全是乱码？**
A: 这是编码问题。请用记事本打开 CSV，选择“另存为”，在编码下拉框中选择 **UTF-8**。即使你用 Excel 编辑，保存时也要选择 "CSV UTF-8 (逗号分隔)" 格式。