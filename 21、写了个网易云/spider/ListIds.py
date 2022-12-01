# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# 音乐榜单配置
from enum import Enum, unique


# 热歌榜 3778678
# 新歌榜 3779629
# 飙升榜 19723756
# 清酒踏月 3174582381
# 华语金曲榜 4395559
# 中国TOP排行榜（内地榜） 64016
# 中国TOP排行榜（港台榜） 112504
# 原创榜 2884035
# 随机 2884037

# 榜单id
@unique
class ListIds(Enum):
    HOT = 3778678
    NEW = 3779629
    SOAR = 19723756
    WINE = 3174582381
    GOLD = 4395559
    MAINLAND = 64016
    HKAT = 112504
    ORIGIN = 2884035
    RANDOM = 2884037
