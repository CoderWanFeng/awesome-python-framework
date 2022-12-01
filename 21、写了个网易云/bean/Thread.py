# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
# QThread 封装 适配
from PyQt5.QtCore import QThread, pyqtSignal


class Thread(QThread):
    finish = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super(Thread, self).__init__()

        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.finish.emit(result)
