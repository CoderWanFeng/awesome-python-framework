# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd


def age_18_to_30(a):
    return a >= 18 and a <= 30


def level_a(s):
    return 85 <= s <= 100


students = pd.read_excel("./example.xlsx", index_col="ID")
students = students.loc[students["Age"].apply(age_18_to_30)].loc[students.Score.apply(level_a)]
print(students)
