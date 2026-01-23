# Selenium POM 自动化测试项目

## 项目简介
这是一个基于 Page Object Model (POM) 设计模式的企业级 Selenium 自动化测试框架。

### 核心特性
- ✅ **定位器集中管理** - 元素定位与页面逻辑分离
- ✅ **数据驱动自动化** - 无需配置，自动查找测试数据
- ✅ **约定优于配置** - 遵循命名约定，减少配置工作
- ✅ **多格式支持** - CSV/JSON/Excel 数据源
- ✅ **POM 最佳实践** - 职责分离，易于维护
- ✅ **多报告支持** - Allure、Pytest HTML、HTMLReport 三种报告格式

## 项目结构
```
Selenium_WarningScreen_Functions/
├── config/                 # 配置文件
│   ├── config.py          # 主配置（URL、环境等）
│   └── __init__.py
├── locators/              # 元素定位器（集中管理）
│   ├── login_locators.py  # 登录页定位器
│   └── __init__.py
├── pages/                 # 页面对象
│   ├── base_page.py       # 基础页面类
│   ├── login_page.py      # 登录页对象
│   ├── home_page.py       # 首页对象
│   └── __init__.py
├── test_cases/            # 测试用例
│   ├── conftest.py        # pytest配置
│   ├── test_login_csv_driven.py  # 数据驱动测试
│   ├── test_login.py      # 传统测试（已注释）
│   └── examples/          # 示例文件
├── test_data/             # 测试数据（自动查找）
│   ├── test_data_config.py  # 数据加载引擎
│   ├── test_type/         # 数据文件目录
│   │   ├── login_test_data.csv   # CSV格式
│   │   ├── login_test_data.json  # JSON格式
│   │   └── login_test_data.xlsx  # Excel格式
│   └── __init__.py
├── utils/                 # 工具类
│   ├── driver_factory.py  # 驱动管理
│   ├── logger.py          # 日志工具
│   ├── screenshot.py      # 截图工具
│   └── excel_reader.py    # Excel读取
├── drivers/               # 浏览器驱动
├── reports/               # 测试报告
│   ├── allure-results/    # Allure结果文件
│   ├── html/              # Pytest HTML生成的报告
│   ├── html_report/       # HTMLReport生成的报告
│   ├── screenshots/       # 失败截图
│   └── logs/              # 日志文件
├── pytest.ini             # pytest配置
├── requirements.txt       # 依赖包
└── run_tests.py           # 测试运行脚本
```

## 环境要求
- Python 3.8+
- pip

## 安装步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
编辑 `config/config.py` 设置测试环境参数（浏览器驱动由 webdriver-manager 自动管理）

## 运行测试

### 快速命令
```bash
python run_tests.py all                                    # 运行所有测试
python run_tests.py smoke                                  # 运行冒烟测试
python run_tests.py regression                             # 运行回归测试
python run_tests.py parallel 4                             # 并行运行（4个进程）
python run_tests.py file test_cases/test_login_csv_driven.py  # 运行指定文件
```

## 报告系统

本项目支持**四种**测试报告格式，所有报告都会自动生成：

### 1. Allure 报告（推荐）
```bash
allure serve reports/allure-results/
```
- ✨ 提供详细的测试执行图表
- 📊 支持测试步骤分解
- 🎨 交互式报告界面（最专业）

### 2. HTMLTestRunner 报告
```
reports/htmltestrunner/report.html
```
- 🏢 企业级报告风格
- 📈 统计数据清晰
- 📝 支持详细日志

### 3. BeautifulReport 报告
```
reports/beautifulreport/report.html
```
- 🌈 界面简洁美观
- 📱 响应式设计
- 💾 支持报告缓存

### 4. HTMLReport 报告
```
reports/html_report/report.html
```
- ⚡ 生成速度快
- 📄 自包含HTML
- 🔍 便于远程查看

**所有报告都会自动生成，无需配置！**

## 最佳实践

### 架构设计
1. **定位器集中管理** - 所有元素定位在 `locators/` 目录
2. **单一职责** - 每个 Page 类只负责一个页面
3. **复用 BasePage** - 所有公共方法在 BasePage 中实现
4. **约定优于配置** - 遵循命名约定，减少配置

### 数据驱动
5. **自动查找数据** - 无需配置，自动查找 `{module}_test_data.*`
6. **多格式支持** - 使用 CSV/JSON/Excel 任一格式
7. **参数化测试** - 使用 `@pytest.mark.parametrize` 和测试数据

### 测试管理
8. **日志记录** - 关键操作记录日志便于调试
9. **失败截图** - 测试失败时自动截图
10. **测试隔离** - 每个测试使用独立的浏览器实例
11. **多报告输出** - 同时生成三种报告格式便于多维度分析

## 添加新页面测试

### 步骤1: 创建定位器
```python
# locators/home_locators.py
from selenium.webdriver.common.by import By

class HomePageLocators:
    """首页元素定位器"""
    WELCOME_TEXT = (By.ID, "welcome")
    LOGOUT_BUTTON = (By.XPATH, "//button[@id='logout']")
```

### 步骤2: 创建页面对象
```python
# pages/home_page.py
from pages.base_page import BasePage
from locators.home_locators import HomePageLocators

class HomePage(BasePage):
    """首页页面对象"""
    
    WELCOME_TEXT = HomePageLocators.WELCOME_TEXT
    LOGOUT_BUTTON = HomePageLocators.LOGOUT_BUTTON
    
    def get_welcome_text(self):
        return self.get_element_text(self.WELCOME_TEXT)
```

### 步骤3: 创建测试数据
```csv
# test_data/test_type/home_test_data.csv
test_case,expected_text,description
valid_user,欢迎回来,有效用户首页显示
```

### 步骤4: 编写测试用例
```python
# test_cases/test_home.py
import pytest
from pages.home_page import HomePage
from test_data.test_data_config import get_test_data

@pytest.mark.parametrize("test_case", get_test_data('home'))
def test_home(driver, test_case):
    home_page = HomePage(driver)
    # ... 测试逻辑
```

**无需任何配置，自动工作！**

## 常见问题

### 1. 驱动版本不匹配
确保浏览器驱动版本与浏览器版本匹配

### 2. 元素定位失败
- 增加等待时间
- 检查定位器是否正确
- 使用显式等待

### 3. 并发执行
使用 pytest-xdist 插件：
```bash
pip install pytest-xdist
pytest -n 4  # 4个进程并行
```

## 技术栈
- Selenium WebDriver
- pytest
- Allure Report
- HTMLReport
- Pytest HTML
- Python 3.x

## 作者
shizhuo

## 许可证
无