from selenium.webdriver.common.by import By


class UserManagementLocators:
    """用户管理定位器"""
# 新增  
    # 新建用户按钮
    USER_ADD_BUTTON = (By.XPATH, "//button[normalize-space(.)='新建用户']")
    # 表单字段
    # 部门选择
    DEPARTMENT_SELECT = (By.XPATH, "//label[contains(normalize-space(.), '所属部门')]/following-sibling::div//input")
    # 部门下拉：用于点击展开下拉框（选择器外壳）
    DEPARTMENT_DROPDOWN_TOGGLE = (By.XPATH, "//label[contains(normalize-space(.), '所属部门')]/following-sibling::div//div[contains(@class,'el-select') or contains(@class,'select')]")
    # 推荐的相对定位：下拉容器内的第一项（更稳健）
    DEPARTMENT_FIRST_OPTION = (By.XPATH, "(//div[contains(@class,'el-select-dropdown') or contains(@class,'el-popper')]//li)[1]")
    # 昵称输入框
    NICKNAME_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '昵称')]/following-sibling::div//input")    
    # 登录账号输入框
    ACCOUNT_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '登录账号')]/following-sibling::div//input")   
    # 手机号输入框
    PHONE_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '手机号')]/following-sibling::div//input")      
    # 性别选择
    GENDER_MALE = (By.XPATH, "//label[contains(normalize-space(.), '性别')]/following-sibling::div//span[normalize-space(.)='男']")
    GENDER_FEMALE = (By.XPATH, "//label[contains(normalize-space(.), '性别')]/following-sibling::div//span[normalize-space(.)='女']")   
    # 角色选择
    ROLE_SELECT = (By.XPATH, "//label[contains(normalize-space(.), '角色')]/following-sibling::div//input")
    # 头像（上传区/文件输入）
    AVATAR_UPLOAD_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '头像')]/following-sibling::div//input[@type='file']")
    AVATAR_UPLOAD_AREA = (By.XPATH, "//label[contains(normalize-space(.), '头像')]/following-sibling::div//*[contains(@class,'upload') or contains(@class,'avatar') or contains(@class,'el-upload')]")
    # 密码输入框
    ADD_PASSWORD_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '密码')]/following-sibling::div//input[@type='password']")    
    # 确认密码输入框
    ADD_CONFIRM_PASSWORD_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '确认密码')]/following-sibling::div//input[@type='password']")    
    # 操作按钮
    CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(.)='确认']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(.)='取消']")
# 编辑
    Edit_USER=(By.XPATH, "//button[normalize-space(.)='修改']")
    Edit_NICKNAME_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '昵称')]/following-sibling::div//input")
# 删除
    Delete_USER=(By.XPATH, "//button[normalize-space(.)='删除']")

# 部门
# 新增部门
    Add_DEPARTMENT=(By.XPATH, "//button[normalize-space(.)='新增部门']")
    # 新增部门表单字段
    Add_Department_NAME_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '部门名称')]/following-sibling::div//input")
    Add_Remarks_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '备注')]/following-sibling::div//input")
    # 新增部门操作按钮
    Add_Department_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(.)='确认']")
    Add_Department_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(.)='取消']")
    # 新增部门成功提示
    Add_Department_SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'el-message') and contains(.,'新增成功')]")
# 新增子部门
    Add_Sub_DEPARTMENT=(By.XPATH, "//button[normalize-space(.)='新增子部门']")
    # 新增子部门表单字段
    Add_Sub_Department_NAME_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '子部门名称')]/following-sibling::div//input")
    Add_Sub_Remarks_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '备注')]/following-sibling::div//input")
    # 新增子部门操作按钮
    Add_Sub_Department_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(.)='确认']")
    Add_Sub_Department_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(.)='取消']")
    # 新增子部门成功提示
    Add_Sub_Department_SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'el-message') and contains(.,'新增成功')]")
# 编辑部门
    Edit_DEPARTMENT=(By.XPATH, "//button[normalize-space(.)='修改']")
    Edit_Department_NAME_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '部门名称')]/following-sibling::div//input")
    Edit_Remarks_INPUT = (By.XPATH, "//label[contains(normalize-space(.), '备注')]/following-sibling::div//input")
    # 编辑部门操作按钮
    Edit_Department_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(.)='确认']")
    Edit_Department_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(.)='取消']")
    # 编辑部门成功提示
    Edit_Department_SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'el-message') and contains(.,'修改成功')]")
# 删除部门
    Delete_DEPARTMENT=(By.XPATH, "//button[normalize-space(.)='删除']")
