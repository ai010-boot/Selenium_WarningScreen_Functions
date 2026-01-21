"""
截图工具模块
提供测试失败时的截图功能
"""
import os
from datetime import datetime
from config.config import Config
from utils.logger import Logger


class Screenshot:
    """截图工具类"""
    
    logger = Logger().get_logger()
    
    @staticmethod
    def take_screenshot(driver, test_name):
        """
        截取当前页面截图
        
        Args:
            driver: WebDriver 实例
            test_name: 测试用例名称
        
        Returns:
            截图文件路径
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{test_name}_{timestamp}.png"
        filepath = Config.SCREENSHOTS_DIR / filename
        
        try:
            driver.save_screenshot(str(filepath))
            Screenshot.logger.info(f"截图已保存: {filepath}")
            return str(filepath)
        except Exception as e:
            Screenshot.logger.error(f"截图失败: {e}")
            return None
    
    @staticmethod
    def take_element_screenshot(element, test_name):
        """
        截取指定元素的截图
        
        Args:
            element: WebElement 实例
            test_name: 测试用例名称
        
        Returns:
            截图文件路径
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{test_name}_element_{timestamp}.png"
        filepath = Config.SCREENSHOTS_DIR / filename
        
        try:
            element.screenshot(str(filepath))
            Screenshot.logger.info(f"元素截图已保存: {filepath}")
            return str(filepath)
        except Exception as e:
            Screenshot.logger.error(f"元素截图失败: {e}")
            return None
