from pages.base_page import BasePage
from locators.Backstage_management_entry import BackstageManagementEntry
import time


class MainPage(BasePage):
    """主页面/后台管理相关操作封装"""

    def __init__(self, driver):
        super().__init__(driver)

    def enter_backend_management(self):
        """尝试进入后台管理，返回 True"""
        elem = self.find_element(BackstageManagementEntry.BACKEND_MANAGEMENT, timeout=5)
        elem.click()
        time.sleep(1)
        return True


