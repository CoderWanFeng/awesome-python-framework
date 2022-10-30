
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")

        Dialog.resize(600, 600)

        self.groupBox = QtWidgets.QGroupBox(Dialog)

        self.groupBox.setGeometry(QtCore.QRect(30, 20, 551, 511))

        self.groupBox.setObjectName("groupBox")

        self.label_2 = QtWidgets.QLabel(self.groupBox)

        self.label_2.setGeometry(QtCore.QRect(20, 30, 31, 16))

        self.label_2.setObjectName("label_2")

        self.comboBox = QtWidgets.QComboBox(self.groupBox)

        self.comboBox.setGeometry(QtCore.QRect(70, 30, 87, 22))

        self.comboBox.setObjectName("comboBox")

        self.comboBox.addItem("")

        self.comboBox.addItem("")

        self.comboBox.addItem("")

        self.textEdit = QtWidgets.QTextEdit(self.groupBox)

        self.textEdit.setGeometry(QtCore.QRect(20, 70, 491, 411))

        self.textEdit.setObjectName("textEdit")

        self.queryBtn = QtWidgets.QPushButton(Dialog)

        self.queryBtn.setGeometry(QtCore.QRect(490, 560, 93, 28))

        self.queryBtn.setObjectName("queryBtn")

        self.clearBtn = QtWidgets.QPushButton(Dialog)

        self.clearBtn.setGeometry(QtCore.QRect(30, 560, 93, 28))

        self.clearBtn.setObjectName("clearBtn")

        self.retranslateUi(Dialog)

        self.clearBtn.clicked.connect(Dialog.clearText)

        self.queryBtn.clicked.connect(Dialog.queryWeather)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate

        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.groupBox.setTitle(_translate("Dialog", "城市天气预报"))

        self.label_2.setText(_translate("Dialog", "城市"))

        self.comboBox.setItemText(0, _translate("Dialog", "北京"))

        self.comboBox.setItemText(1, _translate("Dialog", "苏州"))

        self.comboBox.setItemText(2, _translate("Dialog", "上海"))

        self.queryBtn.setText(_translate("Dialog", "查询"))

        self.clearBtn.setText(_translate("Dialog", "清空"))

