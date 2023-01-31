# 部门:人工智能
# 编写人:张开然
# 开发日期: 2023/1/6
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import turtle
import random
from turtle import Terminator
from tkinter import *
from tkinter import messagebox
global score
score = 0
def conduct():
    try:
        # 创建游戏的主窗口,设定窗口的大小以及背景
        boundary = turtle.Screen()
        boundary.setup(600, 800, 100, 10)
        boundary.bgcolor("wheat")
        boundary.title("2048小游戏")
        boundary.tracer(0)
        boundary.register_shape("bg.gif")
        boundary.register_shape("2.gif")
        boundary.register_shape("4.gif")
        boundary.register_shape("8.gif")
        boundary.register_shape("16.gif")
        boundary.register_shape("32.gif")
        boundary.register_shape("64.gif")
        boundary.register_shape("128.gif")
        boundary.register_shape("256.gif")
        boundary.register_shape("512.gif")
        boundary.register_shape("1024.gif")
        boundary.register_shape("2048.gif")
        boundary.register_shape("title.gif")
        boundary.register_shape("score.gif")

        # 先定义一个turtle类用来画背景
        class Background(turtle.Turtle):
            def __init__(self):
                super().__init__()  #通过super()函数来调用turtle.Turtle的属性方法
                self.penup()
                self.hideturtle()

            def base_back(self):
                self.shape("title.gif")
                self.goto(-125, 300)
                self.stamp()
                self.shape("score.gif")
                self.goto(125, 300)
                self.stamp()
                self.shape("bg.gif")
                for i in co_system:
                    self.goto(i)
                    self.stamp()
            def show_score(self, score):
                self.goto(125, 275)
                self.clear()
                self.write(f'{score}', align="center", font=('Arial', 20, 'bold'))



        # 定义一个类用来创建每个数字块,random_appear方法会在每一个空的位置生成一个Blocks对象
        class Blocks(turtle.Turtle):
            def __init__(self):
                super().__init__()
                self.penup()

            def random_appear(self):
                block_num = random.choice([2, 4])
                self.shape(f'{block_num}.gif')
                location = random.choice(co_system)
                self.goto(location)
                co_system.remove(location)
                block_list.append(self)  # **将每一次随机生成的新的Block对象都存入到这个列表中**

            """定义一个go函数，通过传入参数的不同来实现每个处于不同位置的数字块的移动方式
            a,b,c分别是block_list中每一个block对象对应的x坐标或者y坐标，根据每一个block的横纵坐标判断移动的距离
            g_x,g_y分别是每一个block沿着x轴或者y轴移动的距离，此前规定单元格为50，所以距离大小都是100
            direct代表移动的方向，传入的direct参数决定了移动的方向是横向还是纵向"""
            def go(self, a, b, c, g_x, g_y, direct):
                # 定义三个空列表用来存放移动距离不同的block
                go_1_times, go_2_times, go_3_times = [], [], []
                global moveornot
                moveornot = 0

                for i in block_list:
                    if direct == "landscape":
                        if i.xcor() == a:
                            go_1_times.append(i)
                        elif i.xcor() == b:
                            go_2_times.append(i)
                        elif i.xcor() == c:
                            go_3_times.append(i)
                    else:
                        if i.ycor() == a:
                            go_1_times.append(i)
                        elif i.ycor() == b:
                            go_2_times.append(i)
                        elif i.ycor() == c:
                            go_3_times.append(i)
                for k1 in go_1_times:
                    k1.move(k1.xcor()+g_x, k1.ycor()+g_y)
                for k2 in go_2_times:
                    for num in range(2):
                        k2.move(k2.xcor() + g_x, k2.ycor() + g_y)
                for k3 in go_3_times:
                    for num in range(3):
                        k3.move(k3.xcor() + g_x, k3.ycor() + g_y)

                # 在每次移动后进行判断，因为只有移动了才可以产生新的数字块
                if moveornot != 0:
                    new_block = Blocks()
                    new_block.random_appear()
                judge =judge_game()
                if not judge:
                    winorlose.win_lose_tip("游戏失败,按空格退出")
                for blo in block_list:
                    if blo.shape() == "2048.gif" and judge:
                        winorlose.win_lose_tip("游戏成功,按空格退出")




            """定义一个move函数，实现数字块的具体移动，两种不同的情况
                1）要移动的位置上没有数字快
                2）要移动的位置上有数字块，此时就要判断是否相等，相等就合并，不然不能移动"""
            def move(self, x, y):
                global moveornot,score
                # 要移动的坐标(x,y)在可用的坐标列表里
                if (x, y) in co_system:
                    co_system.append(self.pos())
                    self.goto(x, y)
                    co_system.remove(self.pos())
                    moveornot += 1
                # 要移动的坐标(x,y)有数字块，进行判断
                # 要前往的坐标不在可用的坐标列表co_system中
                else:
                    """判断数字块是否能合并，就是要判断 1）数字相同 2）相邻距离为100"""
                    for i in block_list:
                        if i.pos() == (x, y) and i.shape() == self.shape():
                            co_system.append(self.pos())
                            self.goto(x, y)
                            self.hideturtle()
                            block_list.remove(self)
                            image_num = int(i.shape()[0:-4])
                            i.shape(f'{2 * image_num}.gif')
                            score += image_num
                            score += image_num
                            the_score.show_score(score)
                    moveornot += 1
                    """首先对block_list中的每个Block对象进行遍历，如果它们中某一个的位置恰好就是self这
                       单个block要移动的位置，而且这个处于self周围的block它的图形与self的图形相同，就
                        就需要先从可用坐标中加入self的当前坐标，接着移动self到目标位置并且从block_list中
                        删除self这个对象，接着改变这个对应的i的图形"""

            """4个go_direction函数，前三个参数分别代表可以执行对应操作的数字块对应的横或纵坐标，比如go_right
                只有横坐标不为150的数字块才拥有向右移动的能力"""
            def go_right(self):
                self.go(50, -50, -150, 100, 0, "landscape")

            def go_left(self):
                self.go(-50, 50, 150, -100, 0, "landscape")

            def go_up(self):
                self.go(50, -50, -150, 0, 100, "portrait")

            def go_down(self):
                self.go(-50, 50, 150, 0, -100, "portrait")
        # 定义一个提示的类
        class Tips(turtle.Turtle):
            def __init__(self):
                super().__init__()
                self.penup()
                self.hideturtle()
                self.color("black")

            # 这个函数用来显示提示的内容，设置出现位置和字号，字体
            def win_lose_tip(self, text):
                self.write(f'{text}', align='center', font=('宋体', 20, 'bold'))
        """定义函数来判断当前游戏是否失败，判断依据:只要相邻的两个数字块相同，游戏就还可以进行，利用两层for循环
            对block_list中的每一个Block和其他所有的Blockj进行遍历，只要图形(shape)相同且距离等于100就还可以继续
            如果都没有，游戏就判断失败"""
        def judge_game():
            if len(co_system) == 0:
                for i in block_list:
                    for j in block_list:
                        if i.shape() == j.shape() and j.distance(i) == 100:
                            return True
                        else:
                            return False
            else:
                return True


        # 每一块图片被贴的具体坐标系
        co_system = [(-150, 150), (-50, 150), (50, 150), (150, 150),
                     (-150, 50), (-50, 50), (50, 50), (150, 50),
                     (-150, -50), (-50, -50), (50, -50), (150, -50),
                     (-150, -150), (-50, -150), (50, -150), (150, -150)]

        block_list = []  # 创建一个空的列表用于存放游戏过程中每一个数字块的具体位置
        back = Background()
        back.base_back()
        block = Blocks()
        the_score = Background()
        score = 0
        the_score.show_score(score)
        block.random_appear()
        winorlose = Tips()
        boundary.listen()
        boundary.onkey(block.go_left, "Left")
        boundary.onkey(block.go_right, "Right")
        boundary.onkey(block.go_up, "Up")
        boundary.onkey(block.go_down, "Down")
        boundary.onkey(boundary.bye, "space")
        while True:
            boundary.update()
    except Terminator:pass
    except IndexError:turtle.bye()
