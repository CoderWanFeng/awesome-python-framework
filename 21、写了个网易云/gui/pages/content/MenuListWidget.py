# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import *

from gui.components.content.MenuButton import MenuButton, pyqtSignal
from gui.pages.content.MenuType import MenuType


class MenuListWidget(QWidget):
    WINDOW_MIN_WIDTH = 243

    # 菜单列表中的所有列表
    components = []

    itemClicked = pyqtSignal(int)

    originIndex = -1

    def __init__(self):
        super(MenuListWidget, self).__init__()

        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        self.setContentsMargins(0, 0, 0, 0)

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """
            QListWidget{
                border:none;
            }
            QPushButton{
                border:none;
                /*background:#F6F6F7;*/
                height:45px;
                font-size:20px;
                /*font-weight:bold;*/
                text-align:left;
                padding-left:5px;
            }
            QLabel{
                padding-left:5px;
                color:#999999;
            }
        """
        self.setStyleSheet(style)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        findMusic = MenuButton(MenuType.FIND_MUSIC.value, '发现音乐')
        self.layout.addWidget(findMusic)

        video = MenuButton(MenuType.VIDEO.value, '统计')
        self.layout.addWidget(video)

        myDevice = MenuButton(MenuType.MY_DEVICE.value, '我的设备')  # mobile
        self.layout.addWidget(myDevice)

        myMusic = QLabel('我的音乐')  # music
        myMusic.setFixedHeight(45)
        self.layout.addWidget(myMusic)

        home = MenuButton(MenuType.HOME.value, "本地音乐", 'home')
        self.layout.addWidget(home)

        download = MenuButton(MenuType.DOWNLOAD.value, "下载管理", 'download')
        self.layout.addWidget(download)

        recent = MenuButton(MenuType.RECENT.value, "最近播放", 'ravelry')
        self.layout.addWidget(recent)

        collect = MenuButton(MenuType.COLLECT.value, "我的收藏", 'heart')
        self.layout.addWidget(collect)

        self.layout.addStretch(1)

        # 添加itemClick事件
        for i in range(self.layout.count() - 1):
            component = self.layout.itemAt(i).widget()
            if isinstance(component, MenuButton):
                component.click.connect(self.setCurentIndex)
                self.components.append(component)

    # 根据index查找组件
    def indexAt(self, index):
        for component in self.components:
            if component.getIndex() == index:
                return component

    def resetComponents(self):
        for component in self.components:
            component.setSelected(False)

    def setCurentIndex(self, index):
        if self.originIndex != index:
            self.originIndex = index
            self.resetComponents()
            self.indexAt(index).setSelected(True)
            self.itemClicked.emit(index)

    def setCurrentIndexI(self, index):
        self.resetComponents()
        self.indexAt(index).setSelected(True)
