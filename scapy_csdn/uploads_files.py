
import pyautogui
import pyperclip
import win32con
import win32gui
import time
import traceback
import os


class UploadFilesSelenium(object):
    def __int__(self):
        pass

    def upload_file(self, file_path):
        try:
            pyperclip.copy(file_path)  # 把指定的路径拷贝到焦点
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)  # 等待一秒
            pyautogui.press('enter')  # 进入到目标文件夹

        except:
            print(traceback.print_exc())

    def upload_files(self, file_dir, file_list):
        '''
        :param file_dir: 待上传的文件夹路径
        :param file_list: 待上传的文件列表（在 file_dir路径下）
        有个硬伤：输入的文件列表转换字符串之后总字节无法超过260
        :return:
        '''

        file_upload = ' '.join('"{0}"'.format(x) for x in file_list)
        if len(file_upload) >= 260:
            print("输入文件列表总字节{}大于260，无法上传！".format(len(file_upload)))
            file_upload = os.path.join(file_dir, file_list[0])
        try:
            pyperclip.copy(file_dir)  # 把指定的路径拷贝到焦点
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)  # 等待一秒
            pyautogui.press('enter')  # 进入到目标文件夹
            '''将文件列表转为字符串 ，上传文件'''
            pyperclip.copy(file_upload)  # 把指定的路径拷贝到焦点
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)  # 等待一秒
            pyautogui.press('enter')  # 进入到目标文件夹
        except:
            print(traceback.print_exc())

    def upload_file_all(self, dir):
        try:
            pyperclip.copy(dir)  # 把指定的路径拷贝到焦点
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)  # 等待一秒
            pyautogui.press('enter')  # 进入到目标文件夹
            '''根据文件资源管理器的名字定位'''
            handle = win32gui.FindWindow("#32770", "打开")
            '''文件资源管理器的位置'''
            left, top, right, bottom = win32gui.GetWindowRect(handle)
            '''将鼠标移动到文件资源管理器内部,大致是中间位置'''
            pyautogui.moveTo(right - 30 , bottom - 200, duration=0.25)
            pyautogui.click()  # 点击一下
            pyautogui.hotkey('ctrl', 'a')  # 全选
            button = win32gui.FindWindowEx(handle, 0, 'Button', "打开(&O)")
            win32gui.SendMessage(handle, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
        except:
            print(traceback.print_exc())