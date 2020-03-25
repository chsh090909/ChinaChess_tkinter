#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@file:  common.py
@time:  2020/3/23 15:30
@title:
@content: 提供公共方法
"""
import platform
from PIL import Image, ImageTk
from ChinaChess.customException import *

class Commmon():
    def __init__(self):
        pass

    # 获取当前系统的名称
    def get_system_name(self):
        system_flag = 0
        if platform.uname().system == 'Darwin' or platform.platform().split('-')[0] == 'Darwin':
            # mac系统加载mac配置，设置flag为1
            system_flag = 1
        elif platform.uname().system == 'Windows' or platform.platform().split('-')[0] == 'Windows':
            # windows系统加载默认setting设置，设置flag为2
            system_flag = 2
        return system_flag

    # 压缩图片，改变图片的大小
    def change_img(self, img, width=100, height=100):
        if isinstance(img, str):
            piece1 = Image.open(img)
            piece2 = piece1.resize((width, height))
            changed_img = ImageTk.PhotoImage(piece2)
            return changed_img
        elif isinstance(img, dict):
            img_dict = {}
            for key, value in img.items():
                piece1 = Image.open(value)
                piece2 = piece1.resize((width, height))
                changed_img = ImageTk.PhotoImage(piece2)
                img_dict[key] = changed_img
            return img_dict
        else:
            raise ImgNotFound('传入图片格式不正确或者图片不存在！')

    # 读取文件
    def read_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    common = Commmon()
    common.change_img(img=None)