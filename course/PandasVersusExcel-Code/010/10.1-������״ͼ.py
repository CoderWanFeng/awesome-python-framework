# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：http://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_excel("./example.xlsx")
students.sort_values(by="2017", inplace=True, ascending=False)
print(students)
students.plot.bar(x="Field", y=["2016", "2017"], color=["orange", "red"])
plt.title("International Students by Field", fontsize=16, fontweight="bold")
plt.xlabel("Field", fontweight="bold")
plt.ylabel("Number", fontweight="bold")
ax = plt.gca()
ax.set_xticklabels(students["Field"], rotation=45, ha="right")
f = plt.gcf()
f.subplots_adjust(left=0.2, bottom=0.42)
plt.tight_layout()
plt.show()
