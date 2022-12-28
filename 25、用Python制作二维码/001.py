# -*- coding: UTF-8 -*-
'''
@Author  ：程序员晚枫，B站/抖音/微博/小红书/公众号
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2022/12/28 20:58 
@Description     ：
'''

import segno

price_tag = segno.make("https://mp.weixin.qq.com/s/BRBAJLruGGofgpntwywTGA")
price_tag.save("Price Tag.png")