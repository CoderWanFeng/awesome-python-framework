# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：http://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd
import pyodbc
import sqlalchemy

# 由于未安装数据库，此段代码未测试
query = 'SELECT FirstName, LastName FROM Person.Person'
connection = pyodbc.connect('DRIVER={SQL Server}; SERVER=(local); DATABASE=AdventureWorks;USER=sa;PASSWORD=123456')
df1 = pd.read_sql_query(query, connection)
print(df1.head())
engine = sqlalchemy.create_engine('mssql+pyodbc://sa:123456@(local)/AdventureWorks?driver=SQL+Server')
df2 = pd.read_sql_query(query, engine)
pd.options.display.max_columns = 999
print(df2.head())
