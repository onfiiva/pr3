from os import system, name
import time
import phonenumbers
import maskpass
import Reg
import Auth
def main():
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
        main()
    if (enter > 0 and enter <= 3):
        match enter:
            case 1:
                print("Регистрация у Ашота\n")
                phone_number = input("Введите телефон\n")
                try_number = phonenumbers.parse(phone_number, "RU")
                if phonenumbers.is_valid_number(try_number):
                    if ("+" not in phone_number):
                        phone_number = "+" + phone_number
                    code = input("Введите код подтверждения из SMS\n")
                    password = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                    confirmPassword = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                    if (password == confirmPassword):
                        Reg.Reg(phone_number, password)
                    else:
                        print("Пароли не совпадают. Попробуйте заново.")
                        main()
                else:
                    print("Неверно введен номер телефона.")
                    time.sleep(2)
                    main()
                
            case 2:
                print("Авторизация у Ашота")
                phone_number = input("Введите телефон \n")
                password = maskpass.askpass(prompt="Введите пароль: \n", mask="*")
                Auth.Auth(phone_number, password)
            case 3:
                print("Сворачиваем лавочку...\n")
                time.sleep(2)
                exit()
            case _:
                main()
    else:
        print("Неправильный ввод")
        time.sleep(1)
        main()
main()