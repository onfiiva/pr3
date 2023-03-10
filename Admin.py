import pyodbc
from os import system, name
import os.path
import time
import pathlib
from pathlib import Path
import Main
import Supply
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Admin(adminId):
    _ = system('cls')
    for row in cursor.execute(f"select * from [Admin] where [ID_Admin] = '{adminId}'"):
         balance = row.Balance_Admin
    os.system="cls"

    print("Ашот")
    print(f"У вас на счету {balance} рублей.\n")
    try:
        function = int(input("Выберите функцию\n"
        "1 - Заказать ингридиент\n"
        "2 - История покупок пользователей\n"
        "3 - Карты лояльности пользователей\n"
        "4 - Выйти из аккаунта\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Admin(adminId)

    match function:
        case 1:
            Supply.Supply(adminId)
        case 2:
            AdminUsersHistory(adminId)
        case 3:
            AdminUsersLoyality(adminId)
        case 4:
            Main.mainwindow()

def AdminUsersHistory(adminId):
    _ = system('cls')
    userId, phoneUser, passwordUser, balanceUser, chequeId = [], [], [], [], []
    countFiles = 0
    for row in cursor.execute("select * from [User]"):
        userId.append(row.ID_User)
        phoneUser.append(row.Phone_User)
        passwordUser.append(row.Password_User)
        balanceUser.append(row.Balance_User)

    print("Пользователи:\n")
    for i in range(len(userId)):
        print(f"{userId[i]} - {phoneUser[i]} - {passwordUser[i]} - {balanceUser[i]}")
    
    try:
        idUser = int(input("Выберите пользователя для просмотра истории: \n"
                           "0 - Выйти на главную.\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        AdminUsersHistory(adminId)

    if idUser > 0 and idUser <= len(userId) and userId.count(idUser) > 0:
        for row in cursor.execute(f"select * from [Cheque] where [User_ID] = {idUser}"):
            chequeId.append(row.ID_Cheque)
        for id in range(len(chequeId)):
            directory = Path(pathlib.Path.cwd(), 'Cheques', f'Cheque{chequeId[id]}.txt')
            if (os.path.exists(directory)):
                file = open(directory, 'r')
                strings = file.readlines()
                file.close()
                print("\n")
                for i in range(len(strings)):
                    print(strings[i])
                countFiles += 1
        if countFiles == 0:
            print("У пользователя еще нет истории. \n")
        input("Выйти на главную.")
        Admin(adminId)
    elif (idUser == 0):
        Admin(adminId)
    else:
        print("Неверное действие")
        time.sleep(2)
        AdminUsersHistory(adminId)

def AdminUsersLoyality(adminId):
    _ = system('cls')
    userId, phoneUser, passwordUser, balanceUser = [], [], [], []
    for row in cursor.execute("select * from [User]"):
        userId.append(row.ID_User)
        phoneUser.append(row.Phone_User)
        passwordUser.append(row.Password_User)
        balanceUser.append(row.Balance_User)

    print("Пользователи:\n")
    for i in range(len(userId)):
        print(f"{userId[i]} - {phoneUser[i]} - {passwordUser[i]} - {balanceUser[i]}")
    
    try:
        idUser = int(input("\nВыберите пользователя для просмотра карты лояльности: \n"
                           "0 - Выйти на главную.\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        AdminUsersLoyality(adminId)

    if (idUser > 0 and idUser <= len(userId) and userId.count(idUser) > 0):
        for row in cursor.execute(f"select * from [User] inner join [Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {idUser}"):
            nameLoyality = row.Name_Loyality
            discountLoyality = row.Discount
            discount = discountLoyality * 100
        print(f"Ваша программа лояльности: {nameLoyality}, скидка: {discount}%\n")
        input("Выйти на главную")
        Admin(adminId)
    elif (idUser == 0):
        Admin(adminId)
    else:
        print("Неверное действие.")
        time.sleep(2)
        AdminUsersLoyality(adminId)