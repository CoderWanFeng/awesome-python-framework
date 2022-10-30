

import sys

import Weather

from PyQt5.QtWidgets import QApplication, QDialog

import requests

class MainDialog(QDialog):

    def __init__(self, parent=None):

        super(QDialog, self).__init__(parent)

        self.ui = Weather.Ui_Dialog()

        self.ui.setupUi(self)

    def queryWeather(self):

        cityName = self.ui.comboBox.currentText()

        cityCode = self.getCode(cityName)

        r = requests.get(

            "https://restapi.amap.com/v3/weather/weatherInfo?key=f4fd5b287b6d7d51a3c60fee24e42002&city={}".format(

                cityCode))

        if r.status_code == 200:

            data = r.json()['lives'][0]

            weatherMsg = '城市：{}\n天气：{}\n温度：{}\n风向：{}\n风力：{}\n湿度：{}\n发布时间：{}\n'.format(

                data['city'],

                data['weather'],

                data['temperature'],

                data['winddirection'],

                data['windpower'],

                data['humidity'],

                data['reporttime'],

            )

        else:

            weatherMsg = '天气查询失败，请稍后再试！'

        self.ui.textEdit.setText(weatherMsg)

    def getCode(self, cityName):

        cityDict = {"北京": "110000",

                    "苏州": "320500",

                    "上海": "310000"}

        return cityDict.get(cityName, '101010100')

    def clearText(self):

        self.ui.textEdit.clear()

if __name__ == '__main__':

    myapp = QApplication(sys.argv)

    myDlg = MainDialog()

    myDlg.show()

    sys.exit(myapp.exec_())