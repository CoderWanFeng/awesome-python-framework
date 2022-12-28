# -*- coding: UTF-8 -*-
'''
@Author  ：程序员晚枫，B站/抖音/微博/小红书/公众号
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2022/12/28 21:02 
@Description     ：
'''

import segno

video = segno.make('http://t.cn/A6K3NfvL')
video.save('Video.png', scale=4)