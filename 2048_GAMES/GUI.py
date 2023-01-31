# 部门:人工智能
# 编写人:张开然
# 开发日期: 2023/1/9
# !/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *
import little_game

global back, block, winorlose, block_list
root = Tk()
root.geometry("400x300+200+300")
root.title("2048小游戏")

class Application(Frame):
    """一个经典的GUI写法"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()  # pack是布局管理器，调用它才能让组件进行布局和显示
        self.createwidght()

    def createwidght(self):
        """创建组件"""
        self.btn01 = Button(self)
        self.btn01["text"] = "开始"
        self.btn01.pack()
        self.btn01["command"] = little_game.conduct


        #创建一个退出按钮
        self.btnQuit = Button(self, text="退出",command=root.destroy)
        self.btnQuit.pack()

app = Application(master=root)  #Application的父类是root


root.mainloop()#事件的循环
