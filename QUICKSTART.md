# 快速开始指南

## 项目特性

✅ **定位器集中管理** - 元素定位与页面逻辑分离  
✅ **数据驱动自动化** - 无需配置，自动查找测试数据  
✅ **约定优于配置** - 遵循命名约定，减少配置工作  
✅ **多格式支持** - CSV/JSON/Excel 数据源  
✅ **POM 最佳实践** - 职责分离，易于维护

## 1. 环境准备

### 安装 Python
确保已安装 Python 3.8 或更高版本：
```bash
python --version
```

### 克隆或下载项目
```bash
# 如果是 Git 仓库
git clone <repository_url>
cd selenium-pom-project

# 或直接解压下载的项目包
```

## 2. 安装依赖

### 创建虚拟环境（推荐）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 安装依赖包
```bash
pip install -r requirements.txt
```

## 3. 配置测试环境

修改 `config/config.py` 中的配置：

```python
# 浏览器配置
BROWSER = 'chrome'           # chrome, firefox, edge
HEADLESS = True              # 是否无头模式

# 测试用户
TEST_USER = {
    'username': 'jkcsdw',
    'password': '123456'
}

# 测试 URL
BASE_URL = 'https://aiot.aiysyd.cn/screen/login'
```

## 4. 运行测试

### 使用快速命令
```bash
# 运行所有测试
python run_tests.py all

# 运行冒烟测试
python run_tests.py smoke

# 运行回归测试
python run_tests.py regression

# 并行运行测试（4个进程）
python run_tests.py parallel

# 运行指定测试文件
python run_tests.py file test_cases/test_login_csv_driven.py
```

## 5. 查看测试报告

项目支持**四种**报告格式，所有报告都会自动生成：

### Allure 报告（推荐）
```bash
allure serve reports/allure-results/
```
📊 最专业的报告界面，提供详细的测试分析

### HTMLTestRunner 报告
```
reports/htmltestrunner/report.html
```
企业级报告风格，统计数据清晰

### BeautifulReport 报告  
```
reports/beautifulreport/report.html
```
界面简洁美观，响应式设计

### HTMLReport 报告
```
reports/html_report/report.html
```
生成速度快，自包含HTML，便于远程查看

## 6. 编写数据驱动测试

### 数据文件命名规范
```
test_data/test_type/{module_name}_test_data.{csv|json|xlsx}
```

### 示例
```python
import pytest
from test_data.test_data_config import TestDataConfig

data = TestDataConfig.load_test_data('login')

@pytest.mark.parametrize("test_case", data)
def test_login(self, driver, test_case):
    username = test_case['username']
    password = test_case['password']
    # 测试代码...
```

## 7. 项目结构说明

```
├── config/                    # 配置文件
│   └── config.py             # 全局配置
├── locators/                  # 元素定位器
│   └── {module}_locators.py
├── pages/                     # 页面对象
│   ├── base_page.py
│   └── {module}_page.py
├── test_cases/                # 测试用例
│   ├── conftest.py
│   └── test_*.py
├── test_data/                 # 测试数据
│   ├── test_data_config.py
│   └── test_type/             # 数据文件位置
├── utils/                     # 工具类
│   ├── driver_factory.py
│   ├── logger.py
│   ├── screenshot.py
│   └── excel_reader.py
├── reports/                   # 测试报告
│   ├── allure-results/
│   ├── html/
│   ├── html_report/
│   └── screenshots/
└── drivers/                   # 浏览器驱动
```
