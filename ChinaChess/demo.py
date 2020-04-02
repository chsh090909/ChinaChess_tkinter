#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@file:  demo.py
@time:  2020/3/10 17:37
@title:
@content:
"""
from tkinter import *
import random
from ChinaChess.settings import Settings

all_pieces = {
    'box_0_0': {'box_key': 'red_zu4', 'state': True},
    'box_0_1': {'box_key': 'black_zu4', 'state': True},
    'box_0_2': {'box_key': 'red_ma1', 'state': True},
    'box_0_3': {'box_key': None, 'state': None},
    'box_1_0': {'box_key': 'black_ju2', 'state': True},
    'box_1_1': {'box_key': 'black_shi1', 'state': True},
    'box_1_2': {'box_key': None, 'state': None},
    'box_1_3': {'box_key': 'red_pao1', 'state': False}
}
def fn():
    true_count = 0
    none_count = 0
    for key, value in all_pieces.items():
        for key1, value1 in value.items():
            # print(f"key: {key}")
            # print(f"key1: value1 ==> {key1}: {value1}")
            if key1 == 'state':
                if value1 is True:
                    true_count += 1
                elif value1 is False:
                    return False
                elif value1 is None:
                    none_count += 1

    print(f"true_count: {true_count}")
    print(f"none_count: {none_count}")

fn()

