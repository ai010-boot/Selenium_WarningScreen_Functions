"""
测试执行脚本
提供便捷的测试运行入口
"""
import sys
import os
import pytest
from datetime import datetime


def run_all_tests():
    """运行所有测试"""
    print("=" * 80)
    print("运行所有测试用例")
    print("=" * 80)
    
    args = [
        'test_cases/',
        '-v',
        '-s',
        '--html=reports/html/report.html',
        '--self-contained-html'
    ]
    
    exit_code = pytest.main(args)
    return exit_code


def run_smoke_tests():
    """运行冒烟测试"""
    print("=" * 80)
    print("运行冒烟测试")
    print("=" * 80)
    
    args = [
        'test_cases/',
        '-m', 'smoke',
        '-v',
        '--html=reports/html/smoke_report.html',
        '--self-contained-html'
    ]
    
    exit_code = pytest.main(args)
    return exit_code


def run_regression_tests():
    """运行回归测试"""
    print("=" * 80)
    print("运行回归测试")
    print("=" * 80)
    
    args = [
        'test_cases/',
        '-m', 'regression',
        '-v',
        '--html=reports/html/regression_report.html',
        '--self-contained-html'
    ]
    
    exit_code = pytest.main(args)
    return exit_code


def run_specific_test(test_file):
    """
    运行指定测试文件
    
    Args:
        test_file: 测试文件路径
    """
    print("=" * 80)
    print(f"运行测试文件: {test_file}")
    print("=" * 80)
    
    args = [
        test_file,
        '-v',
        '-s',
        '--html=reports/html/test_report.html',
        '--self-contained-html'
    ]
    
    exit_code = pytest.main(args)
    return exit_code


def run_parallel_tests(num_workers=4):
    """
    并行运行测试
    
    Args:
        num_workers: 并行进程数
    """
    print("=" * 80)
    print(f"并行运行测试 (进程数: {num_workers})")
    print("=" * 80)
    
    args = [
        'test_cases/',
        f'-n', str(num_workers),
        '-v',
        '--html=reports/html/parallel_report.html',
        '--self-contained-html'
    ]
    
    exit_code = pytest.main(args)
    return exit_code


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
