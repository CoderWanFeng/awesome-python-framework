#!/usr/bin/env python
# encoding: utf-8
"""
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.comment import parse_user_info


class FollowerSpider(Spider):
    """
    微博关注数据采集
    """
    name = "follower"
    base_url = 'https://weibo.com/ajax/friendships/friends'

    def start_requests(self):
        """
        爬虫入口
        """
        # 这里user_ids可替换成实际待采集的数据
        user_ids = ['7726957925']
        for user_id in user_ids:
            url = self.base_url + f"?page=1&uid={user_id}"
            yield Request(url, callback=self.parse, meta={'user': user_id, 'page_num': 1})

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        for user in data['users']:
            item = dict()
            item['fan_id'] = response.meta['user']
            item['follower_info'] = parse_user_info(user)
            item['_id'] = response.meta['user'] + '_' + item['follower_info']['_id']
            yield item
        if data['users']:
            response.meta['page_num'] += 1
            url = self.base_url + f"?page={response.meta['page_num']}&uid={response.meta['user']}"
            yield Request(url, callback=self.parse, meta=response.meta)
