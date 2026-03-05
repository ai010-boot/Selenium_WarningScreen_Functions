"""
设备管理页面测试用例
"""

import pytest
import time
from pages.Device_Management_Page import DeviceManagementPage
from test_data.test_data_config import get_test_data


class TestDeviceManagementDataDriven:
    """
    使用 authenticated_driver + CSV 数据驱动的示例：
    - 会话开始时自动登录并进入后台管理
    - 多个测试复用同一浏览器和登录状态
    - 使用 CSV 数据驱动，避免硬编码数据
    - 提升测试速度，减少重复代码
    """

    def test_01_device_management_page_loaded(self, authenticated_driver):
        """验证：设备管理页面已加载（必须成功才能进行后续测试）"""
        page = DeviceManagementPage(authenticated_driver)

        # 确认"新增设备"按钮可见
        assert page.is_element_visible(page.DEVICE_ADD_BUTTON, timeout=5), \
            "Should see DEVICE_ADD_BUTTON on the page after login"

        page.logger.info("✓ 设备管理页面加载成功")

    def test_02_click_add_device_button(self, authenticated_driver):
        """验证：点击"新增设备"按钮打开对话框"""
        page = DeviceManagementPage(authenticated_driver)

        # 点击"新增设备"按钮
        page.click(page.DEVICE_ADD_BUTTON)

        # 等待表单出现（例如设备名称输入框）
        time.sleep(1)  # 给弹窗打开一些时间
        assert page.is_element_visible(page.DEVICE_NAME_INPUT, timeout=5), \
            "Should see form after clicking DEVICE_ADD_BUTTON"

        page.logger.info("✓ 新增设备对话框打开成功")

    @pytest.mark.parametrize("test_data", get_test_data('device_management', 'csv'))
    def test_03_add_device_complete(self, authenticated_driver, test_data):
        """数据驱动测试：添加新设备

        从 CSV 文件读取测试数据，每一行执行一次测试。

        CSV 字段说明：
        - device_name: 设备名称
        - device_code: 设备编号
        - installation_position: 安装位置
        - remarks: 备注（可选）
        - expected_result: 期望结果（success/failure）
        - description: 用例描述
        """
        page = DeviceManagementPage(authenticated_driver)

        # ========== 从 CSV 数据中提取字段 ==========
        device_name = test_data.get('device_name', '').strip()
        device_code = test_data.get('device_code', '').strip()
        installation_position = test_data.get('installation_position', '').strip()
        remarks = test_data.get('remarks', '').strip()
        expected_result = test_data.get('expected_result', 'success').strip()
        description = test_data.get('description', '数据驱动测试').strip()

        page.logger.info(f"\n{'='*60}")
        page.logger.info(f"数据驱动测试: {description}")
        page.logger.info(f"  设备名称: {device_name}")
        page.logger.info(f"  设备编号: {device_code}")
        page.logger.info(f"  安装位置: {installation_position}")
        page.logger.info(f"  备注: {remarks}")
        page.logger.info(f"  期望结果: {expected_result}")

        # ========== 执行添加设备操作 ==========
        result = page.add_device(
            device_name=device_name,
            device_code=device_code,
            installation_position=installation_position,
            remarks=remarks
        )

        # ========== 验证结果 ==========
        if expected_result.lower() == 'success':
            assert result, f"添加设备失败: {device_name}"
            page.logger.info(f"✓ 成功添加设备: {device_name}")
        else:
            assert not result, f"预期失败但成功添加设备: {device_name}"
            page.logger.info(f"✓ 预期失败，设备添加失败: {device_name}")

    def test_04_edit_device_example(self, authenticated_driver):
        """示例：编辑设备（非数据驱动）"""
        page = DeviceManagementPage(authenticated_driver)

        # 示例：编辑第一个设备
        device_name = "测试设备001"
        new_name = "测试设备001_编辑"

        result = page.edit_device(
            device_name=device_name,
            new_device_name=new_name,
            installation_position="编辑后的位置"
        )

        assert result, f"编辑设备失败: {device_name}"
        page.logger.info(f"✓ 成功编辑设备: {device_name} -> {new_name}")

    def test_05_delete_device_example(self, authenticated_driver):
        """示例：删除设备（非数据驱动）"""
        page = DeviceManagementPage(authenticated_driver)

        # 示例：删除第一个设备
        device_name = "测试设备001_编辑"

        result = page.delete_device(device_name=device_name)

        assert result, f"删除设备失败: {device_name}"
        page.logger.info(f"✓ 成功删除设备: {device_name}")