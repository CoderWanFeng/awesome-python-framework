# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from spider.Source import Source
from spider.req import req
import json

URL = 'api.php'


# count 每页数据条数
# source 音乐数据源
# pages 当前页
# keyword 查找关键字
# 获取歌曲清单
def getMusicListByKeyword(count, source, pages, keyword):
    params = {'types': 'search', 'count': count, 'source': source, 'pages': pages, 'name': keyword}
    r = req("POST", URL, params)
    if r != None:
        return json.loads(r.text)
    else:
        return []


# 获取音乐url
def getMusicUrl(id, source):
    params = {'types': 'url', 'id': id, 'source': source}
    r = req("POST", URL, params)
    if r != None:
        result = json.loads(r.text)
        return result
    else:
        return None


# 获取音乐封面图
def getMusicPic(picId, source):
    params = {'types': 'pic', 'id': picId, 'source': source}
    r = req("POST", URL, params)
    return json.loads(r.text)


# 获取歌词
def getMusicLyric(lyricId, source):
    params = {'types': 'lyric', 'id': lyricId, 'source': source}
    r = req("POST", URL, params)
    return json.loads(r.text)


# 根据榜单id爬取榜单歌曲
def getMusicListById(id):
    params = {'types': 'playlist', 'id': id}
    r = req("POST", URL, params)
    return json.loads(r.text)
