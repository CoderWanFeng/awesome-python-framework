# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd
from datetime import date
import numpy as np

pd.options.display.max_columns = 999
orders = pd.read_excel('./Orders.xlsx')
orders['Year'] = pd.DatetimeIndex(orders.Date).year
pt1 = orders.pivot_table(index='Category', columns='Year', values='Total', aggfunc=np.sum)
print(pt1)
groups = orders.groupby(['Category', 'Year'])
s = groups['Total'].sum()
c = groups['ID'].count()
pt2 = pd.DataFrame({'Sum': s, 'Count': c})
print(pt2)
