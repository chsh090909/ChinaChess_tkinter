#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@file:  chess.py
@time:  2020/3/8 16:37
@title:
@content:
"""
import os
import threading
from tkinter import *
from tkinter import dialog
from ChinaChess.settings import Settings
from ChinaChess.gameFunction import GameFunction
from ChinaChess.customDialog import MyDialog
from ChinaChess.playMusic import PlayMusic
from ChinaChess.common import Commmon
from ChinaChess.loggerPrint import LoggerPrint

# 导入settings配置文件
setting = Settings()
# 加载公共模块方法
common = Commmon()
# 加载日志功能
logger = LoggerPrint(setting)
log = logger.printLogToSystem(is_out_file=False)
# 加载游戏逻辑方法
game = GameFunction(setting)
# 加载音乐播放模块
play_music = PlayMusic()
# 初始化所有棋子
all_pieces = game.box_pieces()
log.info(f"all_pieces: {all_pieces}")

class Chess():
    def __init__(self, master):
        self.master = master
        #
        self.is_first_selected = True
        self.first_selected_img = None
        self.first_selected_value = None
        self.second_selected_img = None
        self.second_selected_value = None
        self.box_open_dict = {}
        #
        self.player1 = setting.player1_name
        self.player2 = setting.player2_name
        self.nowPlayer = self.player1
        self.player1Color = None
        self.player2Color = None
        self.totalCount = 0
        self.wonCount = 0
        self.tieCount = 0
        self.numCount = 0
        # 获取系统信息，mac系统flag=1，windows系统flag=2
        self.system_flag = common.get_system_name()
        # 加载目录菜单
        self.init_menu()
        # 加载窗体内容
        self.init_widgets()

    # 初始化菜单栏
    def init_menu(self):
        menubar = Menu(self.master)
        # 添加菜单条
        self.master['menu'] = menubar
        # 创建顶级菜单
        server_menu = Menu(menubar, tearoff=0)
        operation_menu = Menu(menubar, tearoff=0)
        help_menu = Menu(menubar, tearoff=0)
        # 添加顶级菜单
        menubar.add_cascade(label='服务器', menu=server_menu)
        menubar.add_cascade(label='操作', menu=operation_menu)
        menubar.add_cascade(label='帮助', menu=help_menu)
        # 为server_menu添加菜单项
        server_menu.add_command(label='新建', command=None, compound=LEFT)
        server_menu.add_command(label='打开', command=None, compound=LEFT)
        # 此处要判断一下操作系统类型：mac系统自带菜单退出系统功能，windows系统则需要添加
        if self.system_flag == 2:
            # 添加菜单分割条
            server_menu.add_separator()
            # 为windows系统添加退出游戏菜单
            server_menu.add_command(label='退出游戏', command=self.close_window, compound=LEFT)
        # 为operation_menu添加菜单项
        operation_menu.add_command(label='悔棋', command=None, compound=LEFT)
        # 加分割条
        operation_menu.add_separator()
        # 为背景音乐子菜单创建目录
        operation_menu.add_command(label='关闭背景音乐', command=play_music.stop_bg_music, compound=LEFT)
        operation_menu.add_command(label='音乐音效全关', command=None, compound=LEFT)
        bg_music_menu = Menu(operation_menu, tearoff=0)
        operation_menu.add_cascade(label='切换背景音乐', menu=bg_music_menu)
        # 加载背景音乐列表
        bg_music_menu.add_radiobutton(label='随机下一首', command=play_music.play_bg_music, compound=LEFT)
        self.bg_music_var = IntVar()
        for i, music_list in enumerate(setting.music_list):
            bg_music_menu.add_radiobutton(label=music_list, command=self.change_bg_music, variable=self.bg_music_var, value=i)
        # 为help_menu添加菜单项
        help_menu.add_command(label='如何玩?', command=self.how_play, compound=LEFT)
        help_menu.add_command(label='关于...', command=self.about_dialog, compound=LEFT)

    # 为关于菜单，打开自定义对话框展示版本信息等
    def about_dialog(self):
        MyDialog(self.master, title='关于游戏', img=red_jiang_img)

    # 为如何玩菜单，打开pdf文件
    def how_play(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        help_file_path = base_dir + setting.help_file
        # mac系统
        if self.system_flag == 1:
            os.system(f'open {help_file_path}')
        # windows系统
        elif self.system_flag == 2:
            os.system('chcp 65001')
            full_path = '"' + help_file_path + '"'
            os.system('"' + full_path + '"')

    # 为子菜单背景音乐菜单，切换背景音乐功能
    def change_bg_music(self):
        music_id = self.bg_music_var.get()
        music_list = setting.music_list
        play_music.play_bg_music(music_file=music_list[music_id])

    # 初始化窗体内容
    def init_widgets(self):
        # 设置画布
        self.cv = Canvas(self.master, bg=setting.bg_color)
        self.cv.pack(fill=BOTH, expand=YES)
        # 使画布得到焦点
        self.cv.focus_set()
        # 加载棋盘图片
        self.load_chess_board()
        # 加载棋子背面图片
        self.box_back_dict = self.load_pieces_back()
        # 加载玩家信息内容
        self.load_player_info()
        # 加载鼠标悬停棋子的选中效果
        self.piece_selected = self.load_piece_selected()
        # cv绑定鼠标事件
        self.cv.bind('<Motion>', self.move_handler)
        self.cv.bind('<Button-1>', self.click_handler)

    # 加载棋盘图片
    def load_chess_board(self):
        self.cv.create_image(setting.chess_board_localx, setting.chess_board_localy, image=board_img, anchor=NW)

    # 加载棋子背面，循环加载
    def load_pieces_back(self):
        box_back_dict = {}
        for i in range(8):
            for j in range(4):
                piece_local_x = setting.piece_first_x + i * setting.piece_size
                piece_local_y = setting.piece_first_y + j * setting.piece_size
                back_img = self.cv.create_image(piece_local_x, piece_local_y, image=pieces_back_img, anchor=NW)
                box_back_dict[f"box_{i}_{j}"] = back_img
        return box_back_dict

    # 加载选中棋子的图片
    def load_piece_selected(self):
        piece_selected = self.cv.create_image(-100, -100, image=piece_selected_img)
        return piece_selected

    # 加载玩家信息部分的内容
    def load_player_info(self):
        self.cv.create_rectangle(0, 495, 1030, 500, fill='red', outline='red')
        self.cv.create_rectangle(513, 495, 517, 680, fill='red', outline='red')
        #
        player_name_font = (setting.font_style, setting.font_player_size)
        player_info_font = (setting.font_style, setting.font_info_size)
        # 玩家一
        self.player1_name = self.cv.create_text(105, 548, text=self.player1, font=player_name_font, anchor=CENTER, activefill='red')
        self.player1_img = self.cv.create_image(100, 620, image=None)
        self.player1_state = self.cv.create_text(220, 517, text=f'状态：正在走棋。。。', font=player_info_font, anchor=NW)
        self.player1_color = self.cv.create_text(220, 552, text=f'执方：', font=player_info_font, anchor=NW)
        self.player1_won = self.cv.create_text(220, 587, text=f'胜利：0 局', font=player_info_font, anchor=NW)
        self.player1_tie = self.cv.create_text(220, 622, text=f'打平：0 局', font=player_info_font, anchor=NW)
        # 玩家二
        self.player2_name = self.cv.create_text(618, 548, text=self.player2, font=player_name_font, anchor=CENTER, activefill='red')
        self.player2_img = self.cv.create_image(615, 620, image=None)
        self.player2_state = self.cv.create_text(735, 517, text=f'状态：走棋完毕！', font=player_info_font, anchor=NW)
        self.player2_color = self.cv.create_text(735, 552, text=f'执方：', font=player_info_font, anchor=NW)
        self.player2_won = self.cv.create_text(735, 587, text=f'胜利：0 局', font=player_info_font, anchor=NW)
        self.player2_tie = self.cv.create_text(735, 622, text=f'打平：0 局', font=player_info_font, anchor=NW)

    # 更新player_info
    def upd_player_info(self, box_key):
        self.numCount += 1
        if self.numCount == 1:
            self.player1Color = box_key.split('_')[0]
            if self.player1Color == 'red':
                self.cv.itemconfig(self.player1_img, image=red_jiang_img)
                self.cv.itemconfig(self.player2_img, image=black_jiang_img)
                self.cv.itemconfig(self.player1_color, text=f'执方：红方')
                self.cv.itemconfig(self.player2_color, text=f'执方：黑方')
                self.player2Color = 'black'
            else:
                self.cv.itemconfig(self.player1_img, image=black_jiang_img)
                self.cv.itemconfig(self.player2_img, image=red_jiang_img)
                self.cv.itemconfig(self.player1_color, text=f'执方：黑方')
                self.cv.itemconfig(self.player2_color, text=f'执方：红方')
                self.player2Color = 'red'
        self.nowPlayer = self.player2 if self.nowPlayer == self.player1 else self.player1
        #
        if self.numCount % 2 == 1:
            self.cv.itemconfig(self.player1_state, text=f'状态：走棋完毕！')
            self.cv.itemconfig(self.player2_state, text=f'状态：正在走棋。。。')
        else:
            self.cv.itemconfig(self.player1_state, text=f'状态：正在走棋。。。')
            self.cv.itemconfig(self.player2_state, text=f'状态：走棋完毕！')

    # 鼠标移动事件：获取鼠标坐标，画一个高亮的圆，表示当前鼠标在这个棋子上
    def move_handler(self, event):
        if game.get_box_xy(event.x, event.y):
            box_x, box_y = game.get_box_xy(event.x, event.y)
            box_center_x = box_x * setting.piece_size + setting.piece_first_x + setting.piece_size / 2
            box_center_y = box_y * setting.piece_size + setting.piece_first_y + setting.piece_size / 2
            if all_pieces[f"box_{box_x}_{box_y}"]['state'] is not None:
                # 将create_image之后选中的图片，叠加到鼠标对应的棋子上
                self.cv.coords(self.piece_selected, box_center_x, box_center_y)

    # 鼠标单击事件：
    def click_handler(self, event):
        if game.get_box_xy(event.x, event.y):
            box_x, box_y = game.get_box_xy(event.x, event.y)
            #
            box_xy = f'box_{str(box_x)}_{str(box_y)}'
            box_piece = all_pieces[box_xy]
            piece_state = box_piece['state']
            #
            box_local_x = box_x * setting.piece_size + setting.piece_first_x
            box_local_y = box_y * setting.piece_size + setting.piece_first_y
            #
            log.info("鼠标点击事件：判断开始之前：各个参数状态-----开始")
            log.info(f"all_pieces: {all_pieces}")
            log.info(f"self.is_first_selected: {self.is_first_selected}")
            log.info(f"self.first_selected_img: {self.first_selected_img}")
            log.info(f"self.first_selected_value: {self.first_selected_value}")
            log.info(f"self.second_selected_img: {self.second_selected_img}")
            log.info(f"self.second_selected_value: {self.second_selected_value}")
            log.info(f"self.nowPlayer: {self.nowPlayer}")
            log.info(f"self.player1Color: {self.player1Color}")
            log.info(f"self.player2Color: {self.player2Color}")
            log.info(f"self.numCount: {self.numCount}")
            log.info(f"self.box_open_dict: {self.box_open_dict}")
            log.info("鼠标点击事件：判断开始之前：各个参数状态-----结束")
            log.info("=" * 30)
            # 棋子状态为True
            if piece_state is True:
                box_color = box_piece['box_key'].split('_')[0]
                # 当前玩家选择了当前玩家方阵的棋子
                if (self.player1Color == box_color and self.nowPlayer == self.player1) or \
                        (self.player2Color == box_color and self.nowPlayer == self.player2):
                    # 第一次选择为空
                    if self.is_first_selected is True:
                        # 第一次选择棋子，加载选中框
                        self.first_selected_img = self.cv.create_image(box_local_x, box_local_y, image=piece_selected_img, anchor=NW)
                        # 将第一次选择的状态改为false
                        self.is_first_selected = False
                        # 记录下第一次选择的box坐标
                        self.first_selected_value = box_xy
                        # 播放选择棋子的音效
                        play_music.load_play_sound(setting.xz)
                        #
                        log.info("鼠标点击事件：piece_state is True-->self.is_first_selected is True：各个参数状态-----开始")
                        log.info(f"all_pieces: {all_pieces}")
                        log.info(f"self.is_first_selected: {self.is_first_selected}")
                        log.info(f"self.first_selected_img: {self.first_selected_img}")
                        log.info(f"self.first_selected_value: {self.first_selected_value}")
                        log.info(f"self.second_selected_img: {self.second_selected_img}")
                        log.info(f"self.second_selected_value: {self.second_selected_value}")
                        log.info(f"self.nowPlayer: {self.nowPlayer}")
                        log.info(f"self.player1Color: {self.player1Color}")
                        log.info(f"self.player2Color: {self.player2Color}")
                        log.info(f"self.numCount: {self.numCount}")
                        log.info("鼠标点击事件：piece_state is True-->self.is_first_selected is True：各个参数状态-----结束")
                    # 第一次选择不为空
                    else:
                        # 第二次选择的棋子坐标，与第一次选择的坐标相同，表示选择同一个棋子，则认为取消选择
                        if self.first_selected_value == box_xy:
                            # 恢复第一次选择的状态
                            self.cv.delete(self.first_selected_img)
                            self.is_first_selected = True
                            self.first_selected_img = None
                            self.first_selected_value = None
                            # 播放选择棋子的音效
                            play_music.load_play_sound(setting.zqwc)
                            #
                            log.info("鼠标点击事件：self.first_selected_value[0] == box_xy：各个参数状态-----开始")
                            log.info(f"all_pieces: {all_pieces}")
                            log.info(f"self.is_first_selected: {self.is_first_selected}")
                            log.info(f"self.first_selected_img: {self.first_selected_img}")
                            log.info(f"self.first_selected_value: {self.first_selected_value}")
                            log.info(f"self.second_selected_img: {self.second_selected_img}")
                            log.info(f"self.second_selected_value: {self.second_selected_value}")
                            log.info(f"self.nowPlayer: {self.nowPlayer}")
                            log.info(f"self.player1Color: {self.player1Color}")
                            log.info(f"self.player2Color: {self.player2Color}")
                            log.info(f"self.numCount: {self.numCount}")
                            log.info("鼠标点击事件：self.first_selected_value[0] == box_xy：各个参数状态-----结束")
                        # 否则就把第一次的选择改为自己方阵的其他棋子
                        else:
                            self.cv.delete(self.first_selected_img)
                            self.first_selected_img = self.cv.create_image(box_local_x, box_local_y, image=piece_selected_img, anchor=NW)
                            # 记录下重新第一次选择的box坐标
                            self.first_selected_value = box_xy
                            # 播放选择棋子的音效
                            play_music.load_play_sound(setting.xz)
                            #
                            log.info("鼠标点击事件：否则就把第一次的选择改为自己方阵的其他棋子：各个参数状态-----开始")
                            log.info(f"all_pieces: {all_pieces}")
                            log.info(f"self.is_first_selected: {self.is_first_selected}")
                            log.info(f"self.first_selected_img: {self.first_selected_img}")
                            log.info(f"self.first_selected_value: {self.first_selected_value}")
                            log.info(f"self.second_selected_img: {self.second_selected_img}")
                            log.info(f"self.second_selected_value: {self.second_selected_value}")
                            log.info(f"self.nowPlayer: {self.nowPlayer}")
                            log.info(f"self.player1Color: {self.player1Color}")
                            log.info(f"self.player2Color: {self.player2Color}")
                            log.info(f"self.numCount: {self.numCount}")
                            log.info("鼠标点击事件：否则就把第一次的选择改为自己方阵的其他棋子：各个参数状态-----结束")
                # 当前玩家点击了非当前玩家方阵的棋子
                else:
                    if self.is_first_selected is False:
                        self.second_selected_value = box_xy
                        # 逻辑处理：比较两个棋子的大小
                        box1_xy = self.first_selected_value
                        box2_xy = self.second_selected_value
                        box1_name = all_pieces[box1_xy]['box_key']
                        box2_name = all_pieces[box2_xy]['box_key']
                        # vs_res的结果只有'true','false','both'
                        vs_res = game.piece_VS_piece(box1_xy, box2_xy, box1_name, box2_name, all_pieces)
                        log.info(f"逻辑处理的结果: {vs_res}")
                        if vs_res == 'false':
                            # 恢复第一次选择的状态
                            self.cv.delete(self.first_selected_img)
                            self.is_first_selected = True
                            self.first_selected_img = None
                            self.first_selected_value = None
                            self.second_selected_img = None
                            self.second_selected_value = None
                        else:
                            if vs_res == 'true':
                                # 更新图片
                                self.cv.delete(self.box_open_dict[box2_xy])
                                self.box_open_dict[box2_xy] = self.box_open_dict[box1_xy]
                                self.cv.coords(self.box_open_dict[box1_xy], box_local_x, box_local_y)
                                self.box_open_dict[box1_xy] = None
                                # 更新all_pieces
                                all_pieces[box1_xy]['box_key'] = None
                                all_pieces[box1_xy]['state'] = None
                                all_pieces[box2_xy]['box_key'] = box1_name
                            elif vs_res == 'both':
                                # 更新图片
                                self.cv.delete(self.box_open_dict[box1_xy])
                                self.cv.delete(self.box_open_dict[box2_xy])
                                self.box_open_dict[box1_xy] = None
                                self.box_open_dict[box2_xy] = None
                                # 更新all_pieces
                                all_pieces[box1_xy]['box_key'] = None
                                all_pieces[box1_xy]['state'] = None
                                all_pieces[box2_xy]['box_key'] = None
                                all_pieces[box2_xy]['state'] = None
                            # 加载吃棋音效
                            play_music.load_play_sound(setting.cq)
                            # 恢复第一次选择的状态
                            self.cv.delete(self.first_selected_img)
                            self.is_first_selected = True
                            self.first_selected_img = None
                            self.first_selected_value = None
                            self.second_selected_img = None
                            self.second_selected_value = None
                            # 更新playerinfo
                            self.upd_player_info(box_piece['box_key'])
                            #
                            log.info("鼠标点击事件：当前玩家选择了对方的棋子：各个参数状态-----开始")
                            log.info(f"all_pieces: {all_pieces}")
                            log.info(f"self.is_first_selected: {self.is_first_selected}")
                            log.info(f"self.first_selected_img: {self.first_selected_img}")
                            log.info(f"self.first_selected_value: {self.first_selected_value}")
                            log.info(f"self.second_selected_img: {self.second_selected_img}")
                            log.info(f"self.second_selected_value: {self.second_selected_value}")
                            log.info(f"self.nowPlayer: {self.nowPlayer}")
                            log.info(f"self.player1Color: {self.player1Color}")
                            log.info(f"self.player2Color: {self.player2Color}")
                            log.info(f"self.numCount: {self.numCount}")
                            log.info("鼠标点击事件：当前玩家选择了对方的棋子：各个参数状态-----结束")
                            log.info("=" * 30)
            # 棋子状态为Flase
            elif piece_state is False:
                if self.is_first_selected is False:
                    # 恢复第一次选择的状态
                    self.cv.delete(self.first_selected_img)
                    self.is_first_selected = True
                    self.first_selected_img = None
                    self.first_selected_value = None
                # 删除原有的棋子背景图片
                self.cv.delete(self.box_back_dict[box_xy])
                all_pieces[f'box_{box_x}_{box_y}']['state'] = True
                # 取得all_pieces中对应的棋子标记
                box_key = box_piece['box_key']
                # 根据字符串最后一个字符判断，需要读取的img图片
                if box_key[-1:].isnumeric():
                    box_key = box_key[:-1]
                # 从pieces_img字典中获取棋子标记对应的img图片
                piece_img = pieces_img[box_key]
                # 加载新打开的图片
                piece_open = self.cv.create_image(box_local_x, box_local_y, image=piece_img, anchor=NW)
                self.box_open_dict[box_xy] = piece_open
                # 播放选择棋子的音效
                play_music.load_play_sound(setting.xz)
                # 更新player_info的信息
                self.upd_player_info(box_key)
                #
                log.info("鼠标点击事件：piece_state is False：各个参数状态-----开始")
                log.info(f"self.is_first_selected: {self.is_first_selected}")
                log.info(f"self.first_selected_img: {self.first_selected_img}")
                log.info(f"self.first_selected_value: {self.first_selected_value}")
                log.info(f"self.second_selected_img: {self.second_selected_img}")
                log.info(f"self.second_selected_value: {self.second_selected_value}")
                log.info(f"self.nowPlayer: {self.nowPlayer}")
                log.info(f"self.player1Color: {self.player1Color}")
                log.info(f"self.player2Color: {self.player2Color}")
                log.info(f"self.numCount: {self.numCount}")
                log.info("鼠标点击事件：piece_state is False：各个参数状态-----结束")
                log.info("=" * 30)
            # 棋子状态为None
            else:
                pass

    # 关闭窗口事件
    def close_window(self):
        dialog_value = {
            'title': '退出游戏',
            'text': '游戏正在进行中，确定要退出吗？',
            'bitmap': 'question',
            'default': 0,
            'strings': ('确定', '取消')
        }
        d = dialog.Dialog(self.master, dialog_value)
        if d.num == 0:
            play_music.quit_music()
            log.info("游戏退出！")
            self.master.destroy()


if __name__ == '__main__':
    # 整个游戏的入口
    root = Tk()
    # 设置标题
    root.title(setting.game_title)
    # 设置图标
    root.iconbitmap(setting.favicon)
    # 设置窗体固定大小，并设置不能改变大小
    root.geometry(f"{setting.screen_width}x{setting.screen_height}+{setting.window_start_x}+{setting.window_start_y}")
    root.resizable(width=False, height=False)
    # 加载棋盘图片（Canvas的bug，PhonoImage只能和mainloop放一起，不然加载不出图片）
    board_img = PhotoImage(file=setting.chess_board)
    # 加载棋子背面图片，需要改变一下棋子的大小，使用了pil里面的Image和ImageTk
    pieces_back_img = common.change_img(setting.pieces_back)
    # 加载棋子选中时的颜色图片
    piece_selected_img = PhotoImage(file=setting.piece_selected)
    # 加载关于窗体中的favicon图标
    red_jiang_img = common.change_img('images/piece_red_jiang.gif', width=64, height=64)
    black_jiang_img = common.change_img('images/piece_black_jiang.gif', width=64, height=64)
    # 加载所有棋子图片
    pieces_dict = game.get_piece_image()
    pieces_img = common.change_img(img=pieces_dict)
    # 加载背景音乐
    play_music.is_not_busy()
    #
    chess = Chess(master=root)
    root.protocol('WM_DELETE_WINDOW', chess.close_window)
    root.mainloop()
