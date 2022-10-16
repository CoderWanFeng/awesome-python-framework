# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：http://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd

s1 = pd.Series([1, 2, 3], index=[1, 2, 3], name="A")
s2 = pd.Series([10, 20, 30], index=[1, 2, 3], name="B")
s3 = pd.Series([100, 200, 300], index=[2, 3, 4], name="C")
df = pd.DataFrame([s1, s2, s3])
# 以列表形式添加
print(df)
df = pd.DataFrame({s1.name: s1, s2.name: s2, s3.name: s3})
# 以字典形式添加
print(df)
