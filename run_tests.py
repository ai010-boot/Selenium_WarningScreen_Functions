"""
测试执行脚本
提供便捷的测试运行入口
支持的报告格式：Pytest HTML、HTMLReport、Allure
"""
import sys
import os
import pytest
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


def _add_report_options(args: list) -> None:
    """
    添加报告生成选项（三种报告格式）
    
    Args:
        args: pytest 参数列表
    """
    # 1. Pytest HTML - 详细的HTML测试报告
    if _is_module_available('pytest_html'):
        args.append('--html=reports/html/report.html')
        args.append('--self-contained-html')
        print("✓ 启用 Pytest HTML 报告")
    else:
        print("⚠ pytest-html 未安装，跳过HTML报告")
    
    # 2. HTMLReport (pytest-html-reporter) - 现代化测试报告
    if _is_module_available('pytest_html_reporter'):
        args.append(f'--html-report={Config.HTMLREPORT_DIR / "report.html"}')
        print("✓ 启用 HTMLReport 报告")
    else:
        print("⚠ pytest-html-reporter 未安装，跳过HTMLReport报告")
    
    # 3. Allure - 专业级交互式报告
    if _is_module_available('allure_pytest'):
        args.append(f'--alluredir={Config.ALLURE_DIR}')
        print("✓ 启用 Allure 报告")
    else:
        print("⚠ allure-pytest 未安装，跳过Allure报告")


def _generate_allure_html() -> None:
    """
    测试完成后自动生成 Allure HTML 报告
    """
    import subprocess
    
    # 定义 Allure HTML 输出目录
    allure_html_dir = Config.REPORTS_DIR / 'allure-html'
    
    try:
        print("\n🔄 正在生成 Allure HTML 报告...")
        
        # 执行 allure generate 命令
        result = subprocess.run(
            ['allure', 'generate', str(Config.ALLURE_DIR), '-o', str(allure_html_dir), '--clean'],
            capture_output=True,
            text=True,
            timeout=30,
            shell=True  # 在 Windows 上使用 shell 模式
        )
        
        if result.returncode == 0:
            print(f"✓ Allure HTML 报告已生成: {allure_html_dir / 'index.html'}")
            print(f"  提示：直接用浏览器打开 {allure_html_dir / 'index.html'} 即可查看")
        else:
            print(f"⚠ Allure HTML 生成失败")
            if result.stderr:
                print(f"  错误信息: {result.stderr}")
            if result.stdout:
                print(f"  输出信息: {result.stdout}")
            
    except FileNotFoundError:
        print("\n⚠ Allure 命令行工具未找到")
        print("  提示：请确认 Allure 已安装并添加到系统 PATH")
        print("  安装指南: https://docs.qameta.io/allure/#_installing_a_commandline")
    except subprocess.TimeoutExpired:
        print("⚠ Allure HTML 生成超时")
    except Exception as e:
        print(f"⚠ Allure HTML 生成出错: {e}")

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
    
    # 运行测试
    exit_code = pytest.main(args)
    
    # 测试完成后，自动生成 Allure HTML 报告
    if _is_module_available('allure_pytest'):
        _generate_allure_html()
    
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