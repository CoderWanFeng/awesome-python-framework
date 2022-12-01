# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from enum import Enum, unique


@unique
class MenuType(Enum):
    FIND_MUSIC = 1
    VIDEO = 2
    MY_DEVICE = 3
    HOME = 4
    DOWNLOAD = 5
    RECENT = 6
    COLLECT = 7
    SEARCH = 8
