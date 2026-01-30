"""
通用测试数据配置文件 - 自动查找模式（无需配置）

约定优于配置原则：
    1. 数据文件命名：{module_name}_test_data.{csv|json|xlsx}
    2. 文件位置：test_data/test_type/ 目录
    3. 自动查找优先级：csv > json > xlsx

快速使用：
    # 1. 自动查找（推荐）
    data = get_test_data('login')  # 自动找 login_test_data.csv/json/xlsx
    
    # 2. 指定格式
    data = get_test_data('login', 'csv')   # 使用 CSV
    data = get_test_data('login', 'json')  # 使用 JSON
    data = get_test_data('login', 'xlsx')  # 使用 Excel
    
    # 3. 在测试用例中使用
    @pytest.mark.parametrize("test_case", get_test_data('login'))
    def test_login(self, driver, test_case):
        username = test_case['username']
        password = test_case['password']

添加新模块（无需修改代码）：
    步骤1: 创建数据文件
        test_data/test_type/home_test_data.csv  # 任选 CSV/JSON/XLSX
    
    步骤2: 直接使用
        data = get_test_data('home')  # 自动找到并加载
    
    就这么简单！无需任何配置！
"""
import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Any


class TestDataConfig:
    """
    测试数据配置类 - 自动查找模式（无需配置）
    
    约定优于配置：
        - 数据文件命名：{module_name}_test_data.{csv|json|xlsx}
        - 文件位置：test_data/test_type/ 目录
        - 自动查找优先级：csv > json > xlsx
    
    使用示例：
        # 自动查找
        data = get_test_data('login')  # 自动找 login_test_data.csv/json/xlsx
        
        # 指定格式
        data = get_test_data('login', 'csv')
        
        # 添加新模块：只需创建文件，无需修改代码
        # 1. 创建 test_data/test_type/home_test_data.csv
        # 2. 直接使用 get_test_data('home')
    """
    
    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent
    
    @classmethod
    def load_test_data(cls, module_name: str, data_format: str = 'auto') -> List[Dict[str, Any]]:
        """
        加载指定模块的测试数据（自动查找，无需配置）
        
        约定：
            - 数据文件命名规范：{module_name}_test_data.{格式}
            - 数据文件位置：test_data/test_type/ 目录下
            - 支持格式：csv, json, xlsx
        
        Args:
            module_name: 模块名称（如 'login', 'home', 'search'）
            data_format: 数据格式 ('csv', 'json', 'xlsx', 'auto')
                        'auto' 时按 csv > json > xlsx 优先级自动查找
            
        Returns:
            测试数据列表
            
        示例：
            # 自动查找 login_test_data.csv/json/xlsx
            get_test_data('login')
            
            # 指定使用 CSV 格式
            get_test_data('login', 'csv')
            
            # 添加新模块无需配置，只需创建文件：
            # test_data/test_type/home_test_data.csv
            get_test_data('home')
        """
        # 基础路径：test_data/test_type/
        base_path = cls.PROJECT_ROOT / 'test_data' / 'test_type'
        
        # 确定要使用的数据格式
        if data_format == 'auto':
            # 按优先级自动查找文件：csv > json > xlsx
            for fmt in ['csv', 'json', 'xlsx']:
                file_path = base_path / f'{module_name}_test_data.{fmt}'
                if file_path.exists():
                    data_format = fmt
                    data_file = file_path
                    break
                else:
                    # 递归查找（兼容示例子目录等）
                    matches = list(base_path.rglob(f'{module_name}_test_data.{fmt}'))
                    if matches:
                        data_format = fmt
                        data_file = matches[0]
                        break
            else:
                # 未找到任何格式的文件
                raise FileNotFoundError(
                    f"未找到模块 '{module_name}' 的测试数据文件\n"
                    f"请在以下位置创建数据文件：\n"
                    f"  - {base_path / f'{module_name}_test_data.csv'}\n"
                    f"  - {base_path / f'{module_name}_test_data.json'}\n"
                    f"  - {base_path / f'{module_name}_test_data.xlsx'}"
                )
        else:
            # 使用指定格式
            data_file = base_path / f'{module_name}_test_data.{data_format}'
            if not data_file.exists():
                # 递归查找（兼容示例子目录等）
                matches = list(base_path.rglob(f'{module_name}_test_data.{data_format}'))
                if matches:
                    data_file = matches[0]
                else:
                    raise FileNotFoundError(
                        f"找不到测试数据文件: {data_file}\n"
                        f"请创建文件或使用 data_format='auto' 自动查找"
                    )
        
        # 根据文件格式加载数据
        if data_format == 'csv':
            return cls._load_csv_data(data_file)
        elif data_format == 'json':
            return cls._load_json_data(data_file)
        elif data_format == 'xlsx':
            return cls._load_excel_data(data_file)
        else:
            raise ValueError(f"不支持的数据格式: {data_format}，支持：csv, json, xlsx")
    
    @classmethod
    def _load_csv_data(cls, file_path: Path) -> List[Dict[str, Any]]:
        """加载CSV格式的测试数据（支持 # 开头的注释行）"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            # 过滤掉以 # 开头的注释行和空行
            lines = [line for line in file if line.strip() and not line.strip().startswith('#')]
            reader = csv.DictReader(lines)
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
