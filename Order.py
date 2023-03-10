import pyodbc
from os import system, name
import os.path
import time
import pathlib
from pathlib import Path
import Cheque
import CloseOrder
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Orders(userId):
    _ = system('cls')
    try:
        count = int(input("Сколько хачапури желаете заказать?\n"
                          "0 - Выйти на главную\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        Orders(userId)
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
                    Orders(userId)
                        
                if (ingridient <= countIngridient and ingridient > 0):
                    ingridients.append(ingridient)
                elif ingridient == 0:
                    print("Ну, нет - так нет...\n")
                else:
                    print("Неправильный ингридиент.")
                    Orders(userId)

                continueAdd = input("Добавить еще один ингредиент?\n").lower()
                if continueAdd == "yes" or continueAdd == "да":
                    addIngridients = True
                elif continueAdd == "no" or continueAdd == "нет":
                    addIngridients = False
                else:
                    print("Ошибка выбора\n"
                    "Сброс заказа хачапури...\n")
                    time.sleep(2)
                    Orders(userId)

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
            count = 1        
            CloseOrder.CloseOrder(userId, currentIdCheque, endIdHachapury, count)
        elif commit == "no" or commit == "нет":
            try:
                toOrder = input("Выберите действие: \n"
                    "1 - Продолжить оформление заказа\n"
                    "2 - Сбросить заказ\n")
            except ValueError:
                print("Введены неверные данные")
                Cheque.DropCheque(userId, currentIdCheque)
                time.sleep(2)
                Orders(userId)
            if toOrder > 0 and toOrder <= 2:
                match toOrder:
                    case '1':
                        print("Продолжаем заказ...\n")
                        time.sleep(2)
                        Orders(userId)
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
                Orders(userId)
        else:
            print("Неверное действие. Возврат к оформлению заказа.")
            Cheque.DropCheque(userId, currentIdCheque)
            time.sleep(2)
            Orders(userId)
    elif count == 0:
        CloseOrder.CloseOrder(userId, currentIdCheque, endIdHachapury, count)
    else:
        print("Введены неверные данные")
        time.sleep(2)
        Orders(userId)

