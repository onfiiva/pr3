from os import system, name
import time
import phonenumbers
import maskpass
import Voice

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
                try:
                    inputPhone = int(input("Введите телефон\n+7"))
                except ValueError:
                    print("Неправильно введен номер телефона.")
                    time.sleep(2)
                    mainwindow()
                phone_number = "+7" + str(inputPhone)
                try_number = phonenumbers.parse(phone_number, "RU")
                if phonenumbers.is_valid_number(try_number):
                    if ("+" not in phone_number):
                        phone_number = "+" + phone_number
                else:
                    print("Неверно введен номер телефона.")
                    time.sleep(2)
                    mainwindow()
                password = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                confirmPassword = maskpass.askpass(prompt="Подтвердите пароль: \n", mask="*")
                if (password == confirmPassword):
                    place = 0
                    Voice.Voicemethod(place, phone_number, password)
                else:
                    print("Пароли не совпадают. Попробуйте заново.")
                    mainwindow()
                
            case 2:
                print("Авторизация у Ашота")
                phone_number = input("Введите телефон \n")
                password = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                place = 1
                Voice.Voicemethod(place, phone_number, password)
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