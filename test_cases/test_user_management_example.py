"""
用户管理页面测试用例
"""

import pytest
import time
from pages.user_management_page import UserManagementPage
from test_data.test_data_config import get_test_data


class TestUserManagementDataDriven:
    """
    使用 authenticated_driver + CSV 数据驱动的示例：
    - 会话开始时自动登录并进入后台管理
    - 多个测试复用同一浏览器和登录状态
    - 使用 CSV 数据驱动，避免硬编码数据（包含密码、头像路径等）
    - 提升测试速度，减少重复代码
    """

    def test_01_user_management_page_loaded(self, authenticated_driver):
        """验证：用户管理页面已加载（必须成功才能进行后续测试）"""
        page = UserManagementPage(authenticated_driver)
        
        # 确认"新建用户"按钮可见
        assert page.is_element_visible(page.USER_ADD_BUTTON, timeout=5), \
            "Should see USER_ADD_BUTTON on the page after login"
        
        page.logger.info("✓ 用户管理页面加载成功")

    def test_02_click_add_user_button(self, authenticated_driver):
        """验证：点击"新建用户"按钮打开对话框"""
        page = UserManagementPage(authenticated_driver)
        
        # 点击"新建用户"按钮
        page.click(page.USER_ADD_BUTTON)
        
        # 等待表单出现（例如昵称输入框）
        time.sleep(1)  # 给弹窗打开一些时间
        assert page.is_element_visible(page.NICKNAME_INPUT, timeout=5), \
            "Should see form after clicking USER_ADD_BUTTON"
        
        page.logger.info("✓ 新建用户对话框打开成功")

    @pytest.mark.parametrize("test_data", get_test_data('user_management', 'csv'))
    def test_03_fill_user_form_complete(self, authenticated_driver, test_data):
        """数据驱动测试：填写完整的用户表单（包括密码和头像）
        
        从 CSV 文件读取测试数据，每一行执行一次测试。
        
        CSV 字段说明：
        - account: 登录账号
        - nickname: 昵称
        - phone: 手机号
        - gender: 性别（男/女）
        - password: 密码
        - confirm_password: 确认密码
        - avatar_path: 头像文件完整路径（可选，留空则跳过上传）
        - expected_result: 期望结果（success/failure）
        - description: 用例描述
        """
        page = UserManagementPage(authenticated_driver)
        
        # 确保对话框已打开
        if not page.is_element_visible(page.NICKNAME_INPUT, timeout=2):
            page.click(page.USER_ADD_BUTTON)
            time.sleep(1)
        
        # ========== 从 CSV 数据中提取字段 ==========
        account = test_data.get('account', '').strip()
        nickname = test_data.get('nickname', '').strip()
        phone = test_data.get('phone', '').strip()
        gender = test_data.get('gender', '男').strip()
        password = test_data.get('password', '').strip()
        confirm_password = test_data.get('confirm_password', '').strip()
        avatar_path = test_data.get('avatar_path', '').strip()
        expected_result = test_data.get('expected_result', 'success').strip()
        description = test_data.get('description', '数据驱动测试').strip()
        
        page.logger.info(f"\n{'='*60}")
        page.logger.info(f"数据驱动测试: {description}")
        page.logger.info(f"  账号: {account}")
        page.logger.info(f"  昵称: {nickname}")
        page.logger.info(f"  手机: {phone}")
        page.logger.info(f"  性别: {gender}")
        page.logger.info(f"  密码: {'*' * len(password) if password else '(空)'}")
        page.logger.info(f"  头像: {avatar_path if avatar_path else '(未上传)'}")
        page.logger.info(f"{'='*60}")
        
        try:
            # ========== 填写基本信息 ==========
            page.input_text(page.NICKNAME_INPUT, nickname)
            page.logger.info(f"  ✓ 已填昵称")
            
            page.input_text(page.ACCOUNT_INPUT, account)
            page.logger.info(f"  ✓ 已填账号")
            
            page.input_text(page.PHONE_INPUT, phone)
            page.logger.info(f"  ✓ 已填手机")
            
            # 选择性别
            if gender == '女':
                page.click(page.GENDER_FEMALE)
            else:
                page.click(page.GENDER_MALE)
            page.logger.info(f"  ✓ 已选性别: {gender}")
            
            # ========== 填写密码 ==========
            page.input_text(page.ADD_PASSWORD_INPUT, password)
            page.logger.info(f"  ✓ 已填密码")
            
            page.input_text(page.ADD_CONFIRM_PASSWORD_INPUT, confirm_password)
            page.logger.info(f"  ✓ 已填确认密码")
            
            # ========== 上传头像（如果提供） ==========
            if avatar_path and avatar_path.strip():
                try:
                    avatar_input = page.find_element(page.AVATAR_UPLOAD_INPUT, timeout=2)
                    avatar_input.send_keys(avatar_path)
                    page.logger.info(f"  ✓ 已上传头像: {avatar_path}")
                except Exception as e:
                    page.logger.warning(f"  ⚠ 头像上传失败: {e}")
            
            # ========== 验证表单 ==========
            assert page.is_element_visible(page.CONFIRM_BUTTON), \
                "确认按钮应该在表单中可见"
            page.logger.info(f"  ✓ 确认按钮可见")
            
            # ========== 断言期望结果 ==========
            if expected_result == 'success':
                # 验证必填字段都已填写
                assert account and nickname and phone and password, \
                    f"必填字段不能为空: account={bool(account)}, nickname={bool(nickname)}, phone={bool(phone)}, password={bool(password)}"
                page.logger.info(f"\n✓ 测试通过: {description}\n")
            
        except Exception as e:
            page.logger.error(f"\n✗ 测试失败: {description}")
            page.logger.error(f"  错误信息: {e}\n")
            if expected_result == 'failure':
                page.logger.info(f"✓ 符合预期失败 (expected_result=failure)\n")
            else:
                raise

    def test_04_verify_all_form_elements(self, authenticated_driver):
        """验证：表单中的所有主要元素都存在"""
        page = UserManagementPage(authenticated_driver)
        
        # 确保对话框打开
        if not page.is_element_visible(page.NICKNAME_INPUT, timeout=2):
            page.click(page.USER_ADD_BUTTON)
            time.sleep(1)
        
        # 列出要检查的所有元素
        elements_to_check = {
            "昵称输入框": page.NICKNAME_INPUT,
            "账号输入框": page.ACCOUNT_INPUT,
            "手机号输入框": page.PHONE_INPUT,
            "部门选择": page.DEPARTMENT_SELECT,
            "性别-男": page.GENDER_MALE,
            "性别-女": page.GENDER_FEMALE,
            "密码输入框": page.ADD_PASSWORD_INPUT,
            "确认密码输入框": page.ADD_CONFIRM_PASSWORD_INPUT,
            "头像上传区": page.AVATAR_UPLOAD_AREA,
            "确认按钮": page.CONFIRM_BUTTON,
            "取消按钮": page.CANCEL_BUTTON,
        }
        
        missing = []
        for name, locator in elements_to_check.items():
            try:
                if not page.is_element_visible(locator, timeout=1):
                    missing.append(name)
            except:
                missing.append(name)
        
        assert not missing, f"缺少以下表单元素：{missing}"
        page.logger.info(f"✓ 所有表单元素都存在（共 {len(elements_to_check)} 个）")

    def test_05_cancel_form(self, authenticated_driver):
        """验证：点击取消按钮关闭对话框"""
        page = UserManagementPage(authenticated_driver)
        
        # 确保对话框打开
        if not page.is_element_visible(page.CANCEL_BUTTON, timeout=2):
            page.click(page.USER_ADD_BUTTON)
            time.sleep(1)
        
        # 点击取消按钮
        page.click(page.CANCEL_BUTTON)
        time.sleep(1)
        
        # 验证对话框已关闭（昵称输入框不可见）
        is_closed = not page.is_element_visible(page.NICKNAME_INPUT, timeout=1)
        assert is_closed, "对话框应该在点击取消后关闭"
        
        page.logger.info("✓ 对话框已成功关闭")
    
    @pytest.mark.parametrize("test_data", get_test_data('department_management', 'csv'))
    def test_06_department_management(self, authenticated_driver, test_data):
        """数据驱动测试：部门管理功能
        
        从 CSV 文件读取测试数据，每一行执行一次测试。
        
        CSV 字段说明：
        - department_name: 部门名称
        - remarks: 备注
        - parent_department: 父部门名称（子部门时填写）
        - expected_result: 期望结果（success/failure）
        - description: 用例描述
        """
        page = UserManagementPage(authenticated_driver)
        
        # 从 CSV 数据中提取字段
        department_name = test_data.get('department_name', '').strip()
        remarks = test_data.get('remarks', '').strip()
        parent_department = test_data.get('parent_department', '').strip()
        expected_result = test_data.get('expected_result', 'success').strip()
        description = test_data.get('description', '数据驱动测试').strip()
        
        page.logger.info(f"\n{'='*60}")
        page.logger.info(f"数据驱动测试: {description}")
        page.logger.info(f"  部门名称: {department_name}")
        page.logger.info(f"  备注: {remarks if remarks else '(空)'}")
        page.logger.info(f"  父部门: {parent_department if parent_department else '(无)'}")
        page.logger.info(f"{'='*60}")
        
        try:
            if parent_department:
                # 新增子部门
                success = page.add_sub_department(department_name, remarks)
            else:
                # 新增部门
                success = page.add_department(department_name, remarks)
            
            if expected_result == 'success':
                assert success, f"部门操作失败: {description}"
                page.logger.info(f"\n✓ 测试通过: {description}\n")
            else:
                assert not success, f"部门操作应该失败: {description}"
                page.logger.info(f"\n✓ 符合预期失败: {description}\n")
                
        except Exception as e:
            page.logger.error(f"\n✗ 测试失败: {description}")
            page.logger.error(f"  错误信息: {e}\n")
            if expected_result == 'failure':
                page.logger.info(f"✓ 符合预期失败 (expected_result=failure)\n")
            else:
                raise

    def test_07_edit_department(self, authenticated_driver):
        """测试编辑部门功能"""
        page = UserManagementPage(authenticated_driver)
        
        # 先创建一个测试部门
        test_dept_name = f"test_dept_{int(time.time())}"
        page.add_department(test_dept_name, "初始备注")
        
        # 编辑部门
        new_name = f"updated_{test_dept_name}"
        new_remarks = "更新后的备注"
        success = page.edit_department(test_dept_name, new_name, new_remarks)
        
        assert success, "部门编辑失败"
        page.logger.info("✓ 部门编辑成功")

    def test_08_delete_department(self, authenticated_driver):
        """测试删除部门功能"""
        page = UserManagementPage(authenticated_driver)
        
        # 先创建一个测试部门
        test_dept_name = f"test_dept_{int(time.time())}"
        page.add_department(test_dept_name)
        
        # 删除部门
        success = page.delete_department(test_dept_name)
        
        assert success, "部门删除失败"
        page.logger.info("✓ 部门删除成功")
