#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@file:  demo.py
@time:  2020/3/10 17:37
@title:

@content:
"""
# import random
# import time
# from functools import reduce
# from tkinter import *

def multipliers():
    return [lambda x:i*x for i in range(4)]
print([m(2) for m in multipliers()])


def f(x):
    list_f = []
    for i in range(4):
        list_f.append(i*x)
    return list_f

list_a = []
for m in f(2):
    list_a.append(m)
print(list_a)