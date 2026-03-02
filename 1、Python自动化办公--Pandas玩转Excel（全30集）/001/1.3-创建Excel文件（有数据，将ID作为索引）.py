# -*- coding: utf-8 -*-
# ⭐Python 60套学习资源：http://t.cn/A6xASARf
# 📱公众号 :程序员晚枫 读者交流群：https://www.python4office.cn/wechat-group/
# 🏠2022最新视频：1行代码，实现自动化办公：https://www.bilibili.com/video/BV1pT4y1k7FH
import pandas as pd

df = pd.DataFrame({"ID": [1, 2, 3], "Name": ["Tim", "Victory", "Nick"]})
# 创建DataFrame对象
df=df.set_index("ID")
# 设置索引
print(df)
df.to_excel("./001-data-index.xlsx")
print("Done!")
