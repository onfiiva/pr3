import pyodbc
from os import system, name
import os.path
import time
import Order
import Main
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()
def Users(userId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [User] inner join [Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = '{userId}'"):
         balance = row.Balance_User

    print("Магазин 'У Ашота в кармане'")
    print(f"У вас на счету {balance} рублей.\n")
    try:
        function = int(input("Выберите функцию\n"
        "1 - Заказать блюдо\n"
        "2 - История покупок\n"
        "3 - Карта лояльности\n"
        "4 - Выйти из аккаунта\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Users(userId)

    if function > 0 and function <= 4:
        match function:
            case 1:
                Order.Order(userId)
            case 2:
                UserHistory(userId)
            case 3:
                UserLoyality(userId)
            case 4:
                Main.main()
    else:
        print("Неправильная функция.")
        Users(userId)

def UserHistory(userId):
    print("Собираем историю...")
    time.sleep(2)
    chequeId = []
    countFiles = 0
    for row in cursor.execute(f"select * from [Cheque] where [User_ID] = {userId}"):
        chequeId.append(row.ID_Cheque)
    for id in range(len(chequeId)):
        if (os.path.exists(f'C:\\Users\\kiruk\\Python\\prac3\\Cheques\\Cheque{chequeId[id]}.txt')):
            file = open(f'C:\\Users\\kiruk\\Python\\prac3\\Cheques\\Cheque{chequeId[id]}.txt', 'r')
            strings = file.readlines()
            file.close()
            print("\n")
            for i in range(len(strings)):
                print(strings[i])
            countFiles += 1
    if countFiles == 0:
        print("У вас еще нет истории. \n"
              "Попробуйте заказать наш хачапури!\n")
    input("Выйти на главную")
    Users(userId)

def UserLoyality(userId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [User] inner join [Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {userId}"):
        nameLoyality = row.Name_Loyality
        discountLoyality = row.Discount
        discount = discountLoyality * 100
    print(f"Ваша программа лояльности: {nameLoyality}, скидка: {discount}%\n")
    input("Выйти на главную")
    Users(userId)