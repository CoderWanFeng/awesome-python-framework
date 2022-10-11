# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：http://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

sales = pd.read_excel('./Sales.xlsx', dtype={'Month': str})
print(sales)
# plt.bar(sales.index, sales.Revenue)
# plt.title("Sales")
# plt.xticks(sales.index, sales.Month, rotation=90)
# plt.tight_layout()
# plt.show()
slope, intercept, r, p, std_err = linregress(sales.index, sales.Revenue)  # slope:斜率 intercept：截距
exp = sales.index * slope + intercept
print("2019年12月预计销售额：" + str(slope * 35 + intercept))
plt.scatter(sales.index, sales.Revenue)
plt.plot(sales.index, exp, color='orange')
plt.title(f"y={slope}*x+{intercept}")
plt.xticks(sales.index, sales.Month, rotation=90)
plt.show()
