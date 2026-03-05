from pages.base_page import BasePage
from config.config import Config
from locators.Device_Management import DeviceManagementLocators
from locators.Backstage_management_entry import BackstageManagementEntry
from pages.login_page import LoginPage
from pages.main_page import MainPage
from selenium.webdriver.common.by import By
import time


class DeviceManagementPage(BasePage):
#进入设备管理页面
    DEVICE_MANAGEMENT = DeviceManagementLocators.DEVICE_MANAGEMENT 
# 新增设备
    DEVICE_ADD_BUTTON = DeviceManagementLocators.DEVICE_ADD_BUTTON
    ADD_DEVICE_DIALOG = DeviceManagementLocators.ADD_DEVICE_DIALOG
    DIALOG_TITLE = DeviceManagementLocators.DIALOG_TITLE
    DEVICE_NAME_INPUT = DeviceManagementLocators.DEVICE_NAME_INPUT
    DEVICE_CODE_INPUT = DeviceManagementLocators.DEVICE_CODE_INPUT
    DEVICE_LOCATION_SELECT = DeviceManagementLocators.DEVICE_LOCATION_SELECT
    INSTALLATION_POSITION_INPUT = DeviceManagementLocators.INSTALLATION_POSITION_INPUT
    REMARKS_INPUT = DeviceManagementLocators.REMARKS_INPUT
    # 设备定位地图对话框
    LOCATION_MAP_DIALOG = DeviceManagementLocators.LOCATION_MAP_DIALOG
    LOCATION_SEARCH_INPUT = DeviceManagementLocators.LOCATION_SEARCH_INPUT
    MAP_CONTAINER = DeviceManagementLocators.MAP_CONTAINER
    MAP_CONFIRM_BUTTON = DeviceManagementLocators.MAP_CONFIRM_BUTTON
    MAP_CLOSE_BUTTON = DeviceManagementLocators.MAP_CLOSE_BUTTON
    # 对话框按钮
    CANCEL_BUTTON = DeviceManagementLocators.CANCEL_BUTTON
    CONFIRM_BUTTON = DeviceManagementLocators.CONFIRM_BUTTON
    # 设备列表
    DEVICE_LIST_TABLE = DeviceManagementLocators.DEVICE_LIST_TABLE
    DEVICE_LIST_ROWS = DeviceManagementLocators.DEVICE_LIST_ROWS
    # 操作按钮
    EDIT_DEVICE_BUTTON = DeviceManagementLocators.EDIT_DEVICE_BUTTON
    DELETE_DEVICE_BUTTON = DeviceManagementLocators.DELETE_DEVICE_BUTTON
    VIEW_DEVICE_BUTTON = DeviceManagementLocators.VIEW_DEVICE_BUTTON
    MORE_BUTTON = DeviceManagementLocators.MORE_BUTTON
    # 编辑设备对话框
    EDIT_DEVICE_DIALOG = DeviceManagementLocators.EDIT_DEVICE_DIALOG
    EDIT_DIALOG_TITLE = DeviceManagementLocators.EDIT_DIALOG_TITLE
    EDIT_DEVICE_NAME_INPUT = DeviceManagementLocators.EDIT_DEVICE_NAME_INPUT
    EDIT_DEVICE_GROUP_SELECT = DeviceManagementLocators.EDIT_DEVICE_GROUP_SELECT
    DEVICE_GROUP_DROPDOWN = DeviceManagementLocators.DEVICE_GROUP_DROPDOWN
    DEVICE_GROUP_OPTIONS = DeviceManagementLocators.DEVICE_GROUP_OPTIONS
    CAMERA_SCENE_SELECT = DeviceManagementLocators.CAMERA_SCENE_SELECT
    CAMERA_SCENE_DROPDOWN = DeviceManagementLocators.CAMERA_SCENE_DROPDOWN
    CAMERA_SCENE_OPTIONS = DeviceManagementLocators.CAMERA_SCENE_OPTIONS
    EDIT_DEVICE_LOCATION_INPUT = DeviceManagementLocators.EDIT_DEVICE_LOCATION_INPUT
    EDIT_INSTALLATION_POSITION_INPUT = DeviceManagementLocators.EDIT_INSTALLATION_POSITION_INPUT
    EDIT_REMARKS_INPUT = DeviceManagementLocators.EDIT_REMARKS_INPUT
    # 不可编辑字段
    EDIT_DEPARTMENT_INPUT = DeviceManagementLocators.EDIT_DEPARTMENT_INPUT
    EDIT_PRODUCT_INPUT = DeviceManagementLocators.EDIT_PRODUCT_INPUT
    EDIT_DEVICE_CODE_INPUT = DeviceManagementLocators.EDIT_DEVICE_CODE_INPUT
    # 成功消息
    SUCCESS_MESSAGE = DeviceManagementLocators.SUCCESS_MESSAGE
    # 错误消息
    ERROR_MESSAGE = DeviceManagementLocators.ERROR_MESSAGE
    # 编辑设备对话框按钮
    EDIT_DEVICE_BUTTON = DeviceManagementLocators.EDIT_DEVICE_BUTTON
    # 编辑设备列表
    EDIT_DEVICE_DIALOG = DeviceManagementLocators.EDIT_DEVICE_DIALOG
    DIALOG_TITLE = DeviceManagementLocators.EDIT_DIALOG_TITLE
    # 更多下拉菜单
    MORE_DROPDOWN = DeviceManagementLocators.MORE_DROPDOWN
    DELETE_DEVICE_MENU_ITEM = DeviceManagementLocators.DELETE_DEVICE_MENU_ITEM
    ASSOCIATE_DEVICE_MENU_ITEM = DeviceManagementLocators.ASSOCIATE_DEVICE_MENU_ITEM
    SHIELD_SETTINGS_MENU_ITEM = DeviceManagementLocators.SHIELD_SETTINGS_MENU_ITEM
    DEVICE_LINKAGE_MENU_ITEM = DeviceManagementLocators.DEVICE_LINKAGE_MENU_ITEM
    # 删除确认对话框
    DELETE_CONFIRM_DIALOG = DeviceManagementLocators.DELETE_CONFIRM_DIALOG
    DELETE_CONFIRM_BUTTON = DeviceManagementLocators.DELETE_CONFIRM_BUTTON
    DELETE_CANCEL_BUTTON = DeviceManagementLocators.DELETE_CANCEL_BUTTON

    def __init__(self, driver):
        super().__init__(driver)
        """初始化设备管理页面"""
        self.url=Config.BASE_URL
    def complete_login_and_navigation(self, username='jkcsdw', password='123456'):
        """完成登录并进入到设备管理页面"""
        try:
            # 1.执行登录
            login_page=LoginPage(self.driver)
            login_page.navigate_to_login()
            login_page.login(username, password)
            time.sleep(3)
            
            # 2.进入后台管理页面
            main_page=MainPage(self.driver)
            main_page.enter_backend_management()
            time.sleep(3)
            
            self.logger.info("完成登录并成功进入后台管理页面")
            return True
        except Exception as e:
            self.logger.error(f"登录和导航失败: {e}")
            return False
    
    def enter_device_management(self):
        """进入设备管理页面"""
        try:
            # 点击设备管理按钮
            self.click(self.DEVICE_MANAGEMENT)
            self.logger.info("成功进入设备管理页面")
            return True
        except Exception as e:
            self.logger.error(f"进入设备管理页面失败: {e}")
            return False
    
    def add_device(self, device_name, device_code, installation_position, remarks=""):
        """新增设备
        
        Args:
            device_name: 设备名称
            device_code: 设备编号
            installation_position: 安装位置
            remarks: 备注
            
        Returns:
            bool: 是否成功添加
        """
        try:
            # 1. 点击新增设备按钮
            self.click(self.DEVICE_ADD_BUTTON)
            time.sleep(2)  # 等待对话框打开
            
            # 2. 填写设备信息
            self.input_text(self.DEVICE_NAME_INPUT, device_name)
            self.input_text(self.DEVICE_CODE_INPUT, device_code)
            self.input_text(self.INSTALLATION_POSITION_INPUT, installation_position)
            if remarks:
                self.input_text(self.REMARKS_INPUT, remarks)
            
            # 3. 点击确定按钮
            self.click(self.CONFIRM_BUTTON)
            time.sleep(3)  # 等待操作完成
            
            # 4. 验证成功消息
            return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
        except Exception as e:
            self.logger.error(f"新增设备失败: {e}")
            return False
    
    def edit_device(self, device_name, new_device_name=None, device_group=None, camera_scene=None, 
                    device_location=None, installation_position=None, remarks=None):
        """编辑设备
        
        Args:
            device_name: 要编辑的设备名称
            new_device_name: 新的设备名称
            device_group: 设备分组
            camera_scene: 摄像头场景
            device_location: 设备定位
            installation_position: 安装位置
            remarks: 备注
            
        Returns:
            bool: 是否成功编辑
        """
        try:
            # 1. 找到设备并点击编辑按钮
            edit_button = self.find_element(self.EDIT_DEVICE_BUTTON)
            edit_button.click()
            time.sleep(2)  # 等待对话框打开
            
            # 2. 修改设备名称
            if new_device_name:
                self.clear_and_input_text(self.EDIT_DEVICE_NAME_INPUT, new_device_name)
            
            # 3. 修改设备分组
            if device_group:
                self.click(self.EDIT_DEVICE_GROUP_SELECT)
                time.sleep(1)
                # 选择指定的分组
                group_option = self.find_element(self.DEVICE_GROUP_OPTIONS)
                group_option.click()
                time.sleep(1)
            
            # 4. 修改摄像头场景
            if camera_scene:
                self.click(self.CAMERA_SCENE_SELECT)
                time.sleep(1)
                # 选择指定的场景
                scene_option = self.find_element(self.CAMERA_SCENE_OPTIONS)
                scene_option.click()
                time.sleep(1)
            
            # 5. 修改设备定位（点击打开地图选择）
            if device_location:
                self.click(self.EDIT_DEVICE_LOCATION_INPUT)
                time.sleep(2)  # 等待地图对话框打开
                # 这里可以添加地图选择逻辑
                # 暂时直接点击确定
                self.click(self.MAP_CONFIRM_BUTTON)
                time.sleep(1)
            
            # 6. 修改安装位置
            if installation_position:
                self.clear_and_input_text(self.EDIT_INSTALLATION_POSITION_INPUT, installation_position)
            
            # 7. 修改备注
            if remarks:
                self.clear_and_input_text(self.EDIT_REMARKS_INPUT, remarks)
            
            # 8. 点击确定按钮
            self.click(self.CONFIRM_BUTTON)
            time.sleep(3)  # 等待操作完成
            
            # 9. 验证成功消息
            return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
        except Exception as e:
            self.logger.error(f"编辑设备失败: {e}")
            return False
    
    def delete_device(self, device_name):
        """删除设备
        
        Args:
            device_name: 要删除的设备名称
            
        Returns:
            bool: 是否成功删除
        """
        try:
            # 1. 根据设备名称定位到对应行的“更多”按钮并点击
            device_row_xpath = f"//tr[contains(., '{device_name}')]"
            more_button_xpath = f"{device_row_xpath}//button[contains(@class, 'more') or contains(., '更多')]"
            more_button = self.find_element((By.XPATH, more_button_xpath))
            more_button.click()
            time.sleep(1)  # 等待下拉菜单显示
            
            # 2. 点击删除设备选项
            self.click(self.DELETE_DEVICE_MENU_ITEM)
            time.sleep(1)  # 等待确认对话框
            
            # 3. 点击确认删除按钮
            self.click(self.DELETE_CONFIRM_BUTTON)
            time.sleep(3)  # 等待操作完成
            
            # 4. 验证成功消息
            return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
        except Exception as e:
            self.logger.error(f"删除设备失败: {e}")
            return False
    
    def clear_and_input_text(self, locator, text):
        """清空输入框并输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

