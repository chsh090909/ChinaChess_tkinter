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
from ChinaChess.loggerPrint import LoggerPrint

class GameFunction():
    """
    游戏逻辑的所有方法，不涉及到界面显示内容
    """
    def __init__(self, setting):
        self.setting = setting
        self.logger = LoggerPrint(self.setting).printLogToSystem(False)

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
                all_pieces[f"box_{i}_{j}"] = {'box_key': random_key, 'state': False}
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

    # 两个棋子之间的比较
    def piece_VS_piece(self, box1_xy, box2_xy, box1_name, box2_name, all_pieces):
        """
        :param box1_xy: box_2_3
        :param box2_xy: box_3_3
        :param box1_name: red_shi1
        :param box2_name: None
        :return:
        """
        value_list = self.setting.pieces_list
        box1_x = int(box1_xy.split('_')[1])
        box1_y = int(box1_xy.split('_')[2])
        box2_x = int(box2_xy.split('_')[1])
        box2_y = int(box2_xy.split('_')[2])
        box1_color = box1_name.split('_')[0]
        box1_value = box1_name.split('_')[1]
        box1_value_1 = box1_value[:-1] if box1_value[-1:].isnumeric() else box1_value
        box1_value_index = value_list.index(box1_value_1)
        # 如果box1的位置比box2的位置大，则交换他们的值
        if box1_y > box2_y:
            box1_y, box2_y = box2_y, box1_y
        if box1_x > box2_x:
            box1_x, box2_x = box2_x, box1_x
        # box2如果为空，则认为第二次选择了棋盘空格，不为空则需要取box2的值与box1比较
        if box2_name is not None:
            box2_color = box2_name.split('_')[0]
            box2_value = box2_name.split('_')[1]
            box2_value_1 = box2_value[:-1] if box2_value[-1:].isnumeric() else box2_value
            box2_value_index = value_list.index(box2_value_1)
        else:
            return self.__other_vs_piece(box1_x, box1_y, box2_x, box2_y, piece_equal=False)
        # 如果两个棋子相同，返回both
        if box1_value_index == box2_value_index:
            if box1_value_1 == 'pao':
                # '炮'相同时的吃法：
                # 中间有且只有一个棋子，中间棋子不论打没打开都可以，没有距离限制，最后两个棋子同时失去
                return self.__pao_vs_piece(box1_x, box1_y, box2_x, box2_y, all_pieces, piece_equal=True)
            else:
                # 其他相同棋子的吃法：
                # 只能相邻位置两个棋子，最后也是两个棋子同时失去
                return self.__other_vs_piece(box1_x, box1_y, box2_x, box2_y, piece_equal=True)
        # 如果两个棋子不相同
        else:
            if box1_value_1 == 'pao':
                # '炮'的吃法：
                # 1、中间必须有且只有一个棋子，才能吃到对方棋子，没有距离限制；
                # 2、炮没有大小吃法限制，上到将，下到卒都可以吃；
                # 3、炮移动只能相邻的格子移动，不能跳着移动；
                return self.__pao_vs_piece(box1_x, box1_y, box2_x, box2_y, all_pieces, piece_equal=False)
            else:
                # 其他的棋子的吃法：
                # 1、大吃小（将（帅）>士>（象）相>马>车>炮和卒（兵）），两两相同则一起吃掉；
                # 2、炮和卒（兵）、炮和将（帅）相互不能吃，任何棋子都可以吃炮，除了卒（兵）、将（帅）外；
                # 3、任何棋子都可以吃卒（兵），而卒（兵）只吃对方的帅（将）；
                # 4、棋子只能相邻的吃，而且一次只能走一步，吃一个棋子，炮除外
                if box1_value_index < box2_value_index:
                    # 大吃小，除非jiang和zu或pao同时出现
                    if box1_value_1 == 'jiang' and (box2_value_1 in ['zu', 'pao']):
                        self.logger.info("false原因：jiang在和zu或者pao比较")
                        return 'false'
                    else:
                        return self.__other_vs_piece(box1_x, box1_y, box2_x, box2_y, piece_equal=False)
                else:
                    # 最后一种情况：zu只能吃jiang
                    if box1_value_1 == 'zu' and box2_value_1 == 'jiang':
                        return self.__other_vs_piece(box1_x, box1_y, box2_x, box2_y, piece_equal=False)
                    else:
                        self.logger.info("false原因：box1比box2还小")
                        return 'false'

    # pao的比较
    def __pao_vs_piece(self, box1_x, box1_y, box2_x, box2_y, all_pieces, piece_equal=True):
        if box1_x == box2_x and box2_y - box1_y > 1:
            between_state_have = 0
            for i in range(box1_y + 1, box2_y):
                if all_pieces[f"box_{box1_x}_{i}"]['state'] is not None:
                    between_state_have += 1
                if between_state_have > 1:
                    break
            if between_state_have == 1:
                if piece_equal is True:
                    self.logger.info("both：box1和box2相同")
                    return 'both'
                else:
                    return 'true'
            else:
                self.logger.info("false原因：box1和box2之间，在y轴上没有棋子，或者有大于2个的棋子")
                return 'false'
        elif box1_y == box2_y and box2_x - box1_x > 1:
            between_state_have = 0
            for i in range(box1_x + 1, box2_x):
                if all_pieces[f"box_{i}_{box1_y}"]['state'] is not None:
                    between_state_have += 1
                if between_state_have > 1:
                    break
            if between_state_have == 1:
                if piece_equal is True:
                    self.logger.info("both：box1和box2相同")
                    return 'both'
                else:
                    return 'true'
            else:
                self.logger.info("false原因：box1和box2之间，在x轴上没有棋子，或者有大于2个的棋子")
                return 'false'
        else:
            self.logger.info("false原因：box1和box2不在同一条x轴或y轴上")
            return 'false'

    # 其他棋子的比较
    def __other_vs_piece(self, box1_x, box1_y, box2_x, box2_y, piece_equal=True):
        if (box1_x == box2_x and box2_y - box1_y == 1) or (box1_y == box2_y and box2_x - box1_x == 1):
            if piece_equal is True:
                self.logger.info("both：box1和box2相同")
                return 'both'
            else:
                return 'true'
        else:
            self.logger.info("false原因：box1和box2不在同一条x轴或y轴上")
            return 'false'

    # 游戏结束判断
    def is_game_over(self, all_pieces):
        # 总走棋步数必须大于48步
        pass


if __name__ == '__main__':
    from ChinaChess.settings import Settings
    setting = Settings()
    gf = GameFunction(setting)

    pieces = gf.box_pieces()
    print(pieces)
