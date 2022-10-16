# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：http://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd

page_001 = pd.read_excel('Students.xlsx', sheet_name='Page_001')
page_002 = pd.read_excel('Students.xlsx', sheet_name='Page_002')
students = page_001.append(page_002).reset_index(drop=True)
stu = pd.Series({'ID': 41, 'Name': 'Abel', 'Score': 90})
students = students.append(stu, ignore_index=True)
students.at[39, "Name"] = "Bailey"
students.at[39, "Score"] = "120"  # 修改内容
stu = pd.Series({'ID': 39, 'Name': 'Ammy', 'Score': 150})
students.iloc[38] = stu  # 替换整行
stu = pd.Series({'ID': 101, 'Name': 'Danni', 'Score': 101})
part1 = students[:20]  # .iloc[] is the same
part2 = students[20:]
students = part1.append(stu, ignore_index=True).append(part2).reset_index(drop=True)

for i in range(5, 15):
    students['Name'].at[i] = ''
missing = students.loc[students['Name'] == '']
students.drop(missing.index, inplace=True)
students = students.reset_index(drop=True)
print(students)
    