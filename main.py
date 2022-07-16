#-*- coding:utf-8 -*-
import os, random, shutil
import json
import math
import traceback
from PIL import Image, ImageDraw, ImageFont

class CompositePicture():
    def __init__(self, poem_json, fileDir,tarDir,poem_img_folder):
        self.font_type = "C:\\WINDOWS\\Fonts\\simhei.ttf" # 仿宋： simfang.TTF  ；黑体加粗：simhei.ttf
        self.drop_image_Dir = './drop_image/'  # diu
        self.poem_json = poem_json  # 源图片文件夹路径
        self.fileDir = fileDir  # 源图片文件夹路径
        self.tarDir = tarDir  # 移动到新的文件夹路径
        self.poem_img_folder = poem_img_folder
        self.mkdir(self.tarDir)
        self.mkdir(self.poem_img_folder)


    def validateTitle(self,title):
        import re
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def mkdir(self,path):
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False

    def moveFile(self, sourceFile, targetFile):
        i = 0
        while (True):
            i = i+1
            pathDir = os.listdir(sourceFile)  # 取图片的原始路径
            # print(pathDir)
            filenumber = len(pathDir)
            if(filenumber == 0):
                print("没有更多图片了！")
                exit(1)

            rate = 0.01  # 自定义抽取图片的比例，比方说100张抽10张，那就是0.1
            # picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片
            try:
                sample = random.sample(pathDir, 1)[0]  # 随机选取picknumber数量的样本图片
                # print(sample)
                # print(sourceFile)
                # print(targetFile)
                sourceFile = os.path.join(sourceFile, sample)
                targetFile = os.path.join(targetFile, sample)
                shutil.move(sourceFile, targetFile)
                return targetFile
            except:
                print(traceback.print_exc())
                print("文件中找不到可用的图片_%d"%i)
            if i > 10:
                print("连续10次找不到合适的图片！ ")
                return None

    def load(self):
        with open(self.poem_json ,'r',encoding='utf-8') as f:
            data = json.load(f)
            return data

    def getRandomInfo(self,data):
        try:
            temp = random.randrange(0,len(data))
            choice2 = data.pop(temp)
            return choice2
        except:
            return None

    def new_image(self,path,back_color):
        img = Image.open(path)
        img = img.resize((900, 500), Image.ANTIALIAS)
        self.W = img.size[0]
        self.H = img.size[1]
        self.new_img = Image.new('RGB', (self.W, self.H*2), back_color)  # 新建一张2倍高度的 白色底片的 图片 ,默认1200pxi
        self.new_img.paste(img, (0, 0))  # 从犯（0，0）处开始拷贝小图片到大图片
        self.draw = ImageDraw.Draw(self.new_img)  # 得到画笔

    def draw_image(self, font_size, fillColor, spaceSize, text, offset):
        setFont = ImageFont.truetype(self.font_type, font_size)  # 设置字体以及字体大小
        for i in range(len(text)):
            w = len(text[i]) * font_size
            self.draw.text(((self.W-w)/2,  offset + i*(font_size + spaceSize)), text[i], font=setFont,fill = fillColor)  # 利用ImageDraw的内置函数，在图片上写入文字

    def outPutStrLength(self,tempStr,row_length):
        startpoint = 0
        retValue =[]
        tempStr = tempStr.replace('\n', '') # 替换掉字符串中换行符
        seg = math.ceil(len(tempStr)/row_length) # 每行输出row_length 个向上取整有seg行，
        for i in range(seg):
            startpoint = row_length * i  #每行的索引点
            retValue.append(tempStr[startpoint : startpoint + row_length])
            # retValue =  retValue + tempStr[startpoint : startpoint + row_length] + '\n'
            # print(tempStr[startpoint : startpoint + row_length]) # 索引字符串
        return retValue

if __name__ == '__main__':
    image_folder = r"D:\Document\source\picture"
    image_out_folder = r"D:\Document\source\picture_target"
    poem_created_folder = r"D:\Document\source\poem_created"
    poem_folder = r"D:\Document\source\poem\songcijianhgxuan.json"

    C = CompositePicture(poem_folder, image_folder, image_out_folder,poem_created_folder)  # 唐诗
    data = C.load()

    while True:
        index = 0
        random_value = C.getRandomInfo(data)
        if(not random_value):
            print("没有更多的诗词了。")
            break
        print(random_value)
        new_title = C.validateTitle(random_value['poem_title'])
        new_folder = os.path.join(C.poem_img_folder,new_title)
        flag = C.mkdir(new_folder)
        if(not flag):
            continue

        # 诗词内容 ,
        s_num = 9
        font_size = 28
        spaceSize = 10
        row_cut = 16
        retValue = C.outPutStrLength(random_value['poem_body'], row_cut)  # 宋词
        # retValue = random_value['poem_body'].split('\n')  # 唐诗

        seg = math.ceil(len(retValue) / s_num)  # 每行输出row_length 个向上取整有seg行，
        for i in range(seg):
            index = index + 1
            pic_path = C.moveFile(C.fileDir, C.tarDir)
            temp_img = pic_path.split('/')[-1].split('.')[
                0]  # eg: input"./keep_image/4-1Z916153311.jpg" , output 4-1Z916153311
            C.new_image(pic_path, '#EEE5E5')
            if (i == 0):
                setFont = ImageFont.truetype(C.font_type, font_size - 10)  # 写入诗词类型
                C.draw.text((100, C.H * 2 - 70), random_value['poem_type'], font=setFont,
                            fill="#239589")  # 利用ImageDraw的内置函数，在图片上写入文字
                poem_title = C.outPutStrLength(random_value['poem_title'], row_cut)  # 写入诗词标题
                C.draw_image(font_size=font_size + 8, fillColor="#D226DB", spaceSize=spaceSize, text=poem_title,
                             offset=C.H + 20)
                poem_author = C.outPutStrLength(random_value['poem_author'], row_cut)  # 写入诗词作者
                C.draw_image(font_size=font_size - 10, fillColor="#3000f7", spaceSize=spaceSize, text=poem_author,
                             offset=C.H + 65)
            startpoint = s_num * i  # 每行的索引点
            C.draw_image(font_size=font_size, fillColor="#239589", spaceSize=spaceSize, text=str(index),
                         offset=C.H * 2 - 30)  # 写入页脚
            C.draw_image(font_size=font_size, fillColor="#D226DB", spaceSize=spaceSize,
                         text=retValue[startpoint:startpoint + s_num], offset=C.H + 100)  # 46:30
            #C.new_img.show()
            img_name = os.path.join(new_folder, "%s_%s_%d.jpeg" % (new_title, "诗词", index))
            C.new_img.save(img_name, "jpeg")
            print("图片保存成功 ： %s" % img_name)

        # 诗词注释
        text_num_row = 30
        s_num = 11
        font_size = 24
        spaceSize = 10
        retValue = C.outPutStrLength(random_value['poem_yi'], text_num_row)
        seg = math.ceil(len(retValue) / s_num)  # 每行输出row_length 个向上取整有seg行，
        for i in range(seg):
            index = index + 1
            pic_path = C.moveFile(C.fileDir, C.tarDir)
            temp_img = pic_path.split('/')[-1].split('.')[
                0]  # eg: input"./keep_image/4-1Z916153311.jpg" , output 4-1Z916153311
            C.new_image(pic_path, '#def7e7')
            startpoint = s_num * i  # 每行的索引点
            if i == 0:
                C.draw_image(font_size=font_size + 8, fillColor="#D226DB", spaceSize=spaceSize, text=["注释:"],
                             offset=C.H + 20)
            C.draw_image(font_size=font_size, fillColor="#239589", spaceSize=spaceSize, text=str(index),
                         offset=C.H * 2 - 30)
            C.draw_image(font_size=font_size, fillColor="#D226DB", spaceSize=spaceSize,
                         text=retValue[startpoint:startpoint + s_num], offset=C.H + 80)  # 46:30
            #C.new_img.show()
            img_name = os.path.join(new_folder, "%s_%s_%d.jpeg" % (new_title, "注释", index))
            C.new_img.save(img_name, "jpeg")
            print("图片保存成功 ： %s" % img_name)

        # 诗词赏析
        retValue = C.outPutStrLength(random_value['poem_shang'], text_num_row)
        seg = math.ceil(len(retValue) / s_num)  # 每行输出row_length 个向上取整有seg行，
        for i in range(seg):
            index = index + 1
            pic_path = C.moveFile(C.fileDir, C.tarDir)
            temp_img = pic_path.split('/')[-1].split('.')[
                0]  # eg: input"./keep_image/4-1Z916153311.jpg" , output 4-1Z916153311
            C.new_image(pic_path, '#eee4e1')
            startpoint = s_num * i  # 每行的索引点
            if i == 0:
                C.draw_image(font_size=font_size + 8, fillColor="#3000f7", spaceSize=spaceSize, text=["赏析:"],
                             offset=C.H + 20)  # 标题
            C.draw_image(font_size=font_size, fillColor="#239589", spaceSize=spaceSize, text=str(index),
                         offset=C.H * 2 - 30)  # 页脚
            C.draw_image(font_size=font_size, fillColor="#3000f7", spaceSize=spaceSize,
                         text=retValue[startpoint:startpoint + s_num], offset=C.H + 80)  # 内容
            #C.new_img.show()
            img_name = os.path.join(new_folder, "%s_%s_%d.jpeg" % (new_title, "赏析", index))
            C.new_img.save(img_name, "jpeg")
            print("图片保存成功 ： %s" % img_name)
        #break







