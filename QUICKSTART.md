# 快速开始指南

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

## 3. 配置浏览器驱动

### 方法一：手动下载（推荐用于企业环境）
1. 下载对应浏览器的驱动：
   - Chrome: https://chromedriver.chromium.org/
   - Firefox: https://github.com/mozilla/geckodriver/releases
   - Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

2. 将驱动文件放到 `drivers/` 目录

3. 确保驱动版本与浏览器版本匹配

### 方法二：使用 webdriver-manager（可选）
```bash
pip install webdriver-manager
```

然后在 `utils/driver_factory.py` 中启用自动管理。

## 4. 配置测试环境

### 复制环境变量文件
```bash
cp .env.example .env
```

### 编辑配置
修改 `config/config.py` 或 `.env` 文件中的：
- BASE_URL：测试环境地址
- TEST_USER：测试账号信息
- 其他必要配置

## 5. 运行测试

### 运行所有测试
```bash
pytest test_cases/
```

### 运行冒烟测试
```bash
pytest -m smoke
```

### 运行指定测试文件
```bash
pytest test_cases/test_login.py
```

### 指定浏览器
```bash
pytest --browser=chrome
pytest --browser=firefox
```

### 生成测试报告
```bash
pytest --html=reports/html/report.html --self-contained-html
```

### 使用运行脚本
```bash
# 运行所有测试
python run_tests.py all

# 运行冒烟测试
python run_tests.py smoke

# 并行运行（4个进程）
python run_tests.py parallel 4
```

## 6. 查看测试报告

测试报告位于 `reports/` 目录：
- HTML 报告：`reports/html/report.html`
- 截图：`reports/screenshots/`
- 日志：`reports/logs/`

## 7. 常见问题

### Q: 找不到元素
A: 
- 检查元素定位器是否正确
- 增加等待时间
- 使用显式等待

### Q: 驱动版本不匹配
A:
- 确保浏览器驱动版本与浏览器版本匹配
- 使用 webdriver-manager 自动管理

### Q: 测试失败
A:
- 查看 `reports/logs/` 中的日志
- 查看 `reports/screenshots/` 中的截图
- 检查测试环境是否正常

## 8. 下一步

- 查看 `README.md` 了解更多详细信息
- 阅读 `pages/` 目录中的页面对象示例
- 参考 `test_cases/` 目录中的测试用例示例
- 根据实际项目修改配置和测试用例

## 9. 最佳实践

1. 使用虚拟环境隔离依赖
2. 定期更新浏览器驱动
3. 编写可维护的测试用例
4. 使用有意义的测试用例名称
5. 及时查看测试报告和日志
6. 不要在版本控制中提交敏感信息

祝测试顺利！
