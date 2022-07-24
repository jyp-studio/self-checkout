import speech_recognition as sr
import time
import threading
import re
import requests

def main():
    try:
        while True:
            r = sr.Recognizer()
            m = sr.Microphone()
            m.RATE = 44100
            m.CHUNK = 512

            print("你好，請說開始結帳")
            with m as source:
                r.adjust_for_ambient_noise(source)
                if (r.energy_threshold < 2000):
                    r.energy_threshold = 2000
                print("Set minimum energy threshold to {}".format(r.energy_threshold))

                print("再說一次!")
                audio = r.listen(source)
                print("辨識中")

                speechtext = r.recognize_google(audio,language='zh',show_all=True) #Load Google Speech Recognition API
                print(type(speechtext)) #dict
                if len(speechtext) == 0:
                    pass
                else:
                    speechtext = speechtext['alternative'][0]['transcript']
                    speechtext = speechtext.replace(' ', '')
                    print("你說: " + speechtext)
                    if re.search('\s*開始結帳\s*',speechtext):
                        print('開始結帳')
                        return 1
                         # 這裡需要有程式連到影像辨識

                    elif re.search('\s*開始程式\s*',speechtext):
                        print('開始程式運作')
                        return 1 #回傳個flag = 1 表開始-------------

                    elif re.search('\s*結束程式\s*',speechtext):
                        print('結束程式運作')
                        return 2 #回傳個flag = 2 表結束--------------
                    
                    elif re.search('\s*你好\s*',speechtext):
                        print('你好')

                    elif re.search('\s*結束\s*',speechtext):
                        print('結束')

    except KeyboardInterrupt:
        print("Quit")