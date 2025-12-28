from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CourseAutoplayer:
    def __init__(self, browser='chrome', implicit_wait=10):
        """
        初始化自动播放课程类
        :param browser: 浏览器类型，支持'chrome'、'firefox'、'edge'
        :param implicit_wait: 隐式等待时间（秒）
        """
        self.browser = browser
        self.driver = self._init_browser()
        self.driver.implicitly_wait(implicit_wait)
        self.wait = WebDriverWait(self.driver, 20)
    
    def _init_browser(self):
        """初始化浏览器"""
        logger.info(f'初始化{self.browser}浏览器...')
        if self.browser.lower() == 'chrome':
            options = webdriver.ChromeOptions()
            # 添加无头模式等选项（可选）
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
            return webdriver.Chrome(options=options)
        elif self.browser.lower() == 'firefox':
            options = webdriver.FirefoxOptions()
            return webdriver.Firefox(options=options)
        elif self.browser.lower() == 'edge':
            options = webdriver.EdgeOptions()
            return webdriver.Edge(options=options)
        else:
            raise ValueError(f'不支持的浏览器类型: {self.browser}')
    
    def login(self, url, username, password, username_locator, password_locator, login_btn_locator):
        """
        登录课程平台
        :param url: 登录页面URL
        :param username: 用户名
        :param password: 密码
        :param username_locator: 用户名输入框定位器，格式：(By.ID, 'id_value') 或 (By.XPATH, 'xpath_value')
        :param password_locator: 密码输入框定位器
        :param login_btn_locator: 登录按钮定位器
        """
        logger.info(f'访问登录页面: {url}')
        self.driver.get(url)
        
        try:
            # 输入用户名
            username_elem = self.wait.until(EC.presence_of_element_located(username_locator))
            username_elem.clear()
            username_elem.send_keys(username)
            logger.info('用户名输入成功')
            
            # 输入密码
            password_elem = self.wait.until(EC.presence_of_element_located(password_locator))
            password_elem.clear()
            password_elem.send_keys(password)
            logger.info('密码输入成功')
            
            # 点击登录按钮
            login_btn = self.wait.until(EC.element_to_be_clickable(login_btn_locator))
            login_btn.click()
            logger.info('登录按钮点击成功')
            
            # 等待登录成功（可根据实际情况调整）
            time.sleep(5)
            logger.info('登录成功')
            return True
        except TimeoutException as e:
            logger.error(f'登录超时: {e}')
            return False
        except NoSuchElementException as e:
            logger.error(f'找不到登录元素: {e}')
            return False
    
    def navigate_to_course_list(self, course_list_url):
        """
        导航到课程列表页面
        :param course_list_url: 课程列表页面URL
        """
        logger.info(f'导航到课程列表: {course_list_url}')
        self.driver.get(course_list_url)
        time.sleep(3)
    
    def get_course_links(self, course_link_locator):
        """
        获取课程链接列表
        :param course_link_locator: 课程链接定位器，如 (By.CSS_SELECTOR, '.course-link')
        :return: 课程链接元素列表
        """
        try:
            course_links = self.wait.until(EC.presence_of_all_elements_located(course_link_locator))
            logger.info(f'找到{len(course_links)}个课程链接')
            return course_links
        except TimeoutException as e:
            logger.error(f'获取课程链接超时: {e}')
            return []
    
    def play_course(self, course_link, video_locator, next_btn_locator, play_btn_locator=None):
        """
        播放单个课程视频
        :param course_link: 课程链接元素
        :param video_locator: 视频元素定位器
        :param next_btn_locator: 下一课按钮定位器
        :param play_btn_locator: 播放按钮定位器（如果视频需要手动点击播放）
        """
        try:
            # 点击进入课程
            course_title = course_link.text.strip()
            logger.info(f'开始播放课程: {course_title}')
            course_link.click()
            time.sleep(5)
            
            # 找到视频元素
            video = self.wait.until(EC.presence_of_element_located(video_locator))
            
            # 如果需要点击播放按钮
            if play_btn_locator:
                try:
                    play_btn = self.wait.until(EC.element_to_be_clickable(play_btn_locator))
                    play_btn.click()
                    logger.info('点击播放按钮')
                    time.sleep(2)
                except TimeoutException:
                    logger.warning('未找到播放按钮或视频已自动播放')
            
            # 播放视频（监控视频是否结束）
            self._monitor_video_play(video)
            
            # 点击下一课
            try:
                next_btn = self.wait.until(EC.element_to_be_clickable(next_btn_locator))
                next_btn.click()
                logger.info('点击下一课按钮')
                time.sleep(3)
                return True
            except TimeoutException:
                logger.info('已到达最后一课，没有下一课按钮')
                return False
        except Exception as e:
            logger.error(f'播放课程时出错: {e}')
            return False
    
    def _monitor_video_play(self, video, check_interval=30):
        """
        监控视频播放状态
        :param video: 视频元素
        :param check_interval: 检查间隔（秒）
        """
        logger.info('开始监控视频播放')
        while True:
            try:
                # 获取视频当前播放时间和总时长
                current_time = float(self.driver.execute_script("return arguments[0].currentTime;", video))
                duration = float(self.driver.execute_script("return arguments[0].duration;", video))
                
                logger.info(f'视频播放进度: {current_time:.1f}s / {duration:.1f}s')
                
                # 检查视频是否已结束（当前时间接近总时长或已暂停超过阈值）
                if duration - current_time < 1.0:
                    logger.info('视频播放结束')
                    break
                
                # 检查视频是否暂停，如果暂停则继续播放
                paused = self.driver.execute_script("return arguments[0].paused;", video)
                if paused:
                    logger.warning('视频已暂停，尝试继续播放')
                    self.driver.execute_script("arguments[0].play();", video)
                
                time.sleep(check_interval)
            except Exception as e:
                logger.error(f'监控视频时出错: {e}')
                time.sleep(check_interval)
    
    def auto_play_all_courses(self, course_list_url, course_link_locator, video_locator, next_btn_locator, play_btn_locator=None):
        """
        自动播放所有课程
        :param course_list_url: 课程列表页面URL
        :param course_link_locator: 课程链接定位器
        :param video_locator: 视频元素定位器
        :param next_btn_locator: 下一课按钮定位器
        :param play_btn_locator: 播放按钮定位器（可选）
        """
        # 导航到课程列表
        self.navigate_to_course_list(course_list_url)
        
        # 获取课程链接
        course_links = self.get_course_links(course_link_locator)
        
        if not course_links:
            logger.error('未找到课程链接，无法自动播放')
            return
        
        # 依次播放每个课程
        for i, course_link in enumerate(course_links):
            logger.info(f'开始播放第{i+1}/{len(course_links)}个课程')
            
            # 重新获取课程链接（因为页面可能刷新）
            course_links = self.get_course_links(course_link_locator)
            if i >= len(course_links):
                logger.error(f'无法获取第{i+1}个课程链接')
                break
            
            # 播放课程
            success = self.play_course(course_links[i], video_locator, next_btn_locator, play_btn_locator)
            
            if not success:
                logger.warning(f'第{i+1}个课程播放失败，尝试播放下一个')
                
            # 返回课程列表页面
            self.navigate_to_course_list(course_list_url)
            time.sleep(3)
    
    def close(self):
        """
        关闭浏览器
        """
        logger.info('关闭浏览器')
        self.driver.quit()

def main():
    """
    主函数示例
    根据实际课程平台修改配置
    """
    # 初始化自动播放类
    autoplayer = CourseAutoplayer(browser='chrome')
    
    try:
        # 登录配置
        login_url = 'https://example.com/login'  # 替换为实际登录URL
        username = 'your_username'  # 替换为实际用户名
        password = 'your_password'  # 替换为实际密码
        
        # 定位器配置（根据实际网页结构修改）
        username_locator = (By.ID, 'username')  # 替换为实际用户名输入框ID或XPATH
        password_locator = (By.ID, 'password')  # 替换为实际密码输入框ID或XPATH
        login_btn_locator = (By.ID, 'login-btn')  # 替换为实际登录按钮ID或XPATH
        
        # 登录
        autoplayer.login(login_url, username, password, username_locator, password_locator, login_btn_locator)
        
        # 课程列表配置
        course_list_url = 'https://example.com/courses'  # 替换为实际课程列表URL
        course_link_locator = (By.CSS_SELECTOR, '.course-item a')  # 替换为实际课程链接选择器
        
        # 视频播放配置
        video_locator = (By.TAG_NAME, 'video')  # 替换为实际视频元素定位器
        next_btn_locator = (By.ID, 'next-lesson-btn')  # 替换为实际下一课按钮定位器
        play_btn_locator = None  # 如果需要点击播放按钮，替换为实际定位器
        
        # 自动播放所有课程
        autoplayer.auto_play_all_courses(course_list_url, course_link_locator, video_locator, next_btn_locator, play_btn_locator)
        
    except Exception as e:
        logger.error(f'程序运行出错: {e}')
    finally:
        # 关闭浏览器
        autoplayer.close()

if __name__ == '__main__':
    main()
