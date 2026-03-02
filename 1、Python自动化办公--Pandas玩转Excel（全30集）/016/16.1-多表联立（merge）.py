# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd

students = pd.read_excel('./Student_score.xlsx', sheet_name='Students')
scores = pd.read_excel('./Student_score.xlsx', sheet_name='Scores')
table = students.merge(scores, how="left", on="ID").fillna(0)
table.Score = table.Score.astype(int)
print(table)
