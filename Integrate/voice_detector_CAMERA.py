from importlib.resources import path
import speech_recognition as sr
import time
import threading
import re

import cv2
import argparse
import os

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

DELAY = 1.0
COUNTDOWN = 3

def take_picture(video, picture_path):
    # 選擇攝影機
    cap = cv2.VideoCapture(video)
    # 設定影像的尺寸大小
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    PRE_SECOND = time.time()
    count = 0
    while(count <= COUNTDOWN):
        ret, frame_src = cap.read()

        cv2.putText(frame_src,
            str(COUNTDOWN - count),
            (int(CAMERA_WIDTH*0.9),int(CAMERA_HEIGHT*0.08)),
            cv2.FONT_HERSHEY_SIMPLEX,1,
            (0,255,0),6,cv2.LINE_AA)
        cv2.putText(frame_src,
            str(COUNTDOWN - count),
            (int(CAMERA_WIDTH*0.9),int(CAMERA_HEIGHT*0.08)),
            cv2.FONT_HERSHEY_SIMPLEX,1,
            (0,0,0),2,cv2.LINE_AA)

        cv2.imshow('Standing by ....',frame_src)

        POST_SECOND = time.time()
        if POST_SECOND - PRE_SECOND >= DELAY :    
            count = count + 1
            PRE_SECOND = time.time()

        cv2.waitKey(1)

    ret, frame_src = cap.read()
    cv2.imshow('Picture',frame_src)
    cv2.waitKey(1)
    time.sleep(1)
    cv2.imwrite(picture_path + '/OUT' + str(int(time.time()))+'.jpg',frame_src)

    # 釋放攝影機
    cap.release() 
    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()

def main():    
    try:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument(
            '--path', help='File path of *.jpg file.', required=True)
        parser.add_argument(
            '--video', help='Camera number.', required=True, type=int)
        args = parser.parse_args()

        folder = os.path.exists(args.path)

        #判斷結果
        if not folder:
            #如果不存在，則建立新目錄
            os.makedirs(args.path)
            print('資料夾 ' + args.path + ' 建立成功')

        else:
            #如果目錄已存在，則不建立，提示目錄已存在
            print('資料夾 ' + args.path +' 已存在')

        while True:
            r = sr.Recognizer()
            m = sr.Microphone()
            m.RATE = 44100
            m.CHUNK = 512

            print("A moment of silence, please...")
            with m as source:
                r.adjust_for_ambient_noise(source)
                if (r.energy_threshold < 2000):
                    r.energy_threshold = 2000
                print("Set minimum energy threshold to {}".format(r.energy_threshold))

                print("Say something!")
                audio = r.listen(source)
                print("Got it! Now to recognize it...")

                speechtext = r.recognize_google(audio,language='zh',show_all=True) #Load Google Speech Recognition API
                print(type(speechtext)) #dict

                if len(speechtext) == 0:
                    pass
                else:
                    speechtext = speechtext['alternative'][0]['transcript']
                    speechtext = speechtext.replace(' ', '')
                    print("You said: " + speechtext)

                    if re.search('\s*照相\s*',speechtext):
                        take_picture(args.video, args.path)#<--------------------------------------------------------------------------
                        print('已拍照') 

                    elif re.search('\s*開始程式\s*',speechtext):
                        print('開始程式運作')
                        return 1 #回傳個flag = 1 表開始-------------

                    elif re.search('\s*結束程式\s*',speechtext):
                        print('結束程式運作')
                        return 2 #回傳個flag = 2 表結束--------------
                        break

    except KeyboardInterrupt:
        print("Quit")

if __name__ == '__main__':
  main()