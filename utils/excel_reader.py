"""
Excel 数据读取模块
用于读取 Excel 格式的测试数据
"""
import openpyxl
from pathlib import Path
from utils.logger import Logger


class ExcelReader:
    """Excel 读取器类"""
    
    def __init__(self, filepath):
        """
        初始化 Excel 读取器
        
        Args:
            filepath: Excel 文件路径
        """
        self.filepath = Path(filepath)
        self.logger = Logger().get_logger()
        
        if not self.filepath.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        self.workbook = openpyxl.load_workbook(self.filepath)
        self.logger.info(f"已加载 Excel 文件: {filepath}")
    
    def get_sheet_names(self):
        """获取所有工作表名称"""
        return self.workbook.sheetnames
    
    def get_sheet_data(self, sheet_name=None, has_header=True):
        """
        读取工作表数据
        
        Args:
            sheet_name: 工作表名称，默认读取第一个工作表
            has_header: 是否包含表头
        
        Returns:
            列表形式的数据
        """
        if sheet_name:
            sheet = self.workbook[sheet_name]
        else:
            sheet = self.workbook.active
        
        data = []
        rows = list(sheet.iter_rows(values_only=True))
        
        if has_header and len(rows) > 0:
            headers = rows[0]
            for row in rows[1:]:
                row_data = dict(zip(headers, row))
                data.append(row_data)
        else:
            data = [list(row) for row in rows]
        
        self.logger.info(f"从工作表 '{sheet.title}' 读取了 {len(data)} 行数据")
        return data
    
    def get_cell_value(self, sheet_name, row, col):
        """
        获取指定单元格的值
        
        Args:
            sheet_name: 工作表名称
            row: 行号（从1开始）
            col: 列号（从1开始）
        
        Returns:
            单元格值
        """
        sheet = self.workbook[sheet_name]
        return sheet.cell(row=row, column=col).value
    
    def close(self):
        """关闭工作簿"""
        self.workbook.close()
        self.logger.info(f"已关闭 Excel 文件: {self.filepath}")


def read_excel_data(filepath, sheet_name=None):
    """
    便捷函数：读取 Excel 数据
    
    Args:
        filepath: Excel 文件路径
        sheet_name: 工作表名称
    
    Returns:
        数据列表
    """
    reader = ExcelReader(filepath)
    data = reader.get_sheet_data(sheet_name)
    reader.close()
    return data
