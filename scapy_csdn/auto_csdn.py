import re
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os, random, shutil
import json
import traceback
from uploads_files import UploadFilesSelenium
from wigits import *


class ScriptCsdn(object):
    def __init__(self):
        self.driver = None
        self.browser_path = r"D:\Document\scrapy\chromedriver_win32\chromedriver_win32\chromedriver.exe"
        self.login_url = "https://passport.csdn.net/login?"
        self.start_url = "https://blog.csdn.net/qq_34414530?spm=1011.2415.3001.5343"
        self.new_article = "https://editor.csdn.net/md/?not_checkout=1&spm=1001.2014.3001.5352"
        self.image_folder = r"D:\Document\source\poem_created"
        self.image_folder_used = r"D:\Document\source\poem_created_used"
        self.mkdir(self.image_folder_used)

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False

    def init_chrome(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        s = Service(executable_path=self.browser_path)
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()
        self.driver.delete_all_cookies()
        # print(self.driver.get_window_rect())
        # print(self.driver.get_window_size())


    def random_move_dir(self, source_dir, target_dir):
        '''
        随机移动一个文件夹到另一个文件夹下
        :param source_dir:
        :param target_dir:
        :return:
        '''
        try:
            '''获取当前文件夹下的所有子文件夹名称'''
            images_dirs = []
            for root, dirs, files in os.walk(source_dir):
                for sub in dirs:
                    images_dirs.append(sub)

            sample = random.sample(images_dirs, 1)[0]
            # print(sample)
            source_sub_dir = os.path.join(source_dir, sample)
            print("移动:{}".format(source_sub_dir))
            target_sub_dir = os.path.join(target_dir, sample)
            if os.path.exists(target_sub_dir):
                shutil.rmtree(target_sub_dir, ignore_errors=True)
            '''copy后删除源子文件夹'''
            shutil.copytree(source_sub_dir, target_sub_dir)
            shutil.rmtree(source_sub_dir, ignore_errors=True)
            return target_sub_dir
        except:
            print(traceback.print_exc())

    def first_login(self, wait_time):
        '''
        第一次登录，需要人工登录
        :param wait_time:
        :return:
        '''
        # 记得写完整的url 包括http和https
        self.driver.get(self.login_url)
        # 程序打开网页后20秒内 “手动登陆账户”
        time.sleep(wait_time)
        self.driver.get(self.start_url)

    def save_cookies(self):
        '''
        保存浏览器的cookies
        :return:
        '''
        with open("cookies.txt", 'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(self.driver.get_cookies()))

    def inject_cookies(self):
        '''
        向浏览器中写入cookies
        :return:
        '''
        with open("cookies.txt", 'r') as f:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookies_list = json.load(f)
            for cookie in cookies_list:
                # 该字段有问题所以删除就可以
                if 'expiry' in cookie:
                    del cookie['expiry']
                self.driver.add_cookie(cookie)

    def main(self):
        self.driver.get(self.start_url)
        self.inject_cookies()
        self.driver.refresh()
        self.driver.get(self.new_article)

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//div[@class='editor']")))
        print(element)
        editor = self.driver.find_element(By.XPATH, ".//div[@class='editor']/pre")
        editor.send_keys(Keys.CONTROL + 'a')  # CTRL + a ：全选
        editor.send_keys(Keys.DELETE)  # 删除
        '''随机选择古诗文件夹'''
        random_folder = self.random_move_dir(self.image_folder,self.image_folder_used)
        files_list = os.listdir(random_folder)
        files_list.sort(key=lambda x: int(re.search("\d+", x).group()))
        print(files_list)
        self.poem_title = files_list[0].split('_')[0]# 取古诗名待用

        self.write_text(header)
        self.write_text(line)
        '''循环上传图片'''
        for i in files_list:
            self.upload_picture(os.path.join(random_folder,i))
            self.write_text(line)

        '''文章标题先输入'''
        title_input = self.driver.find_element(By.XPATH, ".//div[@class='article-bar__input-box']/input")
        title_input.clear()
        title_input.send_keys(self.poem_title)

        #self.publish_config()

    def publish_config(self):
            '''
            发布文章选择界面
            :return:
            '''
            publish = self.driver.find_element(By.XPATH, ".//button[@class='btn btn-publish']") #点击发送
            publish.click()
            time.sleep(1)  # 等待一秒
            try:# 文章质量不佳，发文助手会提示，再此点击发送发布文章即可
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='modal__content']")))
                print("发送助手又顽皮了")
            except:
                publish = self.driver.find_element(By.XPATH, ".//button[@class='btn btn-publish']")
                publish.click()
                time.sleep(1)  # 等待一秒

            '''封面摘要，上一个兄弟标签'''
            dan_tu = self.driver.find_element(By.XPATH, ".//span[contains(text(),'单图')]//preceding-sibling::span")
            ActionChains(self.driver).move_to_element(dan_tu).click().perform()
            time.sleep(1)  # 等待一秒

            '''摘要简介'''
            zhai_yao = self.driver.find_element(By.XPATH, ".//div[@class='d-flex cover-count-1']//textarea")
            zhai_yao.clear()
            zhai_yao.send_keys(self.poem_title)
            time.sleep(1)  # 等待一秒
            '''封面选择，xpath不容易定位，直接用了浏览器中copy 的xpath'''
            feng_mian = self.driver.find_element(By.XPATH, "./html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div/div/div[3]/div[1]")
            ActionChains(self.driver).move_to_element(feng_mian).click().perform()
            time.sleep(1)  # 等待一秒

            '''专栏选择，checkbox，选择的是input标签的父亲标签label'''
            zhuan_lan = self.driver.find_element(By.XPATH, ".//input[@value='诗词鉴赏']//..")
            #self.driver.execute_script('arguments[0].removeAttribute(\"style\")', zhuan_lan)
            ActionChains(self.driver).move_to_element(zhuan_lan).click().perform()
            time.sleep(1)  # 等待一秒

            '''文章类型选择'''
            artical_type = self.driver.find_element(By.XPATH, ".//label[@for='original']")
            ActionChains(self.driver).move_to_element(artical_type).click().perform()
            time.sleep(1)  # 等待一秒

            '''发布类型选择'''
            publish_type = self.driver.find_element(By.XPATH, ".//label[@for='public']")
            ActionChains(self.driver).move_to_element(publish_type).click().perform()
            time.sleep(1)  # 等待一秒

            '''内容等级选择'''
            content_level = self.driver.find_element(By.XPATH, ".//label[@for='public_1']")
            ActionChains(self.driver).move_to_element(content_level).click().perform()
            time.sleep(1)  # 等待一秒

            '''滚动滑轮下滑，发布文章按钮可能没加载出来'''
            pyautogui.scroll(-1000)  # 向下滚动鼠标
            time.sleep(1)  # 等待一秒

            '''保存'''
            #save = self.driver.find_element(By.XPATH, ".//button[contains(text(),'保存草稿')]")
            save = self.driver.find_element(By.XPATH, "./html/body/div[1]/div[2]/div/div[1]/div[2]/button[2]")
            ActionChains(self.driver).move_to_element(save).click().perform()
            time.sleep(3)  # 等待一秒
            '''取消'''
            quxiao = self.driver.find_element(By.XPATH, "./html/body/div[1]/div[2]/div/div[1]/div[2]/button[1]")
            ActionChains(self.driver).move_to_element(quxiao).click().perform()
            time.sleep(1)  # 等待一秒

            WebDriverWait(self.driver, 3).until_not(
                EC.visibility_of_element_located((By.XPATH, ".//h3[text()='发布文章']")))

            # '''发布'''
            # #save = self.driver.find_element(By.XPATH, ".//button[contains(text(),'保存草稿')]")
            # save = self.driver.find_element(By.XPATH, "./html/body/div[1]/div[2]/div/div[1]/div[2]/button[4]")
            # ActionChains(self.driver).move_to_element(save).click().perform()
            # time.sleep(1)  # 等待一秒
            # WebDriverWait(self.driver, 3).until_not(
            #     EC.visibility_of_element_located((By.XPATH, ".//h3[text()='发布文章']")))

            return None


    def upload_picture(self, file):
        '''
        向CSDN上传图片，单张
        :param file:
        :return:
        '''
        try:
            '''点击商团图片按钮'''
            add_photo = self.driver.find_element(By.XPATH, ".//div//button[@data-title='图片 – Ctrl+Shift+G']")
            add_photo.click()
            time.sleep(1)
            choose_photo = self.driver.find_element(By.XPATH, ".//div[@class='uploadPicture']/input")
            ActionChains(self.driver).move_to_element(choose_photo).click().perform()
            time.sleep(1)  # 等待一秒
            '''文件对话框选择文件'''
            up = UploadFilesSelenium()
            up.upload_file(file)
            try:
                WebDriverWait(self.driver, 10).until_not(
                    EC.visibility_of_element_located((By.XPATH, ".//div[@class='uploadPicture']/input")))
                time.sleep(3)  # 等待3秒
            except:
                print("图片上传失败{}".format(file))
                return None

            '''下拉滑条，js 无法生效不知为何，用pyautogui滚动鼠标'''
            # element = self.driver.find_element(By.XPATH, ".//div[@class='editor']//pare<br><hr style="height:2px;border:none;border-top:2px dashed #0066CC;"/><br><br><hr style="height:2px;border:none;border-top:2px dashed #0066CC;"/><br>nt::div[1]")
            # self.driver.execute_script("arguments[0].scrollTop=10000;", element)
            pyautogui.scroll(-1000)  # 向下滚动鼠标
            time.sleep(1)  # 等待一秒
            '''定位到最后一个div标签，解决无法连续上传问题'''
            last_item = self.driver.find_element(By.XPATH, ".//div[@class='editor']//pre//div[last()]")
            ActionChains(self.driver).move_to_element(last_item).click().perform()
            pyautogui.press('enter')
            time.sleep(1)  # 等待一秒
        except:
            print(traceback.print_exc())

    def write_text(self, text):
        '''
        向CSDN写入文本类型内容
        :param text:
        :return:
        '''
        try:
            pyperclip.copy(text)  # 把指定的路径拷贝到焦点
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            pyautogui.press('enter')
            time.sleep(1)  # 等待一秒
            '''下拉滑条，js 无法生效不知为何，用pyautogui滚动鼠标'''
            # element = self.driver.find_element(By.XPATH, ".//div[@class='editor']//parent::div[1]")
            # self.driver.execute_script("arguments[0].scrollTop=10000;", element)
            pyautogui.scroll(-1000)  # 向下滚动鼠标
            time.sleep(1)  # 等待一秒
            '''定位到最后一个div标签，解决无法连续上传问题'''
            last_item = self.driver.find_element(By.XPATH, ".//div[@class='editor']//pre//div[last()]")
            ActionChains(self.driver).move_to_element(last_item).click().perform()
            pyautogui.press('enter')
            time.sleep(1)  # 等待一秒
        except:
            print(traceback.print_exc())

if __name__ == '__main__':
    C = ScriptCsdn()
    C.init_chrome()
    # C.first_login( 20)
    # C.save_cookies()
    C.main()
    # C.random_move_dir(C.image_folder,C.image_folder_used)
