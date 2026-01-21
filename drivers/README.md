# 浏览器驱动目录

## 说明
此目录用于存放浏览器驱动程序。

## 支持的浏览器驱动

### Chrome
- 下载地址: https://chromedriver.chromium.org/
- 文件名: chromedriver.exe (Windows) 或 chromedriver (Linux/Mac)
- 版本要求: 与 Chrome 浏览器版本匹配

### Firefox
- 下载地址: https://github.com/mozilla/geckodriver/releases
- 文件名: geckodriver.exe (Windows) 或 geckodriver (Linux/Mac)
- 版本要求: 与 Firefox 浏览器版本兼容

### Edge
- 下载地址: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
- 文件名: msedgedriver.exe (Windows) 或 msedgedriver (Linux/Mac)
- 版本要求: 与 Edge 浏览器版本匹配

## 安装步骤

1. 检查浏览器版本
2. 下载对应版本的驱动
3. 将驱动文件复制到此目录
4. 确保驱动文件有执行权限（Linux/Mac）

## Linux/Mac 权限设置

```bash
chmod +x drivers/chromedriver
chmod +x drivers/geckodriver
chmod +x drivers/msedgedriver
```

## 注意事项

- 驱动版本必须与浏览器版本匹配
- 定期更新驱动以支持最新浏览器
- 可以使用 webdriver-manager 自动管理驱动
