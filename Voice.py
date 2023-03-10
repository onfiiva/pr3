import speech_recognition as sr
import pyttsx3
import Main
import Registration as registr
import Authorization 
import time
def Voicemethod(place, phone_number, password):
    print("Проверка на робота.\n"
          "Скажите 'Привет'\n")
    #r = sr.Recognizer()
    #with sr.Microphone() as source:
    #    audio = r.listen(source, 5)
    #    order = r.recognize_google(audio, language="ru-ru")

    exit = int(input())
    if exit == 0:
        if place == 0:
            registr.Regss(phone_number, password)
        else:
            Authorization.Auth(phone_number, password)

    #if (order == "Привет"):
    #    print(order)
    #    engine = pyttsx3.init()
    #    engine.say(order)
    #    engine.runAndWait()
    #    if place == 0:
    #        registr.Regss(phone_number, password)
    #    else:
    #        Authorization.Auth(phone_number, password)
    #else:
    #    print("Вы не прошли проверку на робота.\n")
    #    time.sleep(2)
    #    Main.main()