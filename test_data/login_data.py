"""
登录测试数据
"""

# 有效登录数据
VALID_LOGIN_DATA = {
    'username': 'jkcsdw',
    'password': '123456'
}

# 无效登录数据
INVALID_LOGIN_DATA = [
    {
        'username': 'invalid_user',
        'password': 'password123',
        'description': '无效用户名'
    },
    {
        'username': 'testuser',
        'password': 'wrong_password',
        'description': '错误密码'
    },
    {
        'username': '',
        'password': 'password123',
        'description': '空用户名'
    },
    {
        'username': 'testuser',
        'password': '',
        'description': '空密码'
    },
    {
        'username': '',
        'password': '',
        'description': '空凭证'
    }
]

# # SQL 注入测试数据
# SQL_INJECTION_DATA = [
#     "admin' OR '1'='1",
#     "admin'--",
#     "admin' #",
#     "' OR '1'='1' --",
#     "1' OR '1' = '1",
# ]

# # XSS 攻击测试数据
# XSS_ATTACK_DATA = [
#     "<script>alert('XSS')</script>",
#     "<img src=x onerror=alert('XSS')>",
#     "javascript:alert('XSS')",
#     "<svg/onload=alert('XSS')>",
# ]

# # 边界测试数据
# BOUNDARY_TEST_DATA = {
#     'max_length_username': 'a' * 255,
#     'max_length_password': 'p' * 255,
#     'special_chars_username': '!@#$%^&*()',
#     'unicode_username': '用户名123',
# }
