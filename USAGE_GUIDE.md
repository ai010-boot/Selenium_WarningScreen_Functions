# 使用指南：公共登录和后台管理流程

本文档说明如何在测试中使用 **session-level 登录 fixture**（`authenticated_driver`）以及相关的公共功能。

## 一、快速开始

### 核心概念
- **`authenticated_driver` fixture**：Session 级（整个测试会话复用同一浏览器），自动执行"登录并进入后台管理"。
- **优势**：避免每个测试都重复登录，提升测试速度；减少代码重复。

---

## 二、fixture 说明

### 1. 函数级 `driver` fixture（原有）
适用于**需要隔离浏览器状态**的测试：每个测试函数开启/关闭一次浏览器。

```python
def test_isolated_login(driver):
    """每个测试都独立登录、验证和关闭浏览器；若失败自动截图"""
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(username, password)
    assert login_page.is_login_successful()
```

### 2. Session 级 `authenticated_driver` fixture（新增）
适用于**可共享同一登录会话**的多个测试：整个 pytest 会话启动一次浏览器、登录一次、进入后台，然后供多个测试复用。

```python
def test_user_management_1(authenticated_driver):
    """会话级登录和后台管理已完成，直接进行用户管理业务测试"""
    page = UserManagementPage(authenticated_driver)
    page.click_add_user_button()
    ...

def test_user_management_2(authenticated_driver):
    """复用同一浏览器和登录状态"""
    page = UserManagementPage(authenticated_driver)
    page.click_some_element()
    ...
```

---

## 三、fixture 工作流

### Session 启动时
1. 创建浏览器驱动
2. 调用 `LoginPage.login(username, password)` 登录
3. 等待 `is_login_successful()` 返回 True（超时 20 秒）
4. 调用 `MainPage.enter_backend_management()` 进入后台管理
5. 返回浏览器驱动供测试使用

### Session 结束时
- 关闭浏览器

### 若登录/进入后台失败
- 截图：`authenticated_driver_error` 或 `enter_backend_failed`
- 相关异常向上传播，测试会失败

---

## 四、配置凭据

### 方法 1：环境变量（推荐用于 CI/CD）
```bash
# PowerShell / CMD
set TEST_USERNAME=admin
set TEST_PASSWORD=Admin@123
pytest

# 或在 pytest 命令中
pytest --env TEST_USERNAME=admin --env TEST_PASSWORD=Admin@123
```

### 方法 2：修改代码默认值
编辑 `test_cases/conftest.py`：
```python
@pytest.fixture(scope='session')
def authenticated_driver(request):
    # 修改这两行的默认值
    username = os.getenv('TEST_USERNAME', 'your_default_username')
    password = os.getenv('TEST_PASSWORD', 'your_default_password')
    ...
```

---

## 五、示例代码

### 示例 1：使用 `authenticated_driver` 的最小测试
**文件：`test_cases/test_user_management_example.py`**

```python
import pytest
from pages.user_management_page import UserManagementPage

class TestUserManagementWithSharedSession:
    """使用 authenticated_driver (session-level) 的示例"""

    def test_add_user(self, authenticated_driver):
        """测试：新建用户流程"""
        page = UserManagementPage(authenticated_driver)
        
        # 点击"新建用户"按钮
        page.click(page.USER_ADD_BUTTON)
        
        # 填表...
        page.input_text(page.ACCOUNT_INPUT, 'newuser')
        page.input_text(page.NICKNAME_INPUT, '新用户')
        
        # 断言：检查某个元素是否显示
        assert page.is_element_visible(page.CONFIRM_BUTTON)

    def test_search_user(self, authenticated_driver):
        """测试：搜索用户流程（复用上一个测试的登录状态）"""
        page = UserManagementPage(authenticated_driver)
        
        # 注意：此时还在后台管理页面，浏览器状态保持登录
        # 你可以直接进行测试...
        
        pass
```

### 示例 2：使用 `driver` fixture（函数级隔离）
**文件：`test_cases/test_login_example.py`**

```python
import pytest
from pages.login_page import LoginPage

class TestLoginWithIsolation:
    """使用 driver (function-level) 的示例：每个测试独立登录/关闭"""

    def test_valid_login(self, driver):
        """测试：正确密码登录"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        login_page.login('admin', 'Admin@123')
        
        assert login_page.is_login_successful()

    def test_invalid_login(self, driver):
        """测试：错误密码登录"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        login_page.login('admin', 'wrongpassword')
        
        assert login_page.is_login_failed()
        error_msg = login_page.get_error_message()
        assert '账号或密码错误' in error_msg
```

---

## 六、推荐用法

### ✅ 何时使用 `authenticated_driver`
- 测试**后台管理功能**（用户管理、权限管理等）
- 需要**重复操作同一逻辑**的多个测试用例
- 想要**提升测试速度**、减少重复登录

### ✅ 何时使用 `driver`
- 测试**登录流程本身**（成功、失败、边界条件）
- 需要**隔离浏览器状态**的测试（例如不想被前面的测试影响）
- 需要**自定义登录逻辑或跳过登录**

---

## 七、常见问题

### Q1：`authenticated_driver` 在第一个测试之前卡住了？
**A**：检查登录凭据是否正确（环境变量或默认值）。也可查看 pytest 输出或截图 `authenticated_driver_error`。

### Q2：能否在测试中修改 `authenticated_driver` 的状态（如切换用户）？
**A**：可以。`authenticated_driver` 是普通的 WebDriver，你可以调用 `driver.get(url)` 跳转或重新登录。但要注意一旦状态改变，后续复用该 driver 的测试可能受影响。建议在 teardown 中恢复状态。

### Q3：某个测试失败了，下一个使用 `authenticated_driver` 的测试还能继续吗？
**A**：是的。`authenticated_driver` 是全局会话驱动，一个测试失败不会影响另一个测试的浏览器连接（除非异常崩溃）。pytest 会继续用同一驱动运行后续测试。

### Q4：如何只为某个测试关闭并重建浏览器？
**A**：改用 `driver` fixture（函数级）而不是 `authenticated_driver`。

---

## 八、相关页面对象方法

### `LoginPage` 
```python
from pages.login_page import LoginPage

class LoginPage(BasePage):
    def navigate_to_login(self):
        """导航到登录页"""
    
    def login(self, username, password):
        """执行登录：选择选项 → 输入用户名/密码 → 点击登录"""
    
    def is_login_successful(self):
        """检查是否登录成功"""
    
    def is_login_failed(self):
        """检查是否显示登录失败信息"""
    
    def get_success_message(self):
        """获取成功消息"""
    
    def get_error_message(self):
        """获取错误消息"""
```

### `MainPage`
```python
from pages.main_page import MainPage

class MainPage(BasePage):
    def enter_backend_management(self, timeout=5):
        """
        进入后台管理：
        - 优先尝试第一入口 (BACKEND_MANAGEMENT)
        - 失败则尝试第二入口 (BACKEND_MANAGEMENT_2)
        - 返回 True/False 表示成功/失败
        """
```

### `UserManagementPage`
```python
from pages.user_management_page import UserManagementPage

class UserManagementPage(BasePage):
    # 所有定位器已通过 UserManagementLocators 导入
    USER_ADD_BUTTON
    DEPARTMENT_SELECT
    DEPARTMENT_DROPDOWN_TOGGLE
    DEPARTMENT_FIRST_OPTION
    ROLE_SELECT
    ACCOUNT_INPUT
    NICKNAME_INPUT
    PASSWORD_INPUT
    CONFIRM_PASSWORD_INPUT
    PHONE_INPUT
    # ...更多定位器请见 locators/User_Management.py
```

---

## 九、运行示例

### 仅运行使用 `authenticated_driver` 的测试
```bash
cd d:\我的文件夹\Automated_Testing_Repositor\Selenium_WarningScreen_Functions

# 使用默认凭据（admin / Admin@123）
pytest test_cases/test_user_management_example.py -v

# 使用自定义凭据
set TEST_USERNAME=testuser
set TEST_PASSWORD=testpass123
pytest test_cases/test_user_management_example.py -v
```

### 仅运行使用 `driver` 的测试
```bash
pytest test_cases/test_login_example.py -v
```

### 运行所有测试
```bash
pytest test_cases/ -v --tb=short
```

---

## 十、最佳实践

1. **在 `authenticated_driver` 的多个测试中，避免互相污染状态**
   - 测试 A 若修改了浏览器状态（跳转 URL、刷新页面），在 teardown 中恢复
   - 或在下个测试的 setup 中显式导航到预期页面

2. **坚持 Page Object 模式**
   - 所有定位器放在 `locators/` 目录
   - 所有页面操作放在 `pages/` 目录
   - 测试中只调用页面方法，不直接操作定位器

3. **使用有意义的测试数据**
   - 若数据驱动，将测试数据集中管理（CSV、JSON 等）
   - 避免在测试代码中硬编码账号密码

4. **充分使用日志和截图**
   - BasePage 已内置 logger；在关键步骤调用 logger.info()
   - 测试失败会自动截图；覆盖在 conftest.py 中

---

更多问题或反馈，请参考 [QUICKSTART.md](QUICKSTART.md)。
