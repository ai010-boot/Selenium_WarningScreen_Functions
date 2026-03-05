from selenium.webdriver.common.by import By

# 设备管理定位器
class DeviceManagementLocators:
    """设备管理定位器"""
    # 设备管理进入
    DEVICE_MANAGEMENT = (By.XPATH, "//*[@id='app']/div[1]/div[1]/div[2]/div[2]")
    # 新增设备按钮
    DEVICE_ADD_BUTTON = (By.XPATH, "//button[normalize-space(.)='新增设备']")
    
    # 新增设备对话框
    ADD_DEVICE_DIALOG = (By.XPATH, "//div[contains(@class, 'dialog') and contains(@class, 'visible')]")
    DIALOG_TITLE = (By.XPATH, "//div[contains(@class, 'dialog')]//h3[text()='新增设备']")
    
    # 表单字段
    DEPARTMENT_INPUT = (By.XPATH, "//label[text()='所属单位']/following-sibling::input")
    PRODUCT_SELECT = (By.XPATH, "//label[text()='所属产品']/following-sibling::select")
    DEVICE_NAME_INPUT = (By.XPATH, "//label[text()='设备名称']/following-sibling::input")
    DEVICE_CODE_INPUT = (By.XPATH, "//label[text()='设备编号']/following-sibling::input")
    DEVICE_GROUP_SELECT = (By.XPATH, "//label[text()='设备分组']/following-sibling::select")
    DEVICE_LOCATION_SELECT = (By.XPATH, "//label[text()='设备定位']/following-sibling::select")
    INSTALLATION_POSITION_INPUT = (By.XPATH, "//label[text()='安装位置']/following-sibling::input")
    REMARKS_INPUT = (By.XPATH, "//label[text()='备注']/following-sibling::input")
    
    # 设备定位地图对话框
    LOCATION_MAP_DIALOG = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '请选择设备定位')]")
    LOCATION_SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder, '输入关键字选取地点')]")
    MAP_CONTAINER = (By.XPATH, "//div[contains(@class, 'map')]")
    MAP_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '请选择设备定位')]//button[text()='确定']")
    MAP_CLOSE_BUTTON = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '请选择设备定位')]//button[text()='×' or @class='close']")
    
    # 对话框按钮
    CANCEL_BUTTON = (By.XPATH, "//div[contains(@class, 'dialog')]//button[text()='取消']")
    CONFIRM_BUTTON = (By.XPATH, "//div[contains(@class, 'dialog')]//button[text()='确定']")
    
    # 设备列表
    DEVICE_LIST_TABLE = (By.XPATH, "//table[contains(@class, 'device-list')]")
    DEVICE_LIST_ROWS = (By.XPATH, "//table[contains(@class, 'device-list')]//tbody//tr")
    
    # 操作按钮
    EDIT_DEVICE_BUTTON = (By.XPATH, "//button[contains(., '修改')]")
    DELETE_DEVICE_BUTTON = (By.XPATH, "//button[contains(., '删除')]")
    VIEW_DEVICE_BUTTON = (By.XPATH, "//button[contains(., '详情')]")
    MORE_BUTTON = (By.XPATH, "//button[contains(., '更多')]")
    
    # 编辑设备对话框
    EDIT_DEVICE_DIALOG = (By.XPATH, "//div[contains(@class, 'dialog') and contains(@class, 'visible')]")
    EDIT_DIALOG_TITLE = (By.XPATH, "//div[contains(@class, 'dialog')]//h3[text()='编辑设备']")
    
    # 编辑设备表单字段（可编辑字段）- Vue3 兼容定位
    EDIT_DEVICE_NAME_INPUT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='设备名称']/following-sibling::div//button[@type='button']")
    EDIT_DEVICE_GROUP_SELECT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='设备分组']/following-sibling::div//input")
    DEVICE_GROUP_DROPDOWN = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]")
    DEVICE_GROUP_OPTIONS = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]//li")
    CAMERA_SCENE_SELECT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='摄像头场景']/following-sibling::div//input")
    CAMERA_SCENE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]")
    CAMERA_SCENE_OPTIONS = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]//li")
    EDIT_DEVICE_LOCATION_INPUT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='设备定位']/following-sibling::input")
    EDIT_INSTALLATION_POSITION_INPUT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='安装位置']/following-sibling::input")
    EDIT_REMARKS_INPUT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='备注']/following-sibling::textarea")
    
    # 不可编辑字段（显示用）
    EDIT_DEPARTMENT_INPUT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='所属单位']/following-sibling::input")
    EDIT_PRODUCT_INPUT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='所属产品']/following-sibling::input")
    EDIT_DEVICE_CODE_INPUT = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '编辑设备')]//label[text()='设备编号']/following-sibling::input")
    
    # 成功消息
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'success') and contains(@class, 'message')]")
    
    # 错误消息
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'error') and contains(@class, 'message')]")
    
    # 删除确认对话框
    DELETE_CONFIRM_DIALOG = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '确认删除')]")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '确认删除')]//button[text()='确定']")
    DELETE_CANCEL_BUTTON = (By.XPATH, "//div[contains(@class, 'dialog') and contains(., '确认删除')]//button[text()='取消']")
    
    # 更多下拉菜单
    MORE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]")
    DELETE_DEVICE_MENU_ITEM = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]//li[contains(., '删除设备')]")
    ASSOCIATE_DEVICE_MENU_ITEM = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]//li[contains(., '关联设备')]")
    SHIELD_SETTINGS_MENU_ITEM = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]//li[contains(., '屏蔽设置')]")
    DEVICE_LINKAGE_MENU_ITEM = (By.XPATH, "//div[contains(@class, 'dropdown') and contains(@class, 'visible')]//li[contains(., '设备联动')]")
