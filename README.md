# Selenium Warning Screen Functions - 自动化测试项目

## 项目简介
这是一个基于 **Page Object Model (POM)** 设计模式的企业级 Selenium 自动化测试框架,主要用于 **AIOT 预警大屏 (Warning Screen Functions)** 的功能测试。

### 核心特性
- ✅ **定位器集中管理** - 元素定位与页面逻辑分离,易于维护
- ✅ **数据驱动测试** - 支持 CSV/JSON/Excel 数据源,无需修改代码即可扩展测试场景
- ✅ **约定优于配置** - 遵循命名约定,减少配置工作
- ✅ **POM 最佳实践** - 职责清晰分离,代码复用性高
- ✅ **多报告支持** - Pytest HTML、HTMLReport、Allure 三种专业报告格式
- ✅ **并行执行** - 支持多进程并行测试,大幅提升执行效率

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
│   └── __init__.py
├── test_cases/            # 测试用例
│   ├── conftest.py        # pytest配置
│   ├── test_login_csv_driven.py  # 数据驱动登录测试
│   ├── 测试用例说明.txt    # 用例详细说明
│   └── examples/          # 示例文件（参考代码）
├── test_data/             # 测试数据（自动查找）
│   ├── test_data_config.py  # 数据加载引擎
│   ├── README_数据驱动.txt # 数据驱动说明
│   ├── test_type/         # 数据文件目录
│   │   ├── login_test_data.csv   # CSV格式测试数据
│   │   └── USAGE.md      # 数据使用说明
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
- Chrome 浏览器 (推荐)

## 安装步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
编辑 `config/config.py` 可调整以下参数(浏览器驱动由 webdriver-manager 自动管理):

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `BASE_URL` | `https://aiot.aiysyd.cn/screen/login` | 测试环境地址 |
| `BROWSER` | `chrome` | 浏览器类型 (chrome/firefox/edge) |
| `HEADLESS` | `True` | 无头模式(True=后台运行,False=显示浏览器) |
| `IMPLICIT_WAIT` | `5` | 隐式等待时间(秒) |
| `EXPLICIT_WAIT` | `10` | 显式等待时间(秒) |

## 运行测试

### 快速命令
```bash
# 基础运行
python run_tests.py all                                    # 运行所有测试
python run_tests.py smoke                                  # 运行冒烟测试(快速验证)
python run_tests.py file test_cases/test_login_csv_driven.py  # 运行指定文件

# 并行执行(推荐,大幅提速)
python run_tests.py parallel 4                             # 4个进程并行运行
```

### 性能优化建议

**提升测试速度的方法**:

1. **启用无头模式** (速度提升 30-50%)
   ```python
   # config/config.py
   HEADLESS = True  # 后台运行,不显示浏览器窗口
   ```

2. **并行执行** (速度提升 2-4倍)
   ```bash
   python run_tests.py parallel 4  # 根据CPU核心数调整进程数
   ```

3. **只运行关键测试**
   ```bash
   python run_tests.py smoke  # 只运行标记为 @pytest.mark.smoke 的用例
   ```

## 报告系统

本项目支持**三种**测试报告格式，运行测试后自动生成：

### 1. Pytest HTML 报告（简单实用）
**位置**: `reports/html/report.html`  
**查看方式**: 直接用浏览器打开

**特点**:
- 📄 完整的测试结果统计
- 📝 每个用例的详细日志
- 🖼️ 失败时的截图附件
- 💡 自包含HTML，便于分享

### 2. HTMLReport 报告（现代美观）
**位置**: `reports/html_report/report.html`  
**查看方式**: 直接用浏览器打开

**特点**:
- 🎨 现代化UI设计
- 🌐 支持中英文切换
- 📊 清晰的测试结果展示
- ⚡ 轻量级（约83KB）

### 3. Allure 报告（专业推荐）
**位置**: `reports/allure-results/` (原始数据) 和 `reports/allure-html/` (生成的HTML报告)

**查看方式**:

> ⚠️ **重要**: Allure 报告不能直接用浏览器打开 `file://` 协议的 HTML 文件,会因为跨域限制导致 404 错误或一直显示 "Loading..."。必须使用以下命令之一:

**方法 1: 打开已生成的 HTML 报告**(启动本地服务器)
```bash
allure open reports/allure-html
```

**方法 2: 直接从测试结果生成并打开**(推荐)
```bash
allure serve reports/allure-results
```

**特点**:
- ✨ 专业级交互式报告
- 📈 详细的测试执行图表和趋势分析
- 📊 支持测试步骤分解和时间线展示
- 🔍 强大的筛选和搜索功能
- 👥 最适合团队协作和持续集成

> **提示**: 查看 Allure 报告需先安装 Allure 命令行工具。参考: [Allure 安装指南](https://docs.qameta.io/allure/#_installing_a_commandline)

## 最佳实践与扩展

### 数据驱动
本项目核心采用数据驱动模式，测试数据存放于 `test_data/test_type/` 目录。
例如 `login_test_data.csv` 控制登录测试的各种场景（成功、失败、异常等）。
如需添加新数据，只需修改 CSV 文件即可，无需修改代码。

### 添加新页面测试
1. **创建定位器**: 在 `locators/` 下创建 `xxx_locators.py`。
2. **创建页面对象**: 在 `pages/` 下创建 `xxx_page.py`，继承 `BasePage`。
3. **创建测试数据**: 在 `test_data/test_type/` 下创建对应数据文件。
4. **编写测试用例**: 在 `test_cases/` 下创建 `test_xxx.py`。

更多示例请参考 `test_cases/examples/` 目录。

## 技术栈

### 核心框架
- **Python 3.8+** - 编程语言
- **Selenium WebDriver 4.x** - 浏览器自动化引擎
- **pytest** - 测试框架
- **webdriver-manager** - 自动管理浏览器驱动

### 测试报告
- **Allure Report** - 专业级交互式报告(推荐)
- **pytest-html** - 简洁实用的HTML报告
- **pytest-html-reporter** - 现代化UI报告

### 设计模式
- **Page Object Model (POM)** - 页面对象模式
- **Data-Driven Testing** - 数据驱动测试

## 常见问题

### Q: 如何查看浏览器执行过程?
A: 修改 `config/config.py` 中的 `HEADLESS = False`,测试时会显示浏览器窗口。

### Q: 测试运行太慢怎么办?
A: 使用并行执行 `python run_tests.py parallel 4` 或启用无头模式 `HEADLESS = True`。

### Q: Allure 报告显示 404 错误?
A: 不能直接双击打开,需要使用命令 `allure open reports/allure-html` 或 `allure serve reports/allure-results`。

### Q: 如何添加新的测试数据?
A: 编辑 `test_data/test_type/login_test_data.csv`,添加新行即可,无需修改代码。

## 项目维护

- **作者**: 自动化测试团队
- **测试对象**: AIOT 预警大屏系统
- **更新日期**: 2026-01-30