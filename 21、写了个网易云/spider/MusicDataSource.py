# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# 旧版拉取数据 当时我还太天真...
from spider.Source import Source
from spider.api import getMusicUrl, getMusicPic, getMusicLyric


class MusicDataSource():
    keyword = ''

    def __init__(self, count=1):
        self.count = count
        self.pages = 1
        pass

    def __searchMusicListResolver(self, source):
        recodes = []
        list = searchMusicList(self.count, source, self.pages, self.keyword)
        for item in list:
            recode = {}
            recode['name'] = item.get('name')
            recode['artist'] = item.get('artist')
            recode['album'] = item.get('album')
            recode['url'] = getMusicUrl(item.get('id'), source).get('url')
            recode['avatar'] = getMusicPic(item.get('pic_id'), source).get('url')
            recode['lyric'] = getMusicLyric(item.get('lyric_id'), source).get('lyric')
            recodes.append(recode)
        return recodes

    def __summaryMusicList(self):
        resultSet = []
        for item in Source:
            resultSet += self.__searchMusicListResolver(item.value)
        return resultSet

    def getMusicList(self, keyword):
        self.pages = 1
        self.keyword = keyword
        return self.__summaryMusicList()

    def getNext(self):
        self.pages = self.pages + 1
        return self.__summaryMusicList()
