# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd

books = pd.read_excel("./example.xlsx", index_col="ID")
# books["Price"] = books["ListPrice"] * books["Discount"]  # 直接计算
for i in books.index:  # 用循环计算
    books["Price"].at[i] = books["ListPrice"].at[i] * books["Discount"].at[i]
print(books)
