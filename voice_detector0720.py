import speech_recognition as sr
import re

import OBJECT_FILE_tflite

def main():
    try:
        while True:
            r = sr.Recognizer()
            m = sr.Microphone()
            m.RATE = 44100
            m.CHUNK = 512

            with m as source:
                r.adjust_for_ambient_noise(source)
                if (r.energy_threshold < 2000):
                    r.energy_threshold = 2000
                    
                print("你好，請說開始結帳")
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
                        ll = OBJECT_FILE_tflite.main()
                        return ll

    except KeyboardInterrupt:
        print("Quit")
