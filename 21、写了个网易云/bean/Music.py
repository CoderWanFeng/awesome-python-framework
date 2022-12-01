# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# 音乐实体类
class Music:
    __slots__ = (
        '__id', '__name', '__artists', '__album', '__url', '__avatar', '__lyric', '__favorite', '__path', '__avatarId',
        '__lastestTime', '__size', '__downloadTime', '__lyricId', '__source', '__filePath')

    def __init__(self, id=None, name=None, artists=None, album=None, url='', avatar=None, lyric=None, favorite=False,
                 path=None, avatarId=None, lastestTime='', size=None, downloadTime='', lyricId=None, source=None,
                 filePath=None
                 ):
        self.__id = id  # 歌曲id 唯一不失效
        self.__name = name  # 歌曲名称
        self.__artists = artists  # 歌手 列表
        self.__album = album  # 专辑
        self.__url = url  # 歌曲链接
        self.__avatar = avatar  # 歌曲封面链接
        self.__lyric = lyric  # 歌词
        self.__favorite = favorite  # 是否喜欢
        self.__path = path  # 歌曲封面路径
        self.__avatarId = avatarId  # 封面id
        self.__lastestTime = lastestTime  # 最新播放时间
        self.__size = size  # 音乐大小
        self.__downloadTime = downloadTime  # 下载时间
        self.__lyricId = lyricId
        self.__source = source
        self.__filePath = filePath

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def artists(self):
        return self.__artists

    @property
    def album(self):
        return self.__album

    @property
    def url(self):
        return self.__url

    @property
    def avatar(self):
        return self.__avatar

    @property
    def lyric(self):
        return self.__lyric

    @property
    def favorite(self):
        return self.__favorite

    @property
    def path(self):
        return self.__path

    @property
    def avatarId(self):
        return self.__avatarId

    @property
    def lastestTime(self):
        return self.__lastestTime

    @property
    def size(self):
        return self.__size

    @property
    def downloadTime(self):
        return self.__downloadTime

    @property
    def lyricId(self):
        return self.__lyricId

    @property
    def source(self):
        return self.__source

    @property
    def filePath(self):
        return self.__filePath

    @id.setter
    def id(self, id):
        self.__id = id

    @name.setter
    def name(self, name):
        self.__name = name

    @artists.setter
    def artists(self, artists):
        self.__artists = artists

    @album.setter
    def album(self, album):
        self.__album = album

    @url.setter
    def url(self, url):
        self.__url = url

    @avatar.setter
    def avatar(self, avatar):
        self.__avatar = avatar

    @lyric.setter
    def lyric(self, lyric):
        self.__lyric = lyric

    @favorite.setter
    def favorite(self, favorite):
        self.__favorite = favorite

    @path.setter
    def path(self, path):
        self.__path = path

    @avatarId.setter
    def avatarId(self, avatarId):
        self.__avatarId = avatarId

    @lastestTime.setter
    def lastestTime(self, lastestTime):
        self.__lastestTime = lastestTime

    @size.setter
    def size(self, size):
        self.__size = size

    @downloadTime.setter
    def downloadTime(self, downloadTime):
        self.__downloadTime = downloadTime

    @lyricId.setter
    def lyricId(self, lyricId):
        self.__lyricId = lyricId

    @source.setter
    def source(self, source):
        self.__source = source

    @filePath.setter
    def filePath(self, filePath):
        self.__filePath = filePath

    def __repr__(self):
        return "id:%s  name:%s  artists:%s  album:%s avatar:%s avatarId:%s" % (
            self.__id, self.__name, self.__artists, self.__album, self.__avatar, self.__avatarId)
