import speech_recognition as sr
import time
import threading
import re
import requests

event_name_line = 'sendLine'
key = 'fAf1bFGa2-3np-NztbgltNCQfj3ew3ha6gx7PwBm9IQ'
URL_line = 'https://maker.ifttt.com/trigger/' + \
    event_name_line + '/with/key/' + key

session = requests.Session()

AC = 0
FAN = 0
LIGHT = 0

try:

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

            # Load Google Speech Recognition API
            speechtext = r.recognize_google(
                audio, language='zh', show_all=True)
            print(type(speechtext))  # dict

            if len(speechtext) == 0:
                pass
            else:
                speechtext = speechtext['alternative'][0]['transcript']
                speechtext = speechtext.replace(' ', '')
                print("You said: " + speechtext)

                if re.search('\s*開冷氣\s*', speechtext):
                    print('冷氣機已開啟')
                    AC = 1

                elif re.search('\s*關冷氣\s*', speechtext):
                    print('冷氣機已關閉')
                    AC = 0

                elif re.search('\s*開電扇\s*', speechtext):
                    print('電風扇已開啟')
                    FAN = 1

                elif re.search('\s*關電扇\s*', speechtext):
                    print('電風扇已關閉')
                    FAN = 0

                elif re.search('\s*開電燈\s*', speechtext):
                    print('電燈已開啟')
                    LIGHT = 1

                elif re.search('\s*關電燈\s*', speechtext):
                    print('電燈已關閉')
                    LIGHT = 0

                elif re.search('\s*救命啊\s*', speechtext):
                    print('有人喊救命，趕快處理。')

                    r_line = session.post(
                        URL_line, params={"value1": '緊急事件', "value2": '有人喊救命', "value3": '家裡'})

                elif re.search('\s*失火\s*', speechtext):
                    print('趕快叫消防車119。')

                    r_line = session.post(
                        URL_line, params={"value1": '緊急事件', "value2": '失火了', "value3": '叫119'})

                elif re.search('\s*結束程式\s*', speechtext):
                    print('結束程式運作')
                    break


except KeyboardInterrupt:
    print("Quit")
