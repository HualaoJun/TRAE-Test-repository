# TRAE-Test-repository
for hualao and dy. 
need python environment. 
after python, install selenium from pip. 
paste the command below into the terminal after you installed python: 
pip install selenium   
DO CONFIGURE BEFORE RUNNING THE PROGRAMME!type in the website of the video you need to play.


#### 1. 下载浏览器驱动

根据您使用的浏览器下载对应驱动，并确保驱动版本与浏览器版本匹配：

- **Chrome浏览器**：[ChromeDriver下载地址](https://developer.chrome.com/docs/chromedriver/downloads)
- **Firefox浏览器**：[geckodriver下载地址](https://github.com/mozilla/geckodriver/releases)
- **Edge浏览器**：[EdgeDriver下载地址](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

**注意**：下载后将驱动文件解压到系统PATH目录或与`course_autoplayer.py`同目录。

#### 2. 配置自动播放脚本

编辑`course_autoplayer.py`文件，修改`main()`函数中的配置参数：

```python
# 登录配置
login_url = 'https://example.com/login'  # 替换为您的课程平台登录URL
username = 'your_username'  # 替换为您的用户名
password = 'your_password'  # 替换为您的密码

# 定位器配置（根据网页结构修改）
username_locator = (By.ID, 'username')  # 用户名输入框定位器
password_locator = (By.ID, 'password')  # 密码输入框定位器
login_btn_locator = (By.ID, 'login-btn')  # 登录按钮定位器

# 课程列表配置
course_list_url = 'https://example.com/courses'  # 课程列表URL
course_link_locator = (By.CSS_SELECTOR, '.course-item a')  # 课程链接选择器

# 视频播放配置
video_locator = (By.TAG_NAME, 'video')  # 视频元素定位器
next_btn_locator = (By.ID, 'next-lesson-btn')  # 下一课按钮定位器
```

#### 3. 获取定位器的方法

1. 打开您的课程平台网页
2. 按`F12`打开开发者工具
3. 点击左上角的选择元素按钮（箭头图标）
4. 点击需要定位的元素（如用户名输入框）
5. 在开发者工具中右键点击该元素 → 复制 → 复制选择器/复制XPath

**示例**：如果复制的选择器是`#username`，则定位器为`(By.CSS_SELECTOR, '#username')`；如果复制的是XPath，则为`(By.XPATH, '//*[@id="username"]')`

#### 4. 运行自动播放程序

在命令行中执行：

```bash
python course_autoplayer.py
```

### 功能说明

- 📌 **自动登录**：使用配置的用户名密码自动登录课程平台
- 📌 **课程检测**：自动识别页面上的所有课程链接
- 📌 **视频监控**：实时监控视频播放状态，自动处理暂停情况
- 📌 **自动切换**：视频结束后自动点击下一课按钮
- 📌 **日志记录**：详细记录每一步操作，便于排查问题

### 常见问题解决

1. **浏览器驱动问题**：确保驱动版本与浏览器版本匹配，可在代码中指定驱动路径
2. **定位器错误**：重新检查定位器是否正确，建议使用ID或CSS选择器
3. **登录失败**：检查用户名密码是否正确，或是否有验证码等额外验证
4. **视频无法播放**：检查是否需要点击播放按钮，可配置`play_btn_locator`参数

现在您可以根据自己的课程平台配置脚本，开始享受自动连续播放课程的便利了！
