#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@file:  gameFunction.py
@time:  2020/3/18 20:05
@title:
@content:
"""
import random

class GameFunction():
    """
    游戏逻辑的所有方法，不涉及到界面显示内容
    """
    def __init__(self, setting):
        self.setting = setting

    # 将红黑棋子对应的图片，关联起来，存放在字典中
    def __get_all_pieces(self, piece_flag):
        pieces = []
        for piece in self.setting.pieces_list:
            # value = f"{self.setting.pieces_front}{piece_flag}_{piece}{self.setting.pieces_noun}"
            if piece in ['shi', 'xiang', 'ma', 'ju', 'pao']:
                for i in range(1, 3):
                    pieces.append(f"{piece_flag}_{piece}{str(i)}")
            elif piece == 'zu':
                for i in range(1, 6):
                    pieces.append(f"{piece_flag}_{piece}{str(i)}")
            else:
                pieces.append(f"{piece_flag}_{piece}")
        return pieces

    # 初始化棋子配置
    def box_pieces(self):
        # 获得所有的红黑棋子的dict
        pieces = self.__get_all_pieces('red')
        pieces_black = self.__get_all_pieces('black')
        pieces += pieces_black
        # 取得所有棋子dict的key
        # pieces_key_list = list(pieces.keys())
        all_pieces = {}
        for i in range(8):
            for j in range(4):
                # 随机抽取key放入boxid中，并初始化box的状态为False
                random_key = random.choice(pieces)
                all_pieces[f"box_{str(i)}{str(j)}"] = {'box_key': random_key, 'state': False}
                pieces.remove(random_key)
        return all_pieces

    # 获取鼠标位置所对应的方格坐标
    def get_box_xy(self, event_x, event_y):
        # 确定鼠标的有效矩形位置
        min_area_x = self.setting.piece_first_x
        min_area_y = self.setting.piece_first_y
        max_area_x = min_area_x + 8 * self.setting.piece_size
        max_area_y = min_area_y + 4 * self.setting.piece_size
        # 确认鼠标是在棋盘上有效的矩形范围之内
        if (min_area_x < event_x < max_area_x) and (min_area_x < event_y < max_area_y):
            mouse_x_not = (i * 100 + min_area_x for i in range(1, 9))
            mouse_y_not = (i * 100 + min_area_y for i in range(1, 5))
            # 鼠标不能在棋盘线上
            if (event_x not in mouse_x_not) and (event_y not in mouse_y_not):
                # 计算当前鼠标坐标所在的方格坐标
                box_x = int((event_x - min_area_x) / 100)
                box_y = int((event_y - min_area_y) / 100)
                return (box_x, box_y)

    # 加载棋子对应的图片
    def get_piece_image(self):
        pieces_dict = {}
        for piece_name in self.setting.pieces_list:
            pieces_dict[f"red_{piece_name}"] = f"{self.setting.pieces_front}red_{piece_name}{self.setting.pieces_noun}"
            pieces_dict[f"black_{piece_name}"] = f"{self.setting.pieces_front}black_{piece_name}{self.setting.pieces_noun}"
        return pieces_dict

if __name__ == '__main__':
    from ChinaChess.settings import Settings
    setting = Settings()
    gf = GameFunction(setting)

    pieces = gf.box_pieces()
    print(pieces)
