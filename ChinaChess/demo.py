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


begin = 0
end = 7
value_list = ['t','f','t','f','t','f','t','f']
t_index = 0
if begin > end:
    begin, end = end, begin
for i in range(begin+1, end):
    if value_list[i] == 't':
        t_index += 1
    if t_index > 1:
        break

print(f"t_index: {t_index}")
