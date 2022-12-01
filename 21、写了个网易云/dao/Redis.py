# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import os
import shelve

from gui.utils.Path import getPwd


class Redis():
    # 配置文件名称
    name = 'setting'

    def __init__(self):
        self.path = getPwd() + os.sep + self.name
        self.load()

    # 装载数据
    def load(self):
        db = shelve.open(self.path)
        try:
            self.redis = db['redis']
        except:
            self.redis = {}
        finally:
            db.close()

    # 设置值
    def setValue(self, key, value):
        self.redis[key] = value

    # 获取值,若不存在,则可设置默认值
    def getValue(self, key, default):
        value = self.redis.get(key)
        if value != None:
            return value
        else:
            self.redis[key] = default
            return default

    # 持久化 程序关闭时调用
    def serialize(self):
        db = shelve.open(self.path, writeback=True)
        db['redis'] = self.redis
        db.close()


redis = Redis()
