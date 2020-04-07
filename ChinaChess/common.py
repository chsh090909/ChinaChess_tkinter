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
import sys
import time
import os
import threading
from PIL import Image, ImageTk
from ChinaChess.customException import *
from ChinaChess.loggerPrint import LoggerPrint
from ChinaChess.settings import Settings

class Commmon():
    def __init__(self, setting):
        self.setting = setting
        self.__logger = LoggerPrint(self.setting)
        self.log = self.__logger.printLogToSystem(False)

        self.times = 0
        self.color1, self.color2 = 'red', 'black'

    # 获取当前系统的名称
    def get_system_name(self):
        system_flag = 0
        if platform.uname().system == 'Darwin' or platform.platform().split('-')[0] == 'Darwin':
            # mac系统加载mac配置，设置flag为1
            system_flag = 1
        elif platform.uname().system == 'Windows' or platform.platform().split('-')[0] == 'Windows':
            # windows系统加载默认setting设置，设置flag为2
            system_flag = 2
        else:
            system_flag = 3
        self.log.info(f"当前系统为：{platform.uname().system}")
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
    def read_file(self, filename, flag=None):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                if flag is None:
                    return f.read()
                elif flag == 'info':
                    return f.readlines()
        except Exception as e:
            self.log.exception('读取文件异常！')

    # 写入info文件
    def write_file(self, filename, write_value):
        if isinstance(write_value, str):
            with open(filename, 'ab+') as f:
                writestr = (write_value + os.linesep).encode('utf-8')
                f.write(writestr)
        elif isinstance(write_value, list):
            with open(filename, 'w+', encoding='utf-8') as f:
                f.writelines(write_value)

    # 获取当前系统时间，格式化后添加到文件名称中
    def format_now_time(self):
        ntime = time.strftime('_%Y_%m_%d_%H_%M_%S')
        return ntime

    # 获取当前系统时间
    def get_now_time(self):
        ntime = time.strftime('%Y-%m-%d %H:%M:%S')
        return ntime

    # 计算两个时间之间的时间差，返回str
    def how_long_time(self, begintime, endtime):
        howlongdays = (endtime - begintime).days
        howlongsecs = (endtime - begintime).seconds
        hours = int(howlongsecs / 3600)
        mins = int((howlongsecs % 3600) / 60)
        secs = (howlongsecs % 3600) % 60
        how_long = ''
        if howlongdays != 0:
            howlongdays = '%s天' % (str(howlongdays))
            how_long += howlongdays
        if hours != 0:
            hours = '%s小时' % (str(hours))
            how_long += hours
        if mins != 0:
            mins = '%s分' % (str(mins))
            how_long += mins
        if secs != 0:
            secs = '%s秒' % (str(secs))
            how_long += secs
        return how_long

    # 改变字体颜色
    def change_font_color(self):
        if self.times <= 5:
            self.color1, self.color2 = self.color2, self.color1
            self.times += 1
            t = threading.Timer(1, self.change_font_color)
            t.start()
        print(f"第 {self.times} 次：color1, color2 = {self.color1}, {self.color2}")



if __name__ == '__main__':
    setting = Settings()
    common = Commmon(setting)
    common.change_font_color()