# Selenium POM 自动化测试项目

## 项目简介
这是一个基于 Page Object Model (POM) 设计模式的企业级 Selenium 自动化测试框架。

## 项目结构
```
selenium-pom-project/
├── config/                 # 配置文件
├── drivers/               # 浏览器驱动
├── pages/                 # 页面对象
├── test_cases/            # 测试用例
├── test_data/             # 测试数据
├── utils/                 # 工具类
├── reports/               # 测试报告
├── locators/              # 元素定位器
└── requirements.txt       # 依赖包
```

## 环境要求
- Python 3.8+
- pip

## 安装步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 下载浏览器驱动
- Chrome: https://chromedriver.chromium.org/
- Firefox: https://github.com/mozilla/geckodriver/releases
- Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

将驱动文件放到 `drivers/` 目录

### 3. 配置环境
编辑 `config/config.py` 设置测试环境参数

## 运行测试

### 运行所有测试
```bash
pytest test_cases/
```

### 运行指定测试文件
```bash
pytest test_cases/test_login.py
```

### 运行冒烟测试
```bash
pytest -m smoke
```

### 指定浏览器运行
```bash
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge
```

### 生成 HTML 报告
```bash
pytest --html=reports/html/report.html --self-contained-html
```

### 生成 Allure 报告
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 目录说明

### config/
存放配置文件，支持多环境配置

### pages/
存放页面对象类，每个页面一个类文件

### test_cases/
存放测试用例，按功能模块组织

### test_data/
存放测试数据（JSON、Excel、Python 文件）

### utils/
存放公共工具类（日志、截图、数据读取等）

### reports/
存放测试报告和日志文件

## 编写测试用例示例

```python
from pages.login_page import LoginPage

def test_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login("username", "password")
    assert login_page.is_login_successful()
```

## 最佳实践

1. **单一职责**: 每个 Page 类只负责一个页面
2. **元素定位分离**: 使用 locators 目录或在 Page 类中定义常量
3. **复用 BasePage**: 所有公共方法在 BasePage 中实现
4. **数据驱动**: 使用外部数据文件进行参数化测试
5. **日志记录**: 关键操作记录日志便于调试
6. **截图保存**: 失败用例自动截图

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
- Python 3.x

## 作者
shizhuo

## 许可证
无
