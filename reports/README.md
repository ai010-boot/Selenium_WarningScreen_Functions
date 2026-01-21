# 测试报告目录

此目录用于存放测试执行生成的各类报告和输出文件。

## 目录结构

```
reports/
├── html/           # HTML 测试报告
├── screenshots/    # 测试截图
├── logs/          # 测试日志
└── allure-results/ # Allure 报告数据（如果使用 Allure）
```

## 文件说明

### html/
- 存放 pytest-html 生成的测试报告
- 文件格式: .html
- 可以直接用浏览器打开查看

### screenshots/
- 存放测试失败时的截图
- 文件格式: .png
- 文件名包含测试用例名称和时间戳

### logs/
- 存放测试执行日志
- 文件格式: .log
- 包含详细的测试执行信息

### allure-results/
- Allure 测试报告的原始数据
- 需要使用 Allure 命令生成可视化报告

## 清理报告

定期清理旧的报告文件以节省磁盘空间：

```bash
# 清理所有报告
rm -rf reports/html/*.html
rm -rf reports/screenshots/*.png
rm -rf reports/logs/*.log
```

## 注意事项

- 报告文件不应提交到版本控制系统
- .gitignore 已配置忽略报告文件
- 测试完成后及时查看报告
