# -*- coding: UTF-8 -*-
'''
@Author  ：程序员晚枫，B站/抖音/微博/小红书/公众号
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2022/12/28 21:03
@Description     ：
'''
from tinydb import TinyDB
from potime import RunTime

@RunTime
def create_data():

    db = TinyDB('./city_fly.json')

    ci_t = db.table('city_index')
    ci_t.insert({'city': '广州', 'index': 55})
    ci_t.insert({'city': '北京', 'index': 66})
    ci_t.insert({'city': '杭州', 'index': 77})
    ci_t.insert({'city': '重庆', 'index': 88})

    ci_l = db.table('city_line')
    ci_l.insert({'from': '广州', 'to': '上海'})
    ci_l.insert({'from': '广州', 'to': '北京'})
    ci_l.insert({'from': '广州', 'to': '杭州'})
    ci_l.insert({'from': '广州', 'to': '重庆'})


if __name__ == '__main__':
    create_data()