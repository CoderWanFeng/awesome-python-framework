"""
如果报错：ModuleNotFoundError: No module named 'tkinter'
请按照视频说明进行操作：https://www.bilibili.com/video/BV18g411h7jJ
"""

import turtle


def goto(x, y):  # 定义提笔的位置
    turtle.penup()  # 将笔提起，移动时无图
    turtle.goto(x, y)
    turtle.pendown()  # 将笔放下，移动时绘图。


def yuebing_wai():
    turtle.pensize(20)  # 画笔调粗点
    turtle.color("#F8CD32", "#FBA92D")  # 填充颜色，F8CD32是圆圈的边缘颜色，FBA92D是圆圈的填充颜色
    goto(0, -200)  # 画笔起点位于（0,0）点的下方200向量处
    turtle.begin_fill()  # 准备开始填充
    turtle.circle(200)  # 定义半径
    turtle.end_fill()  # 填充结束


def yuebing_zhong():
    goto(0, 0)  # 画笔起点位于（0，0）处
    turtle.color("#F0BE7C")
    for _ in range(20):  # _是占位符，表示临时变量，仅用一次，后面无需再用到
        turtle.right(18)  # 顺时针移动18度
        turtle.begin_fill()
        turtle.forward(220)  # 向前移动的距离
        turtle.circle(40, 180)  # 上一条向前移动220之后，开始画半径40的半圆
        turtle.goto(0, 0)  # 画完半圆之后回到（0，0）
        turtle.right(360)  # 顺时针转个360度
        turtle.end_fill()


def yuebing_nei():  # 逻辑同上
    turtle.right(360)
    turtle.color('#F5E16F')  # 内层颜色
    goto(0, -180)
    for _ in range(12):
        turtle.begin_fill()
        turtle.circle(60, 120)
        turtle.left(180)
        turtle.circle(60, 120)
        turtle.end_fill()


def fu():  #
    turtle.right(50)
    goto(-70, -80)  # 更高坐标尽量使字靠中间
    turtle.color("Gold")  # 颜色
    turtle.write("福", font=("华文隶书", 120, "bold"))
    turtle.done()


if __name__ == '__main__':
    turtle.speed(90)
    yuebing_zhong()
    yuebing_wai()
    yuebing_nei()
    fu()

turtle.done()
