# 新增业务开发指南 (Development Guide)

本文档是针对开发者的操作指南，详细说明了如何向自动化测试框架中**添加一个新的页面业务**。

当你要测试一个新的页面功能时，请严格按照以下 **4 个步骤** 进行开发：

---

## 步骤 1：定义元素定位 (Locators)
**目标**：将页面上的元素（输入框、按钮等）的定位方式集中管理。

1.  在 `locators/` 目录下创建一个新的 Python 文件，命名格式为 `{module}_locators.py`。
2.  创建一个类，建议命名为 `{Module}PageLocators`。
3.  在该类中定义静态变量，使用 `(By.XXX, "value")` 的元组形式。

**示例代码 (`locators/warning_locators.py`)**:
```python
from selenium.webdriver.common.by import By

class WarningPageLocators:
    """预警大屏页面的元素定位器"""
    
    # 例如：预警列表的标题
    TITLE = (By.XPATH, "//h1[@class='page-title']")
    # 例如：某个具体的预警卡片
    WARNING_CARD = (By.CLASS_NAME, "warning-card")
    # 例如：导出按钮
    EXPORT_BTN = (By.ID, "btn-export")
```

---

## 步骤 2：创建页面对象 (Page Objects)
**目标**：封装页面的业务逻辑（点击、输入、获取文本等），不包含断言。

1.  在 `pages/` 目录下创建一个新的 Python 文件，命名格式为 `{module}_page.py`。
2.  创建一个类，继承自 `BasePage`。
3.  引入步骤 1 中定义的定位器。
4.  编写具体的操作方法（如 `click_export()`）。

**示例代码 (`pages/warning_page.py`)**:
```python
from pages.base_page import BasePage
from locators.warning_locators import WarningPageLocators

class WarningPage(BasePage):
    """预警大屏页面对象"""

    # 引用定位器
    TITLE = WarningPageLocators.TITLE
    EXPORT_BTN = WarningPageLocators.EXPORT_BTN

    def get_page_title(self):
        """获取页面标题"""
        return self.get_text(self.TITLE)

    def click_export_button(self):
        """点击导出按钮"""
        self.click(self.EXPORT_BTN)
        self.logger.info("点击了导出按钮")
```

---

## 步骤 3：准备测试数据 (Test Data)
**目标**：将测试数据与代码分离，实现数据驱动。

1.  在 `test_data/test_type/` 目录下创建一个数据文件。
2.  命名格式必须为 `**{module}_test_data.csv**` (推荐使用 CSV)。
3.  第一行为表头，包含字段名；后续行为具体的测试数据。

**示例文件 (`test_data/test_type/warning_test_data.csv`)**:
```csv
test_case,expected_title,description
ui_check_01,预警监控中心,检查标题是否正确
export_check_01,导出成功,测试导出功能
```

---

## 步骤 4：编写测试用例 (Test Cases)
**目标**：编写具体的测试逻辑，组合页面操作并进行断言。

1.  在 `test_cases/` 目录下创建一个新的 Python 文件，命名格式为 `test_{module}.py`。
2.  使用 `pytest` 编写测试函数或测试类。
3.  使用 `TestDataConfig.load_test_data('{module}')` 读取数据。

**示例代码 (`test_cases/test_warning.py`)**:
```python
import pytest
from pages.warning_page import WarningPage
from test_data.test_data_config import TestDataConfig

class TestWarningScreen:
    
    # 自动加载 'warning' 模块的数据
    @pytest.mark.parametrize("data", TestDataConfig.load_test_data('warning'))
    def test_warning_function(self, driver, data):
        """
        测试预警大屏功能
        """
        warning_page = WarningPage(driver)
        
        # 1. 业务操作
        # (假设已经登录，这里直接验证)
        
        # 2. 验证逻辑
        actual_title = warning_page.get_page_title()
        expected = data['expected_title']
        
        # 3. 断言
        assert actual_title == expected, f"标题不匹配，期望：{expected}，实际：{actual_title}"
        
        print(f"✓ 测试通过: {data['description']}")
```

---

## 总结：开发流程检查清单

- [ ] **Locators**: `locators/{module}_locators.py` 是否已创建？
- [ ] **Pages**: `pages/{module}_page.py` 是否已继承 BasePage？
- [ ] **Data**: `test_data/test_type/{module}_test_data.csv` 是否存在？
- [ ] **TestCase**: `test_cases/test_{module}.py` 是否编写了断言？

完成后，运行以下命令验证：
```bash
python run_tests.py file test_cases/test_{module}.py
```