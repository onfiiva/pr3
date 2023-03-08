import speech_recognition as sr
import pyttsx3
import Main
import Registration
import Authorization
import time
def Voice(place, phone_number, password):
    print("Проверка на робота.\n"
          "Скажите 'Привет'\n")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, 5)
        order = r.recognize_google(audio, language="ru-ru")

    if (order == "Привет"):
        print(order)
        engine = pyttsx3.init()
        engine.say(order)
        engine.runAndWait()
        if place == 0:
            Registration.Reg(phone_number, password)
        else:
            Authorization.Auth(phone_number, password)
    else:
        print("Вы не прошли проверку на робота.\n")
        time.sleep(2)
        Main.main()