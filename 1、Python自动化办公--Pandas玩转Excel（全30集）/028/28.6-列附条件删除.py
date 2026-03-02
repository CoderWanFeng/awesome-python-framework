# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd
import numpy as np

page_001 = pd.read_excel('Students.xlsx', sheet_name='Page_001')
page_002 = pd.read_excel('Students.xlsx', sheet_name='Page_002')
students = pd.concat([page_001, page_002]).reset_index(drop=True)
students['Age'] = 25
students.drop(columns=['Score', 'Age'], inplace=True)
students.insert(1, column='Foo', value=np.repeat('foo', len(students)))
students.rename(columns={'Foo': 'FOO', 'Name': 'NAME'}, inplace=True)

students['ID'] = students['ID'].astype(float)
for i in range(5, 15):
    students['ID'].at[i] = np.nan
students.dropna(inplace=True)
print(students)
