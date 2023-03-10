import pyodbc
from os import system, name
import os.path
import time
import toOrder
import random
import datetime
now = datetime.datetime.now()
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def ChequeSumUpd(userId, currentIdCheque, endIdHachapury):
    sum = 100
    ingridientId = []
    for row in cursor.execute(f"select * from [Hachapury_Ingridient] where [Hachapury_ID] = {endIdHachapury}"):
        ingridientId.append(row.Ingridient_ID)
    
    for id in range(len(ingridientId)):
        for row in cursor.execute(f"select * from [Ingridient] where [ID_Ingridient] = {ingridientId[id]}"):
            costIngridient = row.Cost_Ingridient
        sum += costIngridient

    cursor.execute(f"update [Cheque] set [Sum_Order] = {sum} where [ID_Cheque] = {currentIdCheque}")
    cnxn.commit()


def Cheque(userId, count):
    for row in cursor.execute("select * from [Hachapury]"):
        cost = row.Cost_Hachapury
    sum = count * cost
    currentTime = now.strftime("%d-%m-%Y %H:%M")
    random.seed()
    if random.randint(1, 10) > 5:
        ear = 1
    else:
        ear = 0
    cursor.execute(f"insert into [Cheque] ([User_ID], [Count_Hachapury], [Cost_Hachapury], [Sum_Order], [Time_Order], [Ear]) values (?, ?, ?, ?, ?, ?)", 
                   (userId, count, cost, sum, currentTime, ear))
    cnxn.commit()

def DropCheque(userId, currentIdCheque):
    hachapuries = []
    for row in cursor.execute(f"select * from [Cheque_Hachapury] where [Cheque_ID] = {currentIdCheque}"):
        hachapuries.append(row.Hachapury_ID)
    for id in range(len(hachapuries)):
        cursor.execute(f"delete [Hachapury] where [ID_Hachapury] = {hachapuries[id]}")
        cnxn.commit()
    cursor.execute(f"delete [Cheque] where [ID_Cheque] = {currentIdCheque}")
    cnxn.commit()
    
    print("Возвращаемся в главное меню...")
    time.sleep(2)
    toOrder.toOrder(userId)