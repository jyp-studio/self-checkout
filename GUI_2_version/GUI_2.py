#Ptqt5 設定
from msilib.schema import Font
import sys
import time
import cv2

from start_ui import *
from Main_ui import *

from PyQt5.QtWidgets import QApplication, QWidget,QDesktopWidget
from PyQt5.QtCore import pyqtSlot,QTimer
from PyQt5.QtGui import QImage,QPixmap
a=str('appel\nball\ncook') #自訂字串
#起始畫面的基本設定
class StartWindow(QWidget,Ui_Start):
    def __init__(self):

        super(StartWindow,self).__init__()
        self.setupUi(self)
        
        ###取得螢幕大小並使GUI置中
        screen= QDesktopWidget().screenGeometry()
        #print(screen)
        size= self.geometry()
        #print(size)
        self.move((screen.width()- size.width()) / 2, (screen.height() - size.height()) / 2)
        ###取得螢幕大小並使GUI置中
        
        
        
#主畫面的設定及書寫      
class MainWindow(QWidget,Ui_Main):
    def __init__(self):

        super(MainWindow,self).__init__()
        self.setupUi(self)
        
        ###取得螢幕大小並使GUI置中
        screen= QDesktopWidget().screenGeometry()
        #print(screen)
        size= self.geometry()
        #print(size)
        self.move((screen.width()- size.width()) / 2, (screen.height() - size.height()) / 2)
        

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam) #連結筆電攝影機的功能
        # set control_bt callback clicked  function
        self.control_bt.clicked.connect(self.controlTimer) #按下start後呼叫controlTimer 這支程式
        
    # view camera #這邊是在抓取攝影機的資料 有關於筆電鏡頭的資料
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
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
            # create video capture
            self.cap = cv2.VideoCapture(0) #啟動鏡頭
            # start timer
            self.timer.start(20)
            # update control_bt text
            #按下start 開始啟動 這邊可以做啟動後要的程式書寫
            #SetText("裡面放要給的值")
            self.control_bt.setText("Stop")
            self.Name.setText(a) #把字串放入
            self.Price.setText("start")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            #按下stop 鏡頭會暫停 這邊可以做關閉後要的程式書寫
            #可能是要做資料傳輸google sheet 回傳庫存以及將抓到的物件印在GUI上
            self.control_bt.setText("Start")
            self.Name.setText("stop")
            self.Price.setText("stop")
    
        


if __name__=="__main__":
    app=QApplication(sys.argv)
    
    Start=StartWindow()
    Main=MainWindow()
    
    Start.show()
    Start_Button=Start.Start_Button
    Start_Button.clicked.connect(Main.show)
    
    sys.exit(app.exec_())