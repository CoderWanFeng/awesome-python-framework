# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from bean.RecodeStack import recodeStack
from gui.components.content.DisabledButton import DisabledButton
from gui.components.content.HoverButton import HoverButton
from gui.pages.GlobalSignal import globalSignal
from gui.pages.content.MenuType import MenuType


class SearchWidget(QWidget):
    microphoneSignal = pyqtSignal()

    originKeyword = ''
    changeStatus = False

    def __init__(self):
        super(SearchWidget, self).__init__()

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """
        #backward,#forward{
            background-color:#E13E3E;
            width:32px;
            height:32px;
            border-radius:16px;
        }
        #keyword{
            width:162px;
            height:40px;
            border-radius:20px;
            border:none;
            background-color:#E13E3E;
            color:#ffffff;
            padding-left:40px;
        }
        #search{
            color:#FBD9D9; 
        }
        #search:hover{
            color:#ffffff;       
        }
        #microphone{
            width:42px;
            height:42px;
            border-radius:21px;
            background-color:#E13E3E;
        }
        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        self.setLayout(layout)

        self.backward = DisabledButton(iconName='angle-left')
        self.backward.setObjectName("backward")
        layout.addWidget(self.backward)

        self.forward = DisabledButton(iconName='angle-right')
        self.forward.setObjectName("forward")
        layout.addWidget(self.forward)

        self.keyword = QLineEdit()
        self.keyword.setPlaceholderText("搜索")
        self.keyword.setObjectName("keyword")
        layout.addWidget(self.keyword)

        search = HoverButton(self.keyword, iconName='search', cursor=Qt.ArrowCursor)
        search.setObjectName("search")
        search.move(10, 10)

        microphone = HoverButton(iconName='microphone', activeColor='#F8CECE', inActiveColor='#F8CECE')
        microphone.setObjectName("microphone")
        layout.addWidget(microphone)

        QMetaObject.connectSlotsByName(self)

        # 改变 前进后退 按钮 状态
        globalSignal.backwardStatusSignal.connect(self.changeBackwardStatus)
        globalSignal.forwardStatusSignal.connect(self.changeforwardStatus)

    def resetChangeStatus(self):
        self.changeStatus = False

    def changeBackwardStatus(self, status):
        self.backward.setButtonStatus(status)

    def changeforwardStatus(self, status):
        self.forward.setButtonStatus(status)

    def dispatch(self, page):
        if page[0] == MenuType.SEARCH.value:
            globalSignal.keywordSignalI.emit(page[1])
        else:
            globalSignal.pageIndexSignal.emit(page[0])

    @pyqtSlot()
    def on_backward_clicked(self):
        if not self.backward.disabled:
            self.changeStatus = False
            self.dispatch(recodeStack.backward())
            if recodeStack.isBegin():
                self.backward.setButtonStatus(True)
            self.forward.setButtonStatus(False)

    @pyqtSlot()
    def on_forward_clicked(self):
        if not self.forward.disabled:
            self.changeStatus = False
            self.dispatch(recodeStack.forward())
            if recodeStack.isDeadline():
                self.forward.setButtonStatus(True)
            self.backward.setButtonStatus(False)

    @pyqtSlot()
    def on_microphone_clicked(self):
        self.microphoneSignal.emit()

    @pyqtSlot()
    def on_search_clicked(self):
        self.keywordSearch()

    @pyqtSlot()
    def on_keyword_returnPressed(self):
        self.keywordSearch()

    def keywordSearch(self):
        keyword = self.keyword.text()
        if keyword != '' and keyword != self.originKeyword:
            self.originKeyword = keyword
            self.changeStatus = True
            globalSignal.keywordSignal.emit(keyword)

        if self.changeStatus == False:
            self.changeStatus = True
            globalSignal.keywordSignal.emit(keyword)

    def setBackwardButtonStatus(self, disabled):
        self.backward.setButtonStatus(disabled)

    def setForwardButtonStatus(self, disabled):
        self.forward.setButtonStatus(disabled)
