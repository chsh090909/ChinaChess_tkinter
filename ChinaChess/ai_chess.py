#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@file:  ai_chess.py
@time:  2020/5/25 15:03
@title:
@content:
"""
class Ai_chess():
    def __init__(self):
        # 初始化棋子的自身价值
        self.ai_jiang = 100
        self.ai_shi = 90
        self.ai_xiang = 80
        self.ai_ma = 70
        self.ai_ju = 60
        self.ai_pao = 80
        self.ai_zu = 70
        # 棋子所在位置的价值:数字表示棋子可移动的位置数
        self.ai_4 = 40
        self.ai_3 = 30
        self.ai_2 = 20
        self.ai_1 = 10
        self.ai_0 = 0
        #


