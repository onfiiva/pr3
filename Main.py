from os import system, name
import time
import maskpass
import Voice
import smtplib as smtp
import random

def mainwindow():
    _ = system('cls')
    
    try:
        enter = int(input("Добро пожаловать к Ашоту! \n"
        "Выберите функцию: \n"
        "1 - Регистрация\n"
        "2 - Авторизация\n"
        "3 - Выйти\n"))
    except (KeyboardInterrupt, ValueError):
        print("Введены неверные данные\n")
        time.sleep(2)
        mainwindow()
    if (enter > 0 and enter <= 3):
        match enter:
            case 1:
                print("Регистрация у Ашота\n")
                
                email = input("Введите почту\n")
                
                if (not ("@" and ".") in email):
                    print("Неверно введена почта.")
                    time.sleep(2)
                    mainwindow()
                
                
                #Посыл кода на почту
                smtpEmail = "test_test23r43@mail.ru"
                code = random.randint(100,999)
                smptObj = smtp.SMTP("smtp.mail.ru", 587)
                smptObj.starttls()
                smptObj.login(smtpEmail, "m7x9NpBJaHR7mm12Hntu")
                smptObj.sendmail(smtpEmail, email, f"Your code {code}")
                smptObj.quit()

                try:
                    confirmCode = int(input("Вам на почту выслан код подтверждения.\n"
                      "Введите его\n"))
                except ValueError:
                    print("Введены неверные данные")
                    time.sleep(2)
                    mainwindow()

                if code == confirmCode:

                    password = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                    confirmPassword = maskpass.askpass(prompt="Подтвердите пароль: \n", mask="*")
                    if (password == confirmPassword):
                        place = 0
                        Voice.Voicemethod(place, email, password)
                    else:
                        print("Пароли не совпадают. Попробуйте заново.")
                        mainwindow()
                else:
                    print("Неверный код.")
                    time.sleep(2)
                    mainwindow()
                
            case 2:
                print("Авторизация у Ашота")
                email = input("Введите почту \n")

                if (not ("@" and ".") in email):
                    print("Неверно введена почта.")
                    time.sleep(2)
                    mainwindow()

                #Посыл кода на почту
                smtpEmail = "test_test23r43@mail.ru"
                code = random.randint(100,999)
                smptObj = smtp.SMTP("smtp.mail.ru", 587)
                smptObj.starttls()
                smptObj.login(smtpEmail, "m7x9NpBJaHR7mm12Hntu")
                smptObj.sendmail(smtpEmail, email, f"Your code {code}")
                smptObj.quit()

                try:
                    confirmCode = int(input("Вам на почту выслан код подтверждения.\n"
                      "Введите его\n"))
                except ValueError:
                    print("Введены неверные данные")
                    time.sleep(2)
                    mainwindow()
                
                if code == confirmCode:
                    password = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                    place = 1
                    Voice.Voicemethod(place, email, password)
                else:
                    print("Неверный код.")
                    time.sleep(2)
                    mainwindow()
            case 3:
                print("Сворачиваем лавочку...\n")
                time.sleep(2)
                exit()
            case _:
                mainwindow()
    else:
        print("Неправильный ввод")
        time.sleep(1)
        mainwindow()
mainwindow()