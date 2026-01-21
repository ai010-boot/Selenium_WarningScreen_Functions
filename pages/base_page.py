"""
基础页面类模块
所有页面对象类的基类，提供通用的页面操作方法
"""
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.common.action_chains import ActionChains
from config.config import Config
from utils.logger import Logger
from utils.screenshot import Screenshot


class BasePage:
    """所有页面对象的基类"""
    
    def __init__(self, driver):
        """
        初始化基础页面
        
        Args:
            driver: WebDriver 实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = Logger().get_logger()
        self.actions = ActionChains(driver)
    
    def find_element(self, locator, timeout=None):
        """
        查找单个元素
        
        Args:
            locator: 元素定位器 (By.ID, "element_id")
            timeout: 超时时间
        
        Returns:
            WebElement
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"找到元素: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"未找到元素: {locator}")
            Screenshot.take_screenshot(self.driver, "element_not_found")
            raise
    
    def find_elements(self, locator, timeout=None):
        """
        查找多个元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
        
        Returns:
            WebElement 列表
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            self.logger.debug(f"找到 {len(elements)} 个元素: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"未找到元素: {locator}")
            return []
    
    def click(self, locator, timeout=None):
        """
        点击元素
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"点击元素: {locator}")
        except Exception as e:
            self.logger.error(f"点击元素失败: {locator}, 错误: {e}")
            Screenshot.take_screenshot(self.driver, "click_failed")
            raise
    
    def input_text(self, locator, text, timeout=None):
        """
        输入文本
        
        Args:
            locator: 元素定位器
            text: 要输入的文本
            timeout: 超时时间
        """
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"输入文本到 {locator}: {text}")
        except Exception as e:
            self.logger.error(f"输入文本失败: {locator}, 错误: {e}")
            Screenshot.take_screenshot(self.driver, "input_failed")
            raise
    
    def get_text(self, locator, timeout=None):
        """
        获取元素文本
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
        
        Returns:
            元素文本内容
        """
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"获取元素文本 {locator}: {text}")
        return text
    
    def get_attribute(self, locator, attribute, timeout=None):
        """
        获取元素属性
        
        Args:
            locator: 元素定位器
            attribute: 属性名称
            timeout: 超时时间
        
        Returns:
            属性值
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        self.logger.debug(f"获取元素属性 {locator}.{attribute}: {value}")
        return value
    
    def is_element_visible(self, locator, timeout=None):
        """
        检查元素是否可见
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
        
        Returns:
            bool
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            self.logger.debug(f"元素可见: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"元素不可见: {locator}")
            return False
    
    def is_element_present(self, locator):
        """
        检查元素是否存在于 DOM 中
        
        Args:
            locator: 元素定位器
        
        Returns:
            bool
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """
        等待元素消失
        
        Args:
            locator: 元素定位器
            timeout: 超时时间
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.invisibility_of_element_located(locator))
        self.logger.debug(f"元素已消失: {locator}")
    
    def scroll_to_element(self, locator):
        """
        滚动到元素位置
        
        Args:
            locator: 元素定位器
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.debug(f"滚动到元素: {locator}")
    
    def hover_over_element(self, locator):
        """
        鼠标悬停在元素上
        
        Args:
            locator: 元素定位器
        """
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()
        self.logger.debug(f"鼠标悬停: {locator}")
    
    def switch_to_frame(self, frame_locator):
        """
        切换到 iframe
        
        Args:
            frame_locator: frame 定位器或索引
        """
        if isinstance(frame_locator, tuple):
            frame = self.find_element(frame_locator)
            self.driver.switch_to.frame(frame)
        else:
            self.driver.switch_to.frame(frame_locator)
        self.logger.debug(f"切换到 frame: {frame_locator}")
    
    def switch_to_default_content(self):
        """切换回主文档"""
        self.driver.switch_to.default_content()
        self.logger.debug("切换回主文档")
    
    def switch_to_window(self, window_index=-1):
        """
        切换到指定窗口
        
        Args:
            window_index: 窗口索引，默认切换到最新窗口
        """
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[window_index])
        self.logger.debug(f"切换到窗口: {window_index}")
    
    def execute_script(self, script, *args):
        """
        执行 JavaScript 脚本
        
        Args:
            script: JavaScript 代码
            *args: 脚本参数
        
        Returns:
            脚本执行结果
        """
        result = self.driver.execute_script(script, *args)
        self.logger.debug(f"执行脚本: {script}")
        return result
    
    def get_current_url(self):
        """获取当前页面 URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """获取页面标题"""
        return self.driver.title
    
    def refresh_page(self):
        """刷新页面"""
        self.driver.refresh()
        self.logger.info("刷新页面")
    
    def navigate_back(self):
        """后退"""
        self.driver.back()
        self.logger.info("浏览器后退")
    
    def navigate_forward(self):
        """前进"""
        self.driver.forward()
        self.logger.info("浏览器前进")
