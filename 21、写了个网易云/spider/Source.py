# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# 数据源配置
from enum import Enum, unique


@unique
class Source(Enum):
    Netease_Cloud_Music = 'netease'
    QQ_Music = 'tencent'
    # Migu_Music = 'migu'
    KuGou_Music = 'kugou'
    # Baidu_Music = 'baidu'
