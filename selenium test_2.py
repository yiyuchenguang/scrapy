from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import re
import time
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(
    executable_path=r"C:\MKSProjects\Vision Test Environment\CANoe\Geely_GEEA2\Tools\myPython\chromedriver.exe",
    options=chrome_options)
browser.get("https://so.gushiwen.cn/shiwen/default_1Acde790aa3213A1.aspx")
browser.implicitly_wait(3)

# typecontent = browser.find_elements_by_xpath('.//div[@class ="sons"]//div[@class="typecont"]')
# print(typecontent)
# item ={}
# for child in typecontent:
#     bookMl = child.find_element_by_class_name('bookMl').text
#     urls = child.find_elements_by_xpath('.//span//a')#.get_attribute('href')
#     urls = [i.get_attribute('href') for i in urls]
#     print(bookMl)
#     print(urls)
item ={}

sons = browser.find_elements_by_xpath(".//div[@class='left']//div[@class='sons']")

for son in sons:
    title = son.find_element_by_xpath(".//div[@class = 'cont']//p//a//b").text

    item['poem_title'] = title

    source = son.find_elements_by_xpath(".//div[@class = 'cont']//p[@class = 'source']/a")
    author = [i.text.strip() for i in source]
    item['poem_author'] = '.'.join(author)

    contson = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']")
    body = [i.text.strip() for i in contson]
    item['poem_body'] = ''.join(body)

    yi_button = son.find_element_by_xpath(
        "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'译')]")
    yi_button.click()
    time.sleep(0.2)

    yi = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']//p//span")
    yi = [i.text.strip() for i in yi]
    item['poem_yi'] = ''.join(yi)
    yi_button.click()
    time.sleep(0.2)

    zhu_button = son.find_element_by_xpath(
        "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'注')]")
    zhu_button.click()
    time.sleep(0.2)

    zhu = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']//p//span")
    zhu = [i.text.strip() for i in zhu]
    item['poem_zhu'] = ''.join(zhu)
    zhu_button.click()
    time.sleep(0.2)

    shang_button = son.find_element_by_xpath(
        "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'赏')]")
    shang_button.click()
    time.sleep(0.5)

    shang = son.find_elements_by_xpath(
        ".//div[@class = 'cont']//div[@class = 'contson']//div[@class = 'hr']/following-sibling::p[not(@style)]")
    shang = [i.text.strip() for i in shang]
    item['poem_shang'] = ''.join(shang)
    shang_button.click()
    time.sleep(0.5)

    print(item)