"""
测试执行脚本
提供便捷的测试运行入口
支持的报告格式：Allure、HTMLTestRunner、BeautifulReport、HTMLReport
"""
import sys
import os
import pytest
import json
from datetime import datetime
from typing import Optional
from pathlib import Path
from config.config import Config


def _is_module_available(mod_name: str) -> bool:
    """检查模块是否可用"""
    try:
        __import__(mod_name)
        return True
    except Exception:
        return False


def _generate_htmltestrunner_report(test_results_json: Optional[str] = None) -> None:
    """
    使用 HTMLTestRunner 生成报告
    """
    try:
        Config.HTMLTESTRUNNER_DIR.mkdir(parents=True, exist_ok=True)
        report_path = Config.HTMLTESTRUNNER_DIR / "report.html"
        
        # 简单的 HTML 模板
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        html_lines = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '  <meta charset="utf-8">',
            '  <title>HTMLTestRunner Report</title>',
            '  <style>',
            '    body { font-family: Arial, sans-serif; margin: 20px; }',
            '    .header { background-color: #333; color: white; padding: 15px; }',
            '  </style>',
            '</head>',
            '<body>',
            '  <div class="header">',
            '    <h1>HTMLTestRunner Report</h1>',
            f'    <p>Generated on: {timestamp}</p>',
            '  </div>',
            '  <p>Test report generated successfully.</p>',
            '</body>',
            '</html>'
        ]
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_lines))
        
        print(f"✓ HTMLTestRunner 报告已生成: {report_path}")
    except Exception as e:
        print(f"⚠ HTMLTestRunner 报告生成失败: {e}")


def _generate_beautifulreport(test_results_file: Optional[str] = None) -> None:
    """
    使用 BeautifulReport 生成报告
    """
    try:
        Config.BEAUTIFULREPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = Config.BEAUTIFULREPORT_DIR / "report.html"
        
        # 简单的 HTML 模板
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        html_lines = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            '  <title>BeautifulReport</title>',
            '  <style>',
            '    body { font-family: Segoe UI; background: linear-gradient(to bottom, #667eea, #764ba2); min-height: 100vh; }',
            '    .container { max-width: 1200px; margin: 20px auto; background: white; border-radius: 8px; padding: 30px; }',
            '    h1 { color: #667eea; }',
            '  </style>',
            '</head>',
            '<body>',
            '  <div class="container">',
            '    <h1>Beautiful Test Report</h1>',
            f'    <p>Generated on: {timestamp}</p>',
            '    <p>Test report generated successfully.</p>',
            '  </div>',
            '</body>',
            '</html>'
        ]
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_lines))
        
        print(f"✓ BeautifulReport 报告已生成: {report_path}")
    except Exception as e:
        print(f"⚠ BeautifulReport 报告生成失败: {e}")


def _add_report_options(args: list) -> None:
    """
    添加报告生成选项（支持四种报告格式）
    
    Args:
        args: pytest 参数列表
    """
    # 1. Pytest HTML
    if _is_module_available('pytest_html'):
        args.append('--html=reports/html/report.html')
        args.append('--self-contained-html')
        print("✓ 启用 Pytest HTML 报告")
    
    # 2. HTMLReport (pytest-html-reporter)
    if _is_module_available('pytest_html_reporter'):
        args.append(f'--html-report={Config.HTMLREPORT_DIR / "report.html"}')
        print("✓ 启用 HTMLReport 报告")
    
    # 3. Allure
    if _is_module_available('allure_pytest'):
        args.append(f'--alluredir={Config.ALLURE_DIR}')
        print("✓ 启用 Allure 报告")


def _post_generate_reports(json_results_file: Optional[str] = None) -> None:
    """
    测试完成后生成其他格式的报告
    """
    # 生成 HTMLTestRunner 格式报告
    _generate_htmltestrunner_report(json_results_file)
    
    # 生成 BeautifulReport 格式报告
    _generate_beautifulreport(json_results_file)

def run_tests(test_path: str, marker: Optional[str] = None) -> int:
    """
    运行测试的通用方法
    
    Args:
        test_path: 测试路径（通常是 'test_cases/'）
        marker: pytest marker（如 'smoke', 'regression'）
    
    Returns:
        测试退出代码
    """
    args = [
        test_path,
        '--ignore-glob=test_cases/examples*',
        '-v',
        '-s',
        f'--junitxml=reports/html/junit.xml'
    ]
    
    # 添加 marker 过滤
    if marker:
        args.extend(['-m', marker])
    
    # 添加报告选项
    _add_report_options(args)
    
    exit_code = pytest.main(args)
    
    # 测试完成后生成其他报告格式
    json_file = Config.REPORTS_DIR / 'test_results.json'
    _post_generate_reports(str(json_file) if json_file.exists() else None)
    
    return exit_code


def run_all_tests() -> int:
    """运行所有测试"""
    print("=" * 80)
    print("运行所有测试用例")
    print("=" * 80)
    return run_tests('test_cases/')


def run_smoke_tests() -> int:
    """运行冒烟测试"""
    print("=" * 80)
    print("运行冒烟测试")
    print("=" * 80)
    return run_tests('test_cases/', marker='smoke')


def run_regression_tests() -> int:
    """运行回归测试"""
    print("=" * 80)
    print("运行回归测试")
    print("=" * 80)
    return run_tests('test_cases/', marker='regression')


def run_specific_test(test_file: str) -> int:
    """
    运行指定测试文件
    
    Args:
        test_file: 测试文件路径
    
    Returns:
        测试退出代码
    """
    print("=" * 80)
    print(f"运行测试文件: {test_file}")
    print("=" * 80)
    
    args = [
        test_file,
        '-v',
        '-s'
    ]
    
    _add_report_options(args)
    return pytest.main(args)


def run_parallel_tests(num_workers: int = 4) -> int:
    """
    并行运行测试
    
    Args:
        num_workers: 并行进程数
    
    Returns:
        测试退出代码
    """
    print("=" * 80)
    print(f"并行运行测试 (进程数: {num_workers})")
    print("=" * 80)
    
    args = [
        'test_cases/',
        '--ignore-glob=test_cases/examples*',
        '-n', str(num_workers),
        '-v',
        f'--junitxml=reports/html/junit.xml'
    ]
    
    _add_report_options(args)
    return pytest.main(args)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python run_tests.py all                    # 运行所有测试")
        print("  python run_tests.py smoke                  # 运行冒烟测试")
        print("  python run_tests.py regression             # 运行回归测试")
        print("  python run_tests.py parallel               # 并行运行测试")
        print("  python run_tests.py file <test_file>       # 运行指定文件")
        return 1
    
    command = sys.argv[1].lower()
    
    if command == 'all':
        return run_all_tests()
    elif command == 'smoke':
        return run_smoke_tests()
    elif command == 'regression':
        return run_regression_tests()
    elif command == 'parallel':
        num_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        return run_parallel_tests(num_workers)
    elif command == 'file':
        if len(sys.argv) < 3:
            print("错误: 请指定测试文件")
            return 1
        return run_specific_test(sys.argv[2])
    else:
        print(f"未知命令: {command}")
        return 1


if __name__ == '__main__':
    start_time = datetime.now()
    print(f"\n测试开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    exit_code = main()
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {duration}")
    print("=" * 80)
    
    sys.exit(exit_code)