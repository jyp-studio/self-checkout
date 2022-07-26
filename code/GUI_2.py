# Ptqt5 設定
import sys
from turtle import delay
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
from start_ui import *
from Main_ui import *
import voice_detector0720
import GetPrice
import time

a = str('appel\nball\ncook')  # 自訂字串
# 起始畫面的基本設定

class StartWindow(QWidget, Ui_Start):
    def __init__(self):

        super(StartWindow, self).__init__()
        self.setupUi(self)

        # 取得螢幕大小並使GUI置中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        # 取得螢幕大小並使GUI置中


# 主畫面的設定及書寫
class MainWindow(QWidget, Ui_Main):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 取得螢幕大小並使GUI置中
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)  # 連結筆電攝影機的功能
        # set control_bt callback clicked  function
        # 按下start後呼叫controlTimer 這支程式

        self.control_bt.clicked.connect(self.controlTimer)
        #self.controlTimer()

    def viewCam(self): #改成抓取圖片並顯示
        # read image in BGR format
        image = cv2.imread('output.png')
        image = cv2.resize(image,(571, 731))
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.camera.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer #按下start或stop 會做甚麼樣的動作
    def controlTimer(self):
        
        # if timer is stopped
        if not self.timer.isActive():
            print("loading...")
            self.control_bt.setText("Stop")
            self.camera.setText("loading...")
            self.Name.setText("loading...")
#            delay(10)
            # start timer
            self.timer.start(20)
            # update control_bt text
            # 按下start 開始啟動 這邊可以做啟動後要的程式書寫

            ll = voice_detector0720.main()
            SoldData, InventoryData = GetPrice.gsheet(ll)
            a = ""
            price = ""
            for i in range(0,len(ll)):
                a = a + ll[i]
                a = a + "\n"
                price = price + str(SoldData[ll[i]])
                price = price + "\n"
            total = str(SoldData["Total"])
            
            self.control_bt.setText("Stop")
            self.Name.setText(a)  # 把字串放入
            self.Price.setText(price)
            self.total.setText(total)
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # update control_bt text
            # 按下stop 鏡頭會暫停 這邊可以做關閉後要的程式書寫
            self.control_bt.setText("Start")
            self.Name.setText('name')
            self.Price.setText('price')
            self.total.setText('total')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Start = StartWindow()
    Main = MainWindow()
    Start.show()
    Start_Button = Start.Start_Button
    Start_Button.clicked.connect(Main.show)
    sys.exit(app.exec_())