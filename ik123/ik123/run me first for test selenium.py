from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyperclip
import pyautogui
import time
import os

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('useAutomationExtension', False)

browser_path = r"../../chromedriver_win32/chromedriver_win32/chromedriver.exe"

print(os.path.abspath(browser_path))


# 尝试传参
s = Service(executable_path = browser_path)


browser = webdriver.Chrome(service=s, options=chrome_options)
browser.get("http://p.ik123.com/bizhi/75491.html")
browser.implicitly_wait(10)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight) ')  # 滚动条拉取
print(browser.title)

#pic = browser.find_elements_by_xpath("//div[@id='gui_left']//img")
pic = browser.find_elements(By.XPATH,r"//div[@id='gui_left']//img")
pic_urls = [i.get_attribute('src') for i in pic]
pic_names = [i.split('/')[-1:][0] for i in pic_urls]
pic_root = os.path.abspath(os.path.dirname(os.getcwd()))
image_file = os.path.join(pic_root, 'image')
if not os.path.exists(image_file):
    os.makedirs(image_file)
pic_rejoin_path = [os.path.join(image_file,i) for i in pic_names]
print(pic_rejoin_path)


for i in range(len(pic)):
    actions = ActionChains(browser)
    # 找到图片后右键单击图片
    actions.move_to_element(pic[i]) # 定位到元素
    actions.context_click(pic[i]) # 点击右键
    actions.perform()  # 执行

    pyautogui.typewrite(['v']) # v 是保存的快捷键
    pyperclip.copy(pic_rejoin_path[i]) # 把 指定的路径拷贝到过来
    time.sleep(1)  # 等待一秒
    pyautogui.hotkey('ctrlleft', 'v')# 粘贴
    pyautogui.press('enter')
    time.sleep(1)  # 等待一秒
    print("图片下载完成")

