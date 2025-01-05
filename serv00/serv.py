from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import time

# 自动填表单功能

# 配置 Firefox 浏览器
options = Options()
options.headless = False  # 设为 True 可以使浏览器在后台运行

# 设置 Firefox 驱动程序的位置
service = Service('geckodriver.exe')  # 请将 /path/to/geckodriver 替换为你本地的 geckodriver 路径

# 打开 Firefox 浏览器
driver = webdriver.Firefox(service=service, options=options)

# 访问网站
driver.get('https://www.serv00.com/offer/create_new_account')

# 填写表单
driver.find_element(By.ID, 'id_first_name').send_keys('kaka')
driver.find_element(By.ID, 'id_last_name').send_keys('luote')
driver.find_element(By.ID, 'id_username').send_keys('bestdravench')
driver.find_element(By.ID, 'id_email').send_keys('bestdravench@gmail.com')
driver.find_element(By.ID, 'id_question').send_keys('0')
driver.find_element(By.ID, 'id_tos').click()

# 等待页面加载并找到验证码图片
time.sleep(3)  # 等待3秒以确保页面加载完全
captcha_element = driver.find_element(By.CSS_SELECTOR, 'img.captcha.is-')

# 截图并保存验证码图片
captcha_location = captcha_element.location
captcha_size = captcha_element.size
driver.save_screenshot('screenshot.png')
captcha_image = Image.open('screenshot.png')

# 裁剪验证码图片
left = captcha_location['x']
top = captcha_location['y']
right = captcha_location['x'] + captcha_size['width']
bottom = captcha_location['y'] + captcha_size['height']
captcha_image = captcha_image.crop((left, top, right, bottom))
captcha_image.save('captcha.png')

# 预处理验证码图片
captcha_image = captcha_image.convert('L')  # 转为灰度图像
captcha_image = captcha_image.filter(ImageFilter.MedianFilter())  # 使用中值滤波去除噪点
enhancer = ImageEnhance.Contrast(captcha_image)
captcha_image = enhancer.enhance(2)  # 增强对比度
captcha_image.save('preprocessed_captcha.png')

# 使用 pytesseract 识别验证码
custom_config = r'--oem 3 --psm 6'
captcha_text = pytesseract.image_to_string(captcha_image, config=custom_config)
print('验证码文本:', captcha_text)

# 填写验证码
driver.find_element(By.ID, 'id_captcha_1').send_keys(captcha_text)

# 提交表单
driver.find_element(By.XPATH, '/html/body/section/div/div[2]/div[2]/form/p[9]/button').click()

# 关闭浏览器
# driver.quit()



