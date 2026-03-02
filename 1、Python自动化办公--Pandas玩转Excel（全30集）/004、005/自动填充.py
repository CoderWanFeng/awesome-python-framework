# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd
from datetime import date, timedelta


def add_month(d, md):
    yd = md // 12
    m = d.month + md % 12
    if m != 12:
        yd += m // 12
        m = m % 12
    return date(d.year + yd, m, d.day)


books = pd.read_excel("./Books.xlsx", skiprows=3, usecols="C:F", index_col=None,
                      dtype={"ID": str, "InStore": str, "Date": str})
start = date(2018, 1, 1)
for i in books.index:
    books["ID"].at[i] = i + 1  # 拿到Series改
    # books.at[i, "ID"] = i + 1  # 直接改DataFrame
    books["InStore"].at[i] = "Yes" if i % 2 == 0 else "No"
    # books["Date"].at[i] = start + timedelta(days=i)  # 加一天
    # books["Date"].at[i] = date(start.year + i, start.month, start.day)  # 加一年
    books["Date"].at[i] = add_month(start, i)  # 加一月
books.set_index("ID", inplace=True)
print(books)
books.to_excel("./Output.xlsx")
print("Done!")
