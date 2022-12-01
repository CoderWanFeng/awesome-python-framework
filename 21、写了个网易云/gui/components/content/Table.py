# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
from PyQt5.QtWidgets import *


class Table(QTableWidget):

    def __init__(self, column):
        super(Table, self).__init__()

        self.setStyleSheet("""
            QTableWidget{
                border:none;
            }
        """)

        # 设置列数
        self.setColumnCount(len(column))
        # 设置不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置整行选择
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置不显示垂直标题
        self.verticalHeader().setVisible(False)
        # 设置不显示网格
        self.setShowGrid(False)
        # 设置表头随窗口拉伸
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置表头的高度
        self.horizontalHeader().setFixedHeight(45)
        # 设置单元行的高度
        self.verticalHeader().setDefaultSectionSize(45)
