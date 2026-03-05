from pages.base_page import BasePage
from config.config import Config
from locators.User_Management import UserManagementLocators
from locators.Backstage_management_entry import BackstageManagementEntry
from pages.login_page import LoginPage
from pages.main_page import MainPage
from selenium.webdriver.common.by import By
import time


class UserManagementPage(BasePage):
# 新增用户
    USER_ADD_BUTTON = UserManagementLocators.USER_ADD_BUTTON
    DEPARTMENT_SELECT = UserManagementLocators.DEPARTMENT_SELECT
    DEPARTMENT_DROPDOWN_TOGGLE = UserManagementLocators.DEPARTMENT_DROPDOWN_TOGGLE
    DEPARTMENT_FIRST_OPTION = UserManagementLocators.DEPARTMENT_FIRST_OPTION
    NICKNAME_INPUT = UserManagementLocators.NICKNAME_INPUT
    ACCOUNT_INPUT = UserManagementLocators.ACCOUNT_INPUT
    ADD_PASSWORD_INPUT = UserManagementLocators.ADD_PASSWORD_INPUT
    ADD_CONFIRM_PASSWORD_INPUT = UserManagementLocators.ADD_CONFIRM_PASSWORD_INPUT
    PHONE_INPUT = UserManagementLocators.PHONE_INPUT
    GENDER_MALE = UserManagementLocators.GENDER_MALE
    GENDER_FEMALE = UserManagementLocators.GENDER_FEMALE
    ROLE_SELECT = UserManagementLocators.ROLE_SELECT
    AVATAR_UPLOAD_INPUT = UserManagementLocators.AVATAR_UPLOAD_INPUT
    AVATAR_UPLOAD_AREA = UserManagementLocators.AVATAR_UPLOAD_AREA
    CONFIRM_BUTTON = UserManagementLocators.CONFIRM_BUTTON
    CANCEL_BUTTON = UserManagementLocators.CANCEL_BUTTON    
    # 编辑用户
    EDIT_USER = UserManagementLocators.Edit_USER
    EDIT_NICKNAME_INPUT = UserManagementLocators.Edit_NICKNAME_INPUT    
    # 删除用户
    DELETE_USER = UserManagementLocators.Delete_USER
    
# 部门管理
    # 新增部门
    ADD_DEPARTMENT = UserManagementLocators.Add_DEPARTMENT
    ADD_DEPARTMENT_NAME_INPUT = UserManagementLocators.Add_Department_NAME_INPUT
    ADD_REMARKS_INPUT = UserManagementLocators.Add_Remarks_INPUT
    ADD_DEPARTMENT_CONFIRM_BUTTON = UserManagementLocators.Add_Department_CONFIRM_BUTTON
    ADD_DEPARTMENT_CANCEL_BUTTON = UserManagementLocators.Add_Department_CANCEL_BUTTON
    ADD_DEPARTMENT_SUCCESS_MESSAGE = UserManagementLocators.Add_Department_SUCCESS_MESSAGE
    
    # 新增子部门
    ADD_SUB_DEPARTMENT = UserManagementLocators.Add_Sub_DEPARTMENT
    ADD_SUB_DEPARTMENT_NAME_INPUT = UserManagementLocators.Add_Sub_Department_NAME_INPUT
    ADD_SUB_REMARKS_INPUT = UserManagementLocators.Add_Sub_Remarks_INPUT
    ADD_SUB_DEPARTMENT_CONFIRM_BUTTON = UserManagementLocators.Add_Sub_Department_CONFIRM_BUTTON
    ADD_SUB_DEPARTMENT_CANCEL_BUTTON = UserManagementLocators.Add_Sub_Department_CANCEL_BUTTON
    ADD_SUB_DEPARTMENT_SUCCESS_MESSAGE = UserManagementLocators.Add_Sub_Department_SUCCESS_MESSAGE
    
    # 编辑部门
    EDIT_DEPARTMENT = UserManagementLocators.Edit_DEPARTMENT
    EDIT_DEPARTMENT_NAME_INPUT = UserManagementLocators.Edit_Department_NAME_INPUT
    EDIT_REMARKS_INPUT = UserManagementLocators.Edit_Remarks_INPUT
    EDIT_DEPARTMENT_CONFIRM_BUTTON = UserManagementLocators.Edit_Department_CONFIRM_BUTTON
    EDIT_DEPARTMENT_CANCEL_BUTTON = UserManagementLocators.Edit_Department_CANCEL_BUTTON
    EDIT_DEPARTMENT_SUCCESS_MESSAGE = UserManagementLocators.Edit_Department_SUCCESS_MESSAGE
    
    # 删除部门
    DELETE_DEPARTMENT = UserManagementLocators.Delete_DEPARTMENT

    def __init__(self, driver):
        """
        初始化用户管理页面
        """
        super().__init__(driver)
        self.url = Config.BASE_URL
    
    def complete_login_and_navigation(self, username='jkcsdw', password='123456'):
        """
        完成登录并进入用户管理页面的完整流程
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            bool: 是否成功进入用户管理页面
        """
        # 1. 执行登录
        login_page = LoginPage(self.driver)       
        login_page.navigate_to_login()
        login_page.login(username, password)
        
        # 等待登录成功
        timeout = 20
        start = time.time()
        while time.time() - start < timeout:
            if login_page.is_login_successful():
                break
            time.sleep(0.5)
        
        # 2. 进入后台管理
        main_page = MainPage(self.driver)
        main_page.enter_backend_management()
        
        # 3. 验证是否进入用户管理页面
        time.sleep(2)  # 等待页面加载
        return self.is_element_visible(self.USER_ADD_BUTTON, timeout=10)
    
    def add_new_user(self, account, nickname, password, confirm_password, phone, gender='男', avatar_path=None):
        """
        添加新用户
        """
        # 点击新建用户按钮
        self.click(self.USER_ADD_BUTTON)
        time.sleep(1)  # 等待对话框打开
        # 部门的选择
        self.click(self.DEPARTMENT_SELECT)
        self.click(self.DEPARTMENT_DROPDOWN_TOGGLE)
        self.click(self.DEPARTMENT_FIRST_OPTION)
        # 填写表单
        self.input_text(self.NICKNAME_INPUT, nickname)
        self.input_text(self.ACCOUNT_INPUT, account)
        self.input_text(self.PHONE_INPUT, phone)        
        # 选择性别
        if gender == '女':
            self.click(self.GENDER_FEMALE)
        else:
            self.click(self.GENDER_MALE)
        self.click(self.ROLE_SELECT)
        # 上传头像（如果提供）
        if avatar_path:
            try:
                avatar_input = self.find_element(self.AVATAR_UPLOAD_INPUT, timeout=2)
                avatar_input.send_keys(avatar_path)
                time.sleep(2)  # 等待上传完成
            except Exception as e:
                self.logger.warning(f"头像上传失败: {e}")
        # 填写密码
        self.input_text(self.ADD_PASSWORD_INPUT, password)
        self.input_text(self.ADD_CONFIRM_PASSWORD_INPUT, confirm_password)
        # 点击确认按钮
        self.click(self.CONFIRM_BUTTON)
        time.sleep(2)  # 等待操作完成       
        # 验证是否成功
        return True
    
    def cancel_add_user(self):
        """
        取消添加用户
        
        Returns:
            bool: 是否成功取消
        """
        if self.is_element_visible(self.CANCEL_BUTTON):
            self.click(self.CANCEL_BUTTON)
            time.sleep(1)
            return not self.is_element_visible(self.NICKNAME_INPUT, timeout=2)
        return False
    
    def edit_user(self, username, new_nickname=None, new_phone=None):
        """
        编辑用户
        
        Args:
            username: 要编辑的用户名
            new_nickname: 新昵称
            new_phone: 新手机号
        
        Returns:
            bool: 是否成功编辑
        """
        try:
            # 找到包含指定用户名的行
            user_rows = self.find_elements((By.XPATH, "//table//tr"))
            for row in user_rows:
                if username in row.text:
                    # 点击编辑按钮
                    edit_button = row.find_element(*self.EDIT_USER)
                    edit_button.click()
                    time.sleep(1)  # 等待对话框打开
                    
                    # 填写新信息
                    if new_nickname:
                        self.input_text(self.EDIT_NICKNAME_INPUT, new_nickname)
                    if new_phone:
                        self.input_text(self.PHONE_INPUT, new_phone)
                    
                    # 点击确认按钮
                    self.click(self.CONFIRM_BUTTON)
                    time.sleep(2)  # 等待操作完成
                    return True
            return False
        except Exception as e:
            self.logger.error(f"编辑用户失败: {e}")
            return False
    
    def delete_user(self, username):
        """
        删除用户
        
        Args:
            username: 要删除的用户名
        
        Returns:
            bool: 是否成功删除
        """
        try:
            # 找到包含指定用户名的行
            user_rows = self.find_elements((By.XPATH, "//table//tr"))
            for row in user_rows:
                if username in row.text:
                    # 点击删除按钮
                    delete_button = row.find_element(*self.DELETE_USER)
                    delete_button.click()
                    time.sleep(1)  # 等待确认对话框
                    
                    # 点击确认删除
                    confirm_delete = self.find_element((By.XPATH, "//button[contains(., '确认')]"))
                    confirm_delete.click()
                    time.sleep(2)  # 等待操作完成
                    return True
            return False
        except Exception as e:
            self.logger.error(f"删除用户失败: {e}")
            return False
    
    def add_department(self, department_name, remarks=""):
        """
        新增部门
        
        Args:
            department_name: 部门名称
            remarks: 备注
        
        Returns:
            bool: 是否成功添加
        """
        try:
            # 点击新增部门按钮
            self.click(self.ADD_DEPARTMENT)
            time.sleep(1)  # 等待对话框打开
            
            # 填写部门信息
            self.input_text(self.ADD_DEPARTMENT_NAME_INPUT, department_name)
            if remarks:
                self.input_text(self.ADD_REMARKS_INPUT, remarks)
            
            # 点击确认按钮
            self.click(self.ADD_DEPARTMENT_CONFIRM_BUTTON)
            time.sleep(2)  # 等待操作完成
            
            # 验证成功消息
            return self.is_element_visible(self.ADD_DEPARTMENT_SUCCESS_MESSAGE, timeout=5)
        except Exception as e:
            self.logger.error(f"新增部门失败: {e}")
            return False
    
    def add_sub_department(self, department_name, remarks=""):
        """
        新增子部门
        
        Args:
            department_name: 子部门名称
            remarks: 备注
        
        Returns:
            bool: 是否成功添加
        """
        try:
            # 1. 找到需要悬停的元素（通常是父部门）
            parent_department = self.find_element((By.XPATH, "//span[contains(text(), '部门管理')]"))
            
            # 2. 悬停显示新增子部门按钮
            self.hover_over_element(parent_department)
            time.sleep(1)  # 等待按钮显示
            
            # 3. 点击新增子部门按钮
            self.click(self.ADD_SUB_DEPARTMENT)
            time.sleep(1)  # 等待对话框打开
            
            # 4. 填写子部门信息
            self.input_text(self.ADD_SUB_DEPARTMENT_NAME_INPUT, department_name)
            if remarks:
                self.input_text(self.ADD_SUB_REMARKS_INPUT, remarks)
            
            # 5. 点击确认按钮
            self.click(self.ADD_SUB_DEPARTMENT_CONFIRM_BUTTON)
            time.sleep(2)  # 等待操作完成
            
            # 6. 验证成功消息
            return self.is_element_visible(self.ADD_SUB_DEPARTMENT_SUCCESS_MESSAGE, timeout=5)
        except Exception as e:
            self.logger.error(f"新增子部门失败: {e}")
            return False
    
    def edit_department(self, department_name, new_name=None, new_remarks=""):
        """
        编辑部门
        
        Args:
            department_name: 要编辑的部门名称
            new_name: 新部门名称
            new_remarks: 新备注
        
        Returns:
            bool: 是否成功编辑
        """
        try:
            # 找到包含指定部门名称的行
            dept_rows = self.find_elements((By.XPATH, "//table//tr"))
            for row in dept_rows:
                if department_name in row.text:
                    # 点击编辑按钮
                    edit_button = row.find_element(*self.EDIT_DEPARTMENT)
                    edit_button.click()
                    time.sleep(1)  # 等待对话框打开
                    
                    # 填写新信息
                    if new_name:
                        self.input_text(self.EDIT_DEPARTMENT_NAME_INPUT, new_name)
                    if new_remarks:
                        self.input_text(self.EDIT_REMARKS_INPUT, new_remarks)
                    
                    # 点击确认按钮
                    self.click(self.EDIT_DEPARTMENT_CONFIRM_BUTTON)
                    time.sleep(2)  # 等待操作完成
                    
                    # 验证成功消息
                    return self.is_element_visible(self.EDIT_DEPARTMENT_SUCCESS_MESSAGE, timeout=5)
            return False
        except Exception as e:
            self.logger.error(f"编辑部门失败: {e}")
            return False
    
    def delete_department(self, department_name):
        """
        删除部门
        
        Args:
            department_name: 要删除的部门名称
        
        Returns:
            bool: 是否成功删除
        """
        try:
            # 找到包含指定部门名称的行
            dept_rows = self.find_elements((By.XPATH, "//table//tr"))
            for row in dept_rows:
                if department_name in row.text:
                    # 点击删除按钮
                    delete_button = row.find_element(*self.DELETE_DEPARTMENT)
                    delete_button.click()
                    time.sleep(1)  # 等待确认对话框
                    
                    # 点击确认删除（假设会弹出确认对话框）
                    confirm_delete = self.find_element((By.XPATH, "//button[contains(., '确认')]"))
                    confirm_delete.click()
                    time.sleep(2)  # 等待操作完成
                    return True
            return False
        except Exception as e:
            self.logger.error(f"删除部门失败: {e}")
            return False
