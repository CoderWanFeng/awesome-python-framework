# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.components.content.Table import Table
from gui.components.content.TagWidget import TagWidget

import sys


class MyDeviceWidget(TagWidget):

    def __init__(self, tag):
        super(MyDeviceWidget, self).__init__(tag)

        self.initStyle()
        self.initUI()

    def initStyle(self):
        style = """

        """
        self.setStyleSheet(style)

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.display = QLabel("未检测到设备")
        layout.addWidget(self.display, 0, 0, 1, 2)

        self.checkoutBtn = QPushButton("检测设备")
        self.checkoutBtn.clicked.connect(self.checkout)
        layout.addWidget(self.checkoutBtn, 0, 2)

        self.input = QLineEdit()
        self.input.setPlaceholderText("手机路径")
        self.input.setDisabled(True)
        layout.addWidget(self.input, 1, 0)

        self.insertBtn = QPushButton("添加文件")
        self.insertBtn.clicked.connect(self.insert)
        self.insertBtn.setDisabled(True)
        layout.addWidget(self.insertBtn, 1, 1)

        self.sendBtn = QPushButton("传送")
        self.sendBtn.clicked.connect(self.send)
        self.sendBtn.setDisabled(True)
        layout.addWidget(self.sendBtn, 1, 2)

        headerLabels = ["文件名称"]
        self.table = Table(headerLabels)
        self.table.setHorizontalHeaderLabels(headerLabels)
        layout.addWidget(self.table, 2, 0, 1, 4)

        self.files = []

    # 检测设备
    def checkout(self):
        os.popen('adb connect 127.0.0.1:62001')
        result = os.popen('adb devices')
        if "127.0.0.1:62001	device" in result.read():
            self.display.setText("已检测到设备")
            self.checkoutBtn.setDisabled(True)
            self.input.setDisabled(False)
            self.insertBtn.setDisabled(False)
            self.sendBtn.setDisabled(False)
        else:
            self.display.setText("未检测到设备 请稍后重试！")

    # 添加文件
    def insert(self):
        result = QFileDialog.getOpenFileNames()
        result = result[0]
        length = len(result)
        self.table.setRowCount(self.table.rowCount() + length)
        for index in range(length):
            self.table.setItem(index, 0, QTableWidgetItem(result[index].split('/')[-1]))
        self.files += result

        for i in range(self.table.rowCount()):
            self.table.item(i, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def send(self):
        path = self.input.text()
        if path:
            for file in self.files:
                print(file.split('/')[-1])
                os.system('adb push ' + file + ' ' + path + '/' + file.split('/')[-1])
