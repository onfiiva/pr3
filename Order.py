import pyodbc
from os import system, name
import os.path
import time
import User
import Cheque
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Order(userId):
    _ = system('cls')
    try:
        count = int(input("Сколько хачапури желаете заказать?\n"
                          "0 - Выйти на главную\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Order(userId)
    if (count > 0):
        Cheque.Cheque(userId, count)

        for i in range(count):
            print(f"Собираем хачапури №{i+1}... \n")

            ingridients = []
            addIngridients = True

            while addIngridients ==True:
                nameIngridient, costIngridient, typeIngridient = [], [], []
                print("Ингридиенты: \n")

                for row in cursor.execute("select * from [Ingridient] inner join [Type_Ingridient] on [Type_ID] = [ID_Type]"):
                    nameIngridient.append(row.Name_Ingridient)
                    costIngridient.append(row.Cost_Ingridient)
                    typeIngridient.append(row.Name_Type)

                print("0 - Не выбирать ингридиент\n")
                for i in range(len(nameIngridient)):
                    print(i+1, " - ", typeIngridient[i], " - ", nameIngridient[i], " - ", costIngridient[i], "Рублей \n")
                            
                for count in range(len(nameIngridient)):
                    countIngridient = count+1

                print("Выберите ингридиент: \n")
                try:
                    ingridient = int(input())
                except ValueError:
                    print("Введены неверные данные")
                    time.sleep(2)
                    Order(userId)
                        
                if (ingridient <= countIngridient and ingridient > 0):
                    ingridients.append(ingridient)
                elif ingridient == 0:
                    print("Ну, нет - так нет...\n")
                else:
                    print("Неправильный ингридиент.")
                    Order(userId)

                continueAdd = input("Добавить еще один ингредиент?\n").lower()
                if continueAdd == "yes" or continueAdd == "да":
                    addIngridients = True
                elif continueAdd == "no" or continueAdd == "нет":
                    addIngridients = False
                else:
                    print("Ошибка выбора\n"
                    "Сброс заказа хачапури...\n")
                    time.sleep(2)
                    Order(userId)

            print("Заканчиваем сборку... \n"
                "Добавляются ингридиенты:\n")
            for i in range(len(ingridients)):
                print(nameIngridient[ingridients[i]], " - ", costIngridient[ingridients[i]], "Рублей \n")
                    
            time.sleep(5)

            cursor.execute(f"insert into [Hachapury] ([Cost_Hachapury]) values (100)")
            cnxn.commit()
            idHachapury = []
            for row in cursor.execute("select * from [Hachapury]"):
                idHachapury.append(row.ID_Hachapury)

            for id in range(len(idHachapury)):
                endIdHachapury = idHachapury[id]

            for ingrid in range(len(ingridients)):
                cursor.execute(f"insert into [Hachapury_Ingridient] ([Hachapury_ID], [Ingridient_ID]) values (?, ?)", (endIdHachapury, ingridients[ingrid]))
                cnxn.commit()
                
            idCheque = []

            for row in cursor.execute("select * from [Cheque]"):
                idCheque.append(row.ID_Cheque)

            for id in range(len(idCheque)):
                currentIdCheque = idCheque[id]

            Cheque.ChequeSumUpd(userId, currentIdCheque, endIdHachapury)
            
            print("Собрали ваш хачапури :)")

        commit = input("Завершить оформление заказа?\n").lower()

        if commit == "yes" or commit == "да":
            print("Завершаем оформление заказа...\n")
            time.sleep(2)
                    
            CloseOrder(userId, currentIdCheque, endIdHachapury)
        elif commit == "no" or commit == "нет":
            try:
                toOrder = input("Выберите действие: \n"
                    "1 - Продолжить оформление заказа\n"
                    "2 - Сбросить заказ\n")
            except ValueError:
                print("Введены неверные данные")
                Cheque.DropCheque(userId, currentIdCheque)
                time.sleep(2)
                Order(userId)
            if toOrder > 0 and toOrder <= 2:
                match toOrder:
                    case '1':
                        print("Продолжаем заказ...\n")
                        time.sleep(2)
                        Order(userId)
                    case '2':
                        print("Сбрасываем заказ...\n")
                        time.sleep(2)
                        Cheque.DropCheque(userId, currentIdCheque)
                    case _:
                        print("Сбрасываем заказ...\n")
                        time.sleep(2)
                        Cheque.DropCheque(userId, currentIdCheque)
            else:
                print("Неверное действие. Возврат к оформлению заказа.")
                time.sleep(2)
                Cheque.DropCheque(userId, currentIdCheque)
                Order(userId)
        else:
            print("Неверное действие. Возврат к оформлению заказа.")
            Cheque.DropCheque(userId, currentIdCheque)
            time.sleep(2)
            Order(userId)
    elif count == 0:
        User.User(userId)
    else:
        print("Введены неверные данные")
        time.sleep(2)
        Order(userId)

def CloseOrder(userId, currentIdCheque, endIdHachapury):
    for row in cursor.execute(f"select * from [User] where [ID_User] = {userId}"):
        balance = row.Balance_User
    for row in cursor.execute(f"select * from [Cheque] inner join [User] on [User_ID] = [ID_User] where [ID_Cheque] = {currentIdCheque}"):
        phone = row.Phone_User
        count = row.Count_Hachapury
        cost = row.Cost_Hachapury
        sum = row.Sum_Order
        timeOrder = row.Time_Order
        ear = row.Ear
    
    
    balance -= sum
    if (balance >= 0):
        cursor.execute(f"update [User] set [Balance_User] = {balance} where [ID_User] = {userId}")
        cnxn.commit()
    else:
        print("Недостаточно денег на счету.")
        time.sleep(2)
        Order(userId)

    ingridientId = []
    for row in cursor.execute(f"select * from [Hachapury_Ingridient] where [Hachapury_ID] = {endIdHachapury}"):
        ingridientId.append(row.Ingridient_ID)
    
    file = open(f'C:\\Users\\kiruk\\Python\\prac3\\Cheques\\Cheque{currentIdCheque}.txt', 'w')
    file.write(f"Заказ №{currentIdCheque}\n"
               f"Время: {timeOrder}\n"
               f"Пользователь: {phone}\n"
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
    User.User(userId)
