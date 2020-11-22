#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@file:  scores.py
@time:  2020/6/15 17:33
@title:
@content: 各棋子的价值以及棋子位置的价值得分
"""
class Scores():
    '''
    得分规则：
        1、吃棋得分为十万位分数；
        2、棋子自身价值为万位分数；
        3、移动棋子到有利位置根据可吃棋子数量得分为千位分数；
        4、打开特殊棋子位置得分为百位分数；
        5、打开一个棋子得分为十位分数；
        6、替换位得分为个位得分，是棋子自身价值得分/10000而来，便于区分打开棋子或移动棋子的不同得分来判断棋子的优先级；
    '''
    @staticmethod
    def piece_score(piece_name):
        # 棋子的自身价值得分为万位分数
        piece_score_dict = {
            'jiang': 90000,
            'shi': 80000,
            'xiang': 70000,
            'ma': 40000,
            'ju': 30000,
            'pao': 60000,
            'zu': 50000,
            'zu_no_jiang': 20000,
        }
        return piece_score_dict[piece_name]

    @staticmethod
    def eat_score(key):
        # 吃棋得分为十万位分数
        eat_score_dict = {
            'jiang_jiang': 100000,
            'zu_jiang': 900000,
            'pao_jiang': 900000,
            'shi_shi': 100000,
            'jiang_shi': 800000,
            'pao_shi': 800000,
            'xiang_xiang': 100000,
            'jiang_xiang': 700000,
            'shi_xiang': 700000,
            'pao_xiang': 700000,
            'ma_ma': 100000,
            'jiang_ma': 400000,
            'shi_ma': 400000,
            'xiang_ma': 400000,
            'pao_ma': 400000,
            'ju_ju': 100000,
            'jiang_ju': 300000,
            'shi_ju': 300000,
            'xiang_ju': 300000,
            'ma_ju': 300000,
            'pao_ju': 300000,
            'pao_pao': 100000,
            'shi_pao': 600000,
            'xiang_pao': 600000,
            'ma_pao': 600000,
            'ju_pao': 600000,
            'zu_zu': 100000,
            'shi_zu': 500000,
            'xiang_zu': 500000,
            'ma_zu': 500000,
            'ju_zu': 500000,
            'pao_zu': 500000,
            'zu_zu_no_jiang': 100000,
            'shi_zu_no_jiang': 200000,
            'xiang_zu_no_jiang': 200000,
            'ma_zu_no_jiang': 200000,
            'ju_zu_no_jiang': 200000,
            'pao_zu_no_jiang': 200000,
        }
        return eat_score_dict[key]

    @staticmethod
    def other_pieces_score(key):
        # 棋盘特殊棋子位置得分十位分数
        other_score_dict = {
            'zu_ju': 20,
            'zu_pao': 40,
            'pao_jiang': 50,
            'pao_ju': 30
        }
        return other_score_dict[key]

