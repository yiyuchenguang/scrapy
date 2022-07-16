'''
@随机移动某个文件夹的一个文件到另一个文件夹下
@随机移动移动一个文件夹下的子文件夹到另一个文件夹下
@python 3.8
'''

import os
import random
import shutil
import traceback


def random_move_file(source_dir, target_dir):
    '''
    :param source_dir: 待移动文件的文件夹路径
    :param target_dir: 将要移动到的文件夹路径
    :return:
    '''
    try:
        # out_image文件夹下的所有诗词文件夹
        all_files = os.listdir(source_dir)
        if not all_files:
            print("文件夹下没有文件")
            return None

        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
            print("新建文件夹{}".format(target_dir))

        # 随机选取一个
        sample = random.sample(all_files, 1)[0]
        print(sample)
        source_dir = os.path.join(source_dir, sample)
        shutil.move(source_dir, target_dir)
    except:
        print(traceback.print_exc())

def random_move_dir(source_dir, target_dir):
    try:
        '''获取当前文件夹下的所有子文件夹名称'''
        images_dirs = []
        for root, dirs, files in os.walk(source_dir):
            for sub in dirs:
                images_dirs.append(sub)

        sample = random.sample(images_dirs, 1)[0]
        print(sample)
        source_sub_dir = os.path.join(source_dir, sample)
        # target_sub_dir = os.path.join(target_dir, sample)
        # if os.path.exists(target_sub_dir):
        #     shutil.rmtree(target_sub_dir, ignore_errors=True)
        '''copy后删除源子文件夹'''
        shutil.copytree(source_sub_dir, target_dir)
        shutil.rmtree(source_sub_dir, ignore_errors=True)
    except:
        print(traceback.print_exc())

if __name__ == '__main__':
    source_dir = r"/image_all/out_image_used/金陵图"
    target_dir = r"/image_all/out_image_used/金陵图_moved"
    random_move_file(source_dir, target_dir)

    source_dir = r"/image_all/out_image"
    target_dir = r"/image_all/out_image_used"
    random_move_file(source_dir, target_dir)

