from msilib.schema import Font
import sys
import time

from GUI_ui import *
from PyQt5.QtWidgets import QApplication, QWidget,QDesktopWidget
from PyQt5.QtCore import pyqtSlot

'''
開始結帳函數名稱為:Start_Button
結束結帳函數名稱為:Finish_Button
顯示金額的函數名稱為:money
'''

class MainWindow(QWidget,Ui_Form):
    def __init__(self):

        super(MainWindow,self).__init__()
        self.setupUi(self)
        
        ###取得螢幕大小並使GUI置中
        screen= QDesktopWidget().screenGeometry()
        #print(screen)
        size= self.geometry()
        #print(size)
        self.move((screen.width()- size.width()) / 2, (screen.height() - size.height()) / 2)
        ###取得螢幕大小並使GUI置中
    
    
    #按下開始結帳按鈕的執行程式
    @pyqtSlot()
    def on_Start_Button_clicked(self):
        #按下開始結帳按鈕後要執行的程式從這邊開始寫
        data_in=self.money.setText('5000')
        self.money.setFont(QtGui.QFont("標楷體",48))
        #上面可測試按下按鈕是否能執行程式
        
    #按下結束結帳按鈕的執行程式
    @pyqtSlot()
    def on_Finish_Button_clicked(self):
        #按下結束結帳按鈕後要執行的程式從這邊開始寫
        data_in=self.money.setText('1000')
        self.money.setFont(QtGui.QFont("標楷體",48))
        #上面可測試按下按鈕是否能執行程式
        
           
    



if __name__=="__main__":
    app=QApplication(sys.argv)
   
    window=MainWindow()
    window.show()
    
    sys.exit(app.exec_())