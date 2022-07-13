import io
import time
import datetime
import requests

import tkinter
import tkinter.font as tkFont

from PIL import Image
import PIL.Image, PIL.ImageTk

import os

session = requests.Session()

LINE_KEY = "fAf1bFGa2-3np-NztbgltNCQfj3ew3ha6gx7PwBm9IQ"
LINE_EVENT = "sendLine"
SHEETS_KEY = "None"
SHEETS_EVENT = "None"

class App:
    def __init__(self, window, window_title, video_source_0=0):
        self.window = window
        self.window.title(window_title)
        self.window.geometry('500x570')
        self.window.resizable(False, False)

        self.LINE_event_name = LINE_EVENT
        self.LINE_key = LINE_KEY

        self.SHEETS_event_name = SHEETS_EVENT
        self.SHEETS_key = SHEETS_KEY 

        self.Start_flag = 0

        self.fontStyle = tkFont.Font(size=30)
        self.header_label = tkinter.Label(window, text='雲端訊息傳輸 GUI設計',font=self.fontStyle)
        self.header_label.place(x=1, y=5, width=500, height=40)

        # 建立日期與時間內容資訊標題
        self.fontStyle = tkFont.Font(size=12)
        self.date_label = tkinter.Label(window, text='日期', bg="blue", fg="yellow", font=self.fontStyle)
        self.date_label.place(x=60, y=50, width=189, height=24)

        self.fontStyle = tkFont.Font(size=12)
        self.time_label = tkinter.Label(window, text='時間', bg="blue", fg="yellow", font=self.fontStyle)
        self.time_label.place(x=254, y=50, width=189, height=24)

        # 設定訊息發送選項框架
        self.Message_Option = tkinter.Frame(window, width=160, height=100, bd=1, relief="sunken")
        self.Message_Option.place(x=10, y=150)

        # 設定發送Line訊息 
        self.Line_chkValue = tkinter.BooleanVar() 
        self.Line_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Line_check = tkinter.Checkbutton(self.Message_Option,
                                              text='Send Line Message',
                                              font=self.fontStyle, var=self.Line_chkValue) 
        self.Line_check.grid(column=0, row=0, sticky=tkinter.W)

        # 設定發送 Google Sheets訊息
        self.Sheets_chkValue = tkinter.BooleanVar() 
        self.Sheets_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Sheets_check = tkinter.Checkbutton(self.Message_Option,
                                              text='Send Google Sheets Value',
                                              font=self.fontStyle, var=self.Sheets_chkValue) 
        self.Sheets_check.grid(column=0, row=1, sticky=tkinter.W)

        # 設定發送日期選項框架
        self.Date_Option = tkinter.Frame(window, width=160, height=400, bd=1, relief="sunken")
        self.Date_Option.place(x=10, y=250)

        # 設定發送星期日
        self.Sunday_chkValue = tkinter.BooleanVar() 
        self.Sunday_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Sunday_check = tkinter.Checkbutton(self.Date_Option,
                                              text='星期日',
                                              font=self.fontStyle, var=self.Sunday_chkValue) 
        self.Sunday_check.grid(column=0, row=0, sticky=tkinter.W)
        
        # 設定發送星期一
        self.Monday_chkValue = tkinter.BooleanVar() 
        self.Monday_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Monday_check = tkinter.Checkbutton(self.Date_Option,
                                              text='星期一',
                                              font=self.fontStyle, var=self.Monday_chkValue) 
        self.Monday_check.grid(column=0, row=1, sticky=tkinter.W)

        # 設定發送星期二
        self.Tuesday_chkValue = tkinter.BooleanVar() 
        self.Tuesday_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Tuesday_check = tkinter.Checkbutton(self.Date_Option,
                                              text='星期二',
                                              font=self.fontStyle, var=self.Tuesday_chkValue) 
        self.Tuesday_check.grid(column=0, row=2, sticky=tkinter.W)

        # 設定發送星期三
        self.Wednesday_chkValue = tkinter.BooleanVar() 
        self.Wednesday_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Wednesday_check = tkinter.Checkbutton(self.Date_Option,
                                              text='星期三',
                                              font=self.fontStyle, var=self.Wednesday_chkValue) 
        self.Wednesday_check.grid(column=0, row=3, sticky=tkinter.W)

        # 設定發送星期四
        self.Thursday_chkValue = tkinter.BooleanVar() 
        self.Thursday_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Thursday_check = tkinter.Checkbutton(self.Date_Option,
                                              text='星期四',
                                              font=self.fontStyle, var=self.Thursday_chkValue) 
        self.Thursday_check.grid(column=0, row=4, sticky=tkinter.W)

        # 設定發送星期五
        self.Friday_chkValue = tkinter.BooleanVar() 
        self.Friday_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Friday_check = tkinter.Checkbutton(self.Date_Option,
                                              text='星期五',
                                              font=self.fontStyle, var=self.Friday_chkValue) 
        self.Friday_check.grid(column=0, row=5, sticky=tkinter.W)

        # 設定發送星期六
        self.Saturday_chkValue = tkinter.BooleanVar() 
        self.Saturday_chkValue.set(True)
        self.fontStyle = tkFont.Font(size=14) 
        self.Saturday_check = tkinter.Checkbutton(self.Date_Option,
                                              text='星期六',
                                              font=self.fontStyle, var=self.Saturday_chkValue) 
        self.Saturday_check.grid(column=0, row=6, sticky=tkinter.W)


        #設定起始時間框架
        self.Time_Option = tkinter.Frame(window, width=50, height=10, bd=1, relief="sunken")
        self.Time_Option.place(x=120, y=250)
        self.fontStyle = tkFont.Font(size=14)
        self.Label_Start = tkinter.Label(self.Time_Option, text='起始時間', font=self.fontStyle)
        self.Label_Start.grid(column=0, row=0, sticky=tkinter.W)        
        
        self.fontStyle = tkFont.Font(size=14)
        self.Label_Hour = tkinter.Label(self.Time_Option, text='時', font=self.fontStyle)
        self.Label_Hour.grid(column=0, row=1, sticky=tkinter.E)        
        self.Entry_Hour = tkinter.Entry(self.Time_Option, width=5, font=self.fontStyle)
        self.Entry_Hour.grid(column=1, row=1)

        self.fontStyle = tkFont.Font(size=14)
        self.Label_Min = tkinter.Label(self.Time_Option, text='分', font=self.fontStyle)
        self.Label_Min.grid(column=0, row=2, sticky=tkinter.E)        
        self.Entry_Min = tkinter.Entry(self.Time_Option, width=5, font=self.fontStyle)
        self.Entry_Min.grid(column=1, row=2)

        self.fontStyle = tkFont.Font(size=14)
        self.Label_Sec = tkinter.Label(self.Time_Option, text='秒', font=self.fontStyle)
        self.Label_Sec.grid(column=0, row=3, sticky=tkinter.E)        
        self.Entry_Sec = tkinter.Entry(self.Time_Option, width=5, font=self.fontStyle)
        self.Entry_Sec.grid(column=1, row=3)


        #設定時間間隔框架
        self.Interval_Option = tkinter.Frame(window, width=50, height=10, bd=1, relief="sunken")
        self.Interval_Option.place(x=120, y=360)
        self.fontStyle = tkFont.Font(size=14)
        self.Label_Interval = tkinter.Label(self.Interval_Option, text='間隔時間', font=self.fontStyle)
        self.Label_Interval.grid(column=0, row=0, sticky=tkinter.W)        
        
        self.fontStyle = tkFont.Font(size=14)
        self.Label_Hour = tkinter.Label(self.Interval_Option, text='時', font=self.fontStyle)
        self.Label_Hour.grid(column=0, row=1, sticky=tkinter.E)        
        self.Interval_Hour = tkinter.Entry(self.Interval_Option, width=5, font=self.fontStyle)
        self.Interval_Hour.grid(column=1, row=1)

        self.fontStyle = tkFont.Font(size=14)
        self.Label_Min = tkinter.Label(self.Interval_Option, text='分', font=self.fontStyle)
        self.Label_Min.grid(column=0, row=2, sticky=tkinter.E)        
        self.Interval_Min = tkinter.Entry(self.Interval_Option, width=5, font=self.fontStyle)
        self.Interval_Min.grid(column=1, row=2)

        self.fontStyle = tkFont.Font(size=14)
        self.Label_Sec = tkinter.Label(self.Interval_Option, text='秒', font=self.fontStyle)
        self.Label_Sec.grid(column=0, row=3, sticky=tkinter.E)        
        self.Interval_Sec = tkinter.Entry(self.Interval_Option, width=5, font=self.fontStyle)
        self.Interval_Sec.grid(column=1, row=3)

        #設定ON/OFF按鈕框架
        self.SW_Option = tkinter.Frame(window, width=50, height=10, bd=1, relief="sunken")
        self.SW_Option.place(x=10, y=500)

        # 設定ON按鈕的樣式與位置
        self.fontStyle = tkFont.Font(size=20)
        self.ON_button = tkinter.Button(self.SW_Option, text="啟動", state=tkinter.NORMAL,
                                        font=self.fontStyle, bg='red', command=self.ON_Option)
        self.ON_button.grid(column=0, row=0)
        
        # 設定OFF按鈕的樣式與位置
        self.fontStyle = tkFont.Font(size=20)
        self.OFF_button = tkinter.Button(self.SW_Option, text="停止", state=tkinter.DISABLED,
                                         font=self.fontStyle, bg='gainsboro', command=self.OFF_Option)
        self.OFF_button.grid(column=1, row=0)

        # 建立識別狀況框架區
        self.attend_status_frame = tkinter.Frame(window)
        self.attend_status_frame.place(x=280, y=130, width=200, height=420)
        self.update_attend_status()

        self.update_clock()

        self.hint_flag = 0

        self.window.mainloop()

    def ON_Option(self):
        print('ON')
        self.ON_button['state'] = tkinter.DISABLED
        self.ON_button['bg'] = 'gainsboro'
        self.OFF_button['state'] = tkinter.NORMAL
        self.OFF_button['bg'] = 'red'
        self.delay_time = int(self.Interval_Hour.get())*3600 + int(self.Interval_Min.get())*60 + int(self.Interval_Sec.get())
        print(self.delay_time)

    def OFF_Option(self):
        print('OFF')
        self.OFF_button['state'] = tkinter.DISABLED
        self.OFF_button['bg'] = 'gainsboro'
        self.ON_button['state'] = tkinter.NORMAL
        self.ON_button['bg'] = 'red'
        self.Start_flag = 0

    def update_attend_status(self):
        # 建立出席狀況區框架裡的卷軸功能
        sb_status = tkinter.Scrollbar(self.attend_status_frame)
        sb_status.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # 建立一個出席狀況清單
        fontStyle = tkFont.Font(size=16)
        # 將選項框在Y軸的動作與捲軸進行關聯
        self.attend_status_listbox = tkinter.Listbox(self.attend_status_frame, height=8, 
            yscrollcommand = sb_status.set, font=fontStyle)  
        self.attend_status_listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    def add_status_list(self):
        self.name=''
        # attend_status_value = self.attend_value.get()
        self.face()
        if (self.name != ''):
            name_value = self.name
            self.attend_status_listbox.insert(tkinter.END, name_value + ' ' + 
                time.strftime("%H") + ':' + time.strftime("%M") + ':' + time.strftime("%S"))

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        now_date = time.strftime("%Y/%m/%d")
    
        self.week_day_dict = {
            0 : '(星期一)',
            1 : '(星期二)',
            2 : '(星期三)',
            3 : '(星期四)',
            4 : '(星期五)',
            5 : '(星期六)',
            6 : '(星期天)',
        }
        fontStyle = tkFont.Font(size=14)
        self.day = datetime.date.today().weekday()
        now_date_info = tkinter.Label(text=now_date + ' ' + self.week_day_dict[self.day], 
            bg="red", fg='yellow', font=fontStyle)
        now_date_info.place(x=60, y=80, width=189, height=32)

        now_time = time.strftime("%H:%M:%S")
        fontStyle = tkFont.Font(size=14)
        now_time_info = tkinter.Label(text=now_time, bg="red", fg='yellow', font=fontStyle)
        now_time_info.place(x=254, y=80, width=189, height=32)

        now_hr=int(time.strftime("%H"))
        now_min=int(time.strftime("%M"))
        now_sec=int(time.strftime("%S"))


        if ((self.ON_button['state'] == 'disabled') and
            (now_hr == int(self.Entry_Hour.get())) and
            (now_min == int(self.Entry_Min.get())) and
            (now_sec == int(self.Entry_Sec.get()))
            ):
            print('Start for Send Messages')
            self.IFTTT_work('啟動傳輸',now_time,'曾俊霖')
            self.PRE_SECOND = int(time.time())
            self.Start_flag = 1

        if ((self.ON_button['state'] == 'disabled') and
            (self.Start_flag == 1)
            ):
            self.POST_SECOND = int(time.time())
            if (self.POST_SECOND - self.PRE_SECOND) >= self.delay_time :
                print('Send: '+str(now_time))
                self.PRE_SECOND = int(time.time())
                self.IFTTT_work('用藥提醒', now_time,'曾俊霖')
        
        self.window.after(500, self.update_clock)

    def IFTTT_work(self,value1,value2,value3):
        # Your IFTTT LINE_URL with event name, key and json parameters (values)
        self.LINE_URL='https://maker.ifttt.com/trigger/' + self.LINE_event_name + '/with/key/' + self.LINE_key
        self.r = session.post(self.LINE_URL, params={"value1":value1,"value2":value2,"value3":value3})

        # Your IFTTT SHEETS_URL with event name, key and json parameters (values)
        self.SHEETS_URL='https://maker.ifttt.com/trigger/' + self.SHEETS_event_name + '/with/key/' + self.SHEETS_key
        self.r = session.post(self.SHEETS_URL, params={"value1":value1,"value2":value2,"value3":value3})


# Create a window and pass it to the Application object
App(tkinter.Tk(), '雲端訊息傳輸 GUI設計')
