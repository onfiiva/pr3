import pyodbc
from os import system, name
import os.path
import time
import pathlib
from pathlib import Path
import toUser
import Order
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()
ingridientId = []
def CloseOrder(adminId, userId, currentIdCheque, endIdHachapury, count):
    if count == 0:
        toUser.toUser(userId)
    for row in cursor.execute(f"select * from [User] where [ID_User] = {userId}"):
        balance = row.Balance_User
    for row in cursor.execute(f"select * from [Admin] where [ID_Admin] = {adminId}"):
        balanceAdmin = row.Balance_Admin
    for row in cursor.execute(f"select * from [Cheque] inner join [User] on [User_ID] = [ID_User] where [ID_Cheque] = {currentIdCheque}"):
        email = row.Email_User
        count = row.Count_Hachapury
        cost = row.Cost_Hachapury
        sum = row.Sum_Order
        timeOrder = row.Time_Order
        ear = row.Ear
        noticed = row.Noticed
    
    for row in cursor.execute(f"select * from [User] inner join [Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {userId}"):
        loyalityDiscount = row.Discount
        nameLoyality = row.Name_Loyality
    
    discount = sum * loyalityDiscount
    print(f"Ваша скидка : {discount}")
    balance -= (sum - discount)
    balanceAdmin += (sum - discount)
    if (balance >= 0):
        cursor.execute(f"update [User] set [Balance_User] = {balance} where [ID_User] = {userId}")
        cnxn.commit()
        cursor.execute(f"update [Admin] set [Balance_Admin] = {balanceAdmin} where [ID_Admin] = {adminId}")
        cnxn.commit()
    else:
        print("Недостаточно денег на счету.")
        time.sleep(2)
        Order.Orders(userId)

    for i in range(len(endIdHachapury)):
        for row in cursor.execute(f"select * from [Hachapury_Ingridient] where [Hachapury_ID] = {endIdHachapury[i]}"):
            ingridientId.append(row.Ingridient_ID)
            
    directory = Path(pathlib.Path.cwd(), 'Cheques')
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = Path(pathlib.Path.cwd(), 'Cheques', f'Cheque{currentIdCheque}.txt')
    file = open(directory, 'w')
    file.write(f"Заказ №{currentIdCheque}\n"
               f"Время: {timeOrder}\n"
               f"Пользователь: {email}\n"
               "\n"
               "Состав заказа: \n"
               "\n"
               f"Хачапури: {count} шт., {cost} руб. за шт.\n"
               "Ингридиенты: \n")
    
    for id in range(len(ingridientId)):
        for row in cursor.execute(f"select * from [Ingridient] where [ID_Ingridient] = {ingridientId[id]}"):
            nameIngridient = row.Name_Ingridient
            costIngridient = row.Cost_Ingridient
            countIngridient = row.Count_Ingridient
        count = ingridientId.count(ingridientId[id])
        sumIngridient = costIngridient * count
        
        cursor.execute(f"update [Ingridient] set [Count_Ingridient] = {countIngridient - count} where [ID_Ingridient] = {ingridientId[id]}")
        cnxn.commit()

        file.write(f"{nameIngridient}, {count} шт., {costIngridient} рублей за шт., {sumIngridient} рублей итого.\n")
               
    file.write(f"Ухо: {ear}\n"
               f"Пользователь заметил: {noticed}\n"
                "\n"
               f"Итого: {sum}")
    file.close()

    print(f"Заказ оформлен! Чек №{currentIdCheque}")
    if (sum > 200):
        cursor.execute(f"update [User] set [Loyality_ID] = 2 where [ID_User] = {userId}")
        cnxn.commit()
    elif (sum > 300):
        cursor.execute(f"update [User] set [Loyality_ID] = 3 where [ID_User] = {userId}")
        cnxn.commit()
    elif (sum > 500):
        cursor.execute(f"update [User] set [Loyality_ID] = 4 where [ID_User] = {userId}")
        cnxn.commit()
    time.sleep(2)
    toUser.toUser(adminId, userId)