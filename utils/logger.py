"""
日志工具模块
提供统一的日志记录功能
"""
import logging
import sys
from pathlib import Path
from config.config import Config


class Logger:
    """日志记录器类"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化日志记录器"""
        if self._initialized:
            return
        
        self._initialized = True
        self.logger = logging.getLogger('AutomationTest')
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            
            # 文件处理器
            log_file = Config.LOGS_DIR / 'automation.log'
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(Config.LOG_FORMAT)
            file_handler.setFormatter(file_formatter)
            
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def get_logger(self):
        """获取日志记录器实例"""
        return self.logger
    
    def debug(self, message):
        """调试级别日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息级别日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """错误级别日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """严重错误级别日志"""
        self.logger.critical(message)


# 创建全局日志实例
logger = Logger()
