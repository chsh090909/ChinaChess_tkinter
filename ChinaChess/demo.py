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

setting = Settings()

root = Tk()
root.title('五子棋')
root.geometry(f"{setting.screen_width}x{setting.screen_height}")
root.resizable(width=False, height=False)

cv = Canvas(root, background='white')
cv.pack(fill=BOTH, expand=YES)

board_img = PhotoImage(file=setting.chess_board)
cv.create_image(setting.chess_board_localx, setting.chess_board_localy, image=board_img)



for i in range(8):
    for j in range(4):
        pass


root.mainloop()