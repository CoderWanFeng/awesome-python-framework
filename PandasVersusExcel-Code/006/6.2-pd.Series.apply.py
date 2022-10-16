# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：http://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd


def add_2(x):
    return x + 2


books = pd.read_excel("./example.xlsx", index_col="ID")
books["ListPrice"] = books["ListPrice"].apply(add_2)
print(books)