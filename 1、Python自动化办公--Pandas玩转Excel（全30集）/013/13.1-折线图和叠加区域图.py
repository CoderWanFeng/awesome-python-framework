# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd
import matplotlib.pyplot as plt

weeks = pd.read_excel("./example.xlsx", index_col="Week")
print(weeks)
print(weeks.columns)
# weeks.plot(y=['Accessories', 'Bikes', 'Clothing', 'Components'])
weeks.plot.area(y=['Accessories', 'Bikes', 'Clothing', 'Components'])
# weeks.plot.bar(y=['Accessories', 'Bikes', 'Clothing', 'Components'],stacked=True)
plt.title("Sales Weekly Trend", fontsize=16, fontweight="bold")
plt.ylabel("Total", fontsize=12, fontweight="bold")
plt.xticks(weeks.index, fontsize=8)
plt.show()
