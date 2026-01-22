"""
通用测试数据配置文件
统一管理所有测试数据，便于在不同模块中引用
"""
import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Any


class TestDataConfig:
    """
    测试数据配置类
    统一管理所有测试数据，提供便捷的访问接口
    """
    
    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent
    
    # 测试数据文件路径配置
    TEST_DATA_PATHS = {
        'login': {
            'csv': PROJECT_ROOT / 'test_data' / 'test_type' / 'login_test_data.csv',
            'json': PROJECT_ROOT / 'test_data' / 'test_type' /  'login_test_data.json',
            'xlsx': PROJECT_ROOT / 'test_data' / 'test_type' /  'login_test_data.xlsx'
        },
        # 可以在这里添加更多模块的测试数据路径
        # 'home': {
        #     'csv': PROJECT_ROOT / 'test_data' / 'home_test_data.csv',
        #     'json': PROJECT_ROOT / 'test_data' / 'home_test_data.json',
        #     'xlsx': PROJECT_ROOT / 'test_data' / 'home_test_data.xlsx'
        # },
    }
    
    @classmethod
    def load_test_data(cls, module_name: str, data_format: str = 'auto') -> List[Dict[str, Any]]:
        """
        加载指定模块的测试数据
        
        Args:
            module_name: 模块名称（如 'login', 'home' 等）
            data_format: 数据格式 ('csv', 'json', 'xlsx', 'auto')
            
        Returns:
            测试数据列表
        """
        if module_name not in cls.TEST_DATA_PATHS:
            raise ValueError(f"未找到模块 {module_name} 的测试数据配置")
        
        # 确定要使用的数据格式
        if data_format == 'auto':
            # 按优先级查找可用的数据文件
            for fmt in ['csv', 'json', 'xlsx']:
                if fmt in cls.TEST_DATA_PATHS[module_name]:
                    data_file = cls.TEST_DATA_PATHS[module_name][fmt]
                    if os.path.exists(data_file):
                        data_format = fmt
                        break
        else:
            data_file = cls.TEST_DATA_PATHS[module_name][data_format]
        
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"找不到测试数据文件: {data_file}")
        
        # 根据文件格式加载数据
        if data_format == 'csv':
            return cls._load_csv_data(data_file)
        elif data_format == 'json':
            return cls._load_json_data(data_file)
        elif data_format == 'xlsx':
            return cls._load_excel_data(data_file)
        else:
            raise ValueError(f"不支持的数据格式: {data_format}")
    
    @classmethod
    def _load_csv_data(cls, file_path: Path) -> List[Dict[str, Any]]:
        """加载CSV格式的测试数据"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 处理空值：将空字符串转换为None（可选）或保持原样
                # 过滤掉所有字段都为空的行
                row_dict = dict(row)
                if any(value.strip() if isinstance(value, str) else value for value in row_dict.values()):
                    data.append(row_dict)
        return data
    
    @classmethod
    def _load_json_data(cls, file_path: Path) -> List[Dict[str, Any]]:
        """加载JSON格式的测试数据"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
            # 尝试多种可能的键名
            # 1. {module}_test_data (如: login_test_data)
            key_name = f"{file_path.stem.replace('_test_data', '')}_test_data"
            if key_name in content:
                return content[key_name]
            # 2. 直接使用文件名作为键（如果文件名就是 login_test_data.json）
            if file_path.stem in content:
                return content[file_path.stem]
            # 3. 如果内容直接是数组，直接返回
            if isinstance(content, list):
                return content
            # 4. 如果以上都不匹配，返回空列表
            return []
    
    @classmethod
    def _load_excel_data(cls, file_path: Path) -> List[Dict[str, Any]]:
        """加载Excel格式的测试数据"""
        try:
            from utils.excel_reader import ExcelReader
            reader = ExcelReader(str(file_path))
            # 假设Excel的第一个工作表包含测试数据
            sheet_name = reader.sheet_names[0] if reader.sheet_names else None
            if not sheet_name:
                reader.close()
                return []
            data = reader.get_sheet_data(sheet_name)
            reader.close()
            # 过滤掉所有字段都为空的行
            filtered_data = []
            for row in data:
                if any(value for value in row.values() if value is not None and str(value).strip()):
                    filtered_data.append(row)
            return filtered_data
        except ImportError:
            # 如果无法导入ExcelReader，抛出异常
            raise ImportError("Could not import ExcelReader, please check if openpyxl is installed")
        except Exception as e:
            raise Exception(f"加载Excel文件失败: {e}")
    
    @classmethod
    def _get_default_data(cls, module_name: str) -> List[Dict[str, Any]]:
        """获取指定模块的默认测试数据"""
        # 移除默认数据，返回空列表
        return []


# 便捷函数，方便在测试中直接使用
def get_test_data(module_name: str, data_format: str = 'auto') -> List[Dict[str, Any]]:
    """
    便捷函数：获取指定模块的测试数据
    
    Args:
        module_name: 模块名称
        data_format: 数据格式 ('csv', 'json', 'xlsx', 'auto')
        
    Returns:
        测试数据列表
    """
    return TestDataConfig.load_test_data(module_name, data_format)


# 预加载常用测试数据（可选）
# 注意：如果数据文件不存在，这行代码会导致模块加载失败
# 建议在测试中按需加载，而不是在模块级别预加载
# LOGIN_TEST_DATA = get_test_data('login')  # 已注释，按需使用