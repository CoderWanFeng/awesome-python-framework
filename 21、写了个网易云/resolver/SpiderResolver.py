# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# 解析爬虫模块数据 再也不必牵一发而动全身啦
from bean.Music import Music
from spider.api import *


def getMusicListByIdResolver(id):
    data = getMusicListById(id)
    if data.get('code') == 200:
        playlist = data.get('playlist')
        coverImgUrl = playlist.get('coverImgUrl')
        tracks = playlist.get('tracks')

        musicList = []
        for track in tracks:
            music = Music()
            music.id = track.get('id')
            music.name = track.get('name')
            music.artists = []
            for artist in track.get('ar'):
                music.artists.append(artist.get('name'))
            music.avatar = track.get('al').get('picUrl')
            music.album = track.get('al').get('name')
            musicList.append(music)
        return {
            'coverImgUrl': coverImgUrl,
            'musicList': musicList
        }


# 获取网易云榜单歌曲url
def getMusicUrlResolver(id):
    result = getMusicUrl(id, Source.Netease_Cloud_Music.value)
    if result != None:
        return result.get('url')
    else:
        return ''


# 获取网易云榜单歌曲url和size
def getMusicUrlSizeResolver(id):
    return getMusicUrl(id, Source.Netease_Cloud_Music.value)


def getMusicListByKeywordResolver(count, pages, keyword):
    musicList = []
    for s in Source:
        for track in getMusicListByKeyword(count, s.value, pages, keyword):
            music = Music()
            music.id = track.get('id')
            music.name = track.get('name')
            music.artists = []
            for artist in track.get('artist'):
                music.artists.append(artist)
            music.avatarId = track.get('pic_id')
            music.album = track.get('album')
            music.lyricId = track.get('lyric_id')
            music.source = track.get('source')
            musicList.append(music)
    return musicList


def getAvatarByIdResolver(id):
    data = getMusicPic(id, Source.Netease_Cloud_Music.value)
    return data.get('url')


def getLyricByIdResolver(id, source):
    return getMusicLyric(id, source).get('lyric')
