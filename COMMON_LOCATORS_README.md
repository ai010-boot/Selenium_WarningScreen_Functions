# 核心公共定位器说明

## 📌 核心定义

本项目中有 **两个核心的公共定位器文件**，它们是整个测试框架的基础，被所有测试直接或间接依赖：

1. **`locators/login_locators.py`** - 登录页面定位器
2. **`locators/Backstage_management_entry.py`** - 后台管理入口定位器

---

## 🔐 为什么是公共的？

### 登录流程是所有测试的前置条件
- 任何功能测试都需要先**登录**
- `session-level authenticated_driver` fixture 使用 `LoginPageLocators`
- 登录定位器修改会影响所有依赖 `authenticated_driver` 的测试

**关键文件**：
- `pages/login_page.py` 依赖 `LoginPageLocators`
- `test_cases/conftest.py` 通过 `LoginPage.login()` 执行公共登录流程

### 进入后台是所有业务测试的前置条件
- 所有后台功能测试都需要先**进入后台管理**
- `session-level authenticated_driver` fixture 使用 `BackstageManagementEntry`
- 后台入口定位器修改会影响所有依赖 `authenticated_driver` 的测试

**关键文件**：
- `pages/main_page.py` 依赖 `BackstageManagementEntry`
- `test_cases/conftest.py` 通过 `MainPage.enter_backend_management()` 执行公共进入后台流程

---

## 📋 定位器列表

### 1. LoginPageLocators (`locators/login_locators.py`)

| 定位器 | 说明 | 值 |
|--------|------|-----|
| `LOGIN_OPTIONS` | 登录选项切换 | `(By.ID, "tab-password")` |
| `USERNAME_INPUT` | 用户名/账号输入框 | `(By.XPATH, "//input[@placeholder='账号']")` |
| `PASSWORD_INPUT` | 密码输入框 | `(By.XPATH, "//input[@placeholder='密码']")` |
| `LOGIN_BUTTON` | 登录按钮 | `(By.XPATH, "//button[@type='button']//span[1]")` |
| `PROMPT_MESSAGE` | 登录消息提示（成功/失败） | `(By.XPATH, "//p[@class='el-message__content']")` |

**使用场景**：
- 登录功能测试（`test_cases/test_login_csv_driven.py`）
- `authenticated_driver` fixture（`test_cases/conftest.py`）

---

### 2. BackstageManagementEntry (`locators/Backstage_management_entry.py`)

| 定位器 | 说明 | 值 |
|--------|------|-----|
| `BACKEND_MANAGEMENT` | 后台管理入口（图标） | `(By.XPATH, "(//img)[1]")` |
| `BACKEND_MANAGEMENT_2` | 后台管理入口（菜单项） | `(By.XPATH, "(//li[@role='menuitem'])[1]")` |

**使用场景**：
- 所有业务功能测试的前置（进入后台）
- `authenticated_driver` fixture（`test_cases/conftest.py`）
- `MainPage.enter_backend_management()`

---

## ⚠️ 重要提示

### ✅ DO（应该做）

1. **使用这两个定位器文件**，不要复制或重新定义
   ```python
   # ✓ 正确做法
   from locators.login_locators import LoginPageLocators
   from locators.Backstage_management_entry import BackstageManagementEntry
   ```

2. **在页面对象中导入并使用**
   ```python
   # pages/login_page.py
   class LoginPage(BasePage):
       USERNAME_INPUT = LoginPageLocators.USERNAME_INPUT
       PASSWORD_INPUT = LoginPageLocators.PASSWORD_INPUT
   
   # pages/main_page.py
   class MainPage(BasePage):
       BACKEND_MANAGEMENT = BackstageManagementEntry.BACKEND_MANAGEMENT
   ```

3. **修改这两个文件时要谨慎**
   - 修改前检查所有依赖者
   - 修改后运行 smoke 测试验证登录和后台进入流程

### ❌ DO NOT（不应该做）

1. **不要在其他定位器文件中重复定义登录或后台入口定位器**
   ```python
   # ✗ 不要这样做！
   class UserManagementLocators:
       LOGIN_BUTTON = (By.XPATH, "...")  # 应该从 LoginPageLocators 导入
   ```

2. **不要在测试中直接使用原始 XPath，需要通过定位器**
   ```python
   # ✗ 错误做法
   driver.find_element(By.XPATH, "//button[@type='button']//span[1]")
   
   # ✓ 正确做法
   page.find_element(LoginPageLocators.LOGIN_BUTTON)
   ```

3. **不要复制登录或后台进入的实现逻辑**
   ```python
   # ✗ 每个测试中重复写登录逻辑
   def test_xxx(driver):
       login_page = LoginPage(driver)
       login_page.navigate_to_login()
       login_page.login('admin', 'Admin@123')  # ← 重复
       # ... 下面才是你的功能测试
   
   # ✓ 改用 authenticated_driver fixture
   def test_xxx(authenticated_driver):
       # 登录和进入后台已自动完成
       page = UserManagementPage(authenticated_driver)
       page.click(page.USER_ADD_BUTTON)  # 直接开始功能测试
   ```

---

## 🔄 使用流程图

```
pytest 启动
  ↓
conftest.py: authenticated_driver fixture 初始化
  ↓
[1] 创建浏览器驱动 (DriverFactory.get_driver)
  ↓
[2] LoginPage(driver).login(username, password)
    ├→ navigate_to_login()
    ├→ click(LoginPageLocators.LOGIN_OPTIONS)
    ├→ input(LoginPageLocators.USERNAME_INPUT, username)
    ├→ input(LoginPageLocators.PASSWORD_INPUT, password)
    ├→ click(LoginPageLocators.LOGIN_BUTTON)
    └→ 验证 is_login_successful()
  ↓
[3] MainPage(driver).enter_backend_management()
    ├→ 尝试 click(BackstageManagementEntry.BACKEND_MANAGEMENT)
    └→ 若失败，尝试 click(BackstageManagementEntry.BACKEND_MANAGEMENT_2)
  ↓
✓ 返回已登录 + 已进入后台的 driver
  ↓
测试执行（直接使用该 driver）
  ↓
[测试1] test_xxx(authenticated_driver) → 复用已登录 driver
[测试2] test_yyy(authenticated_driver) → 复用已登录 driver
[测试3] ...
  ↓
会话结束，关闭浏览器
```

---

## 📝 修改公共定位器的清单

若需修改 `LoginPageLocators` 或 `BackstageManagementEntry`：

- [ ] 更新定位器文件
- [ ] 更新本文档中的定位器列表
- [ ] 运行登录功能测试验证
  ```bash
  pytest test_cases/test_login_csv_driven.py -v
  ```
- [ ] 运行依赖 `authenticated_driver` 的所有测试
  ```bash
  pytest test_cases/ -k "authenticated_driver" -v
  ```
- [ ] 确保没有其他地方重复定义这些定位器

---

## 🎯 总结

| 方面 | 说明 |
|------|------|
| **核心公共文件** | `login_locators.py`, `Backstage_management_entry.py` |
| **页面对象** | `pages/login_page.py`, `pages/main_page.py` |
| **Fixture** | `test_cases/conftest.py: authenticated_driver` |
| **影响范围** | 所有使用 `authenticated_driver` 的测试 |
| **修改风险** | 高（影响全局），需谨慎 |
| **维护方式** | 集中管理，统一版本 |

---

有问题或需要更新定位器？请先检查本文档，确保遵循上述规范。
