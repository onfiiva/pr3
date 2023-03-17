import pyodbc
from os import system, name
import time
import random
#import Main
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def Regss(email, password):
    _ = system('cls')
    loyality = 1
    confirmReg = True
    email_user, phone_admin = [], []
    for row in cursor.execute("select * from [User]"):
        email_user.append(row.Email_User)
    
    for row in cursor.execute("select * from [Admin]"):
        phone_admin.append(row.Email_Admin)

    for id in range(len(phone_admin)):
        if email == phone_admin[id]:
            confirmReg = False

    for id in range(len(email_user)):
        if email == email_user[id]:
            confirmReg = False
    
    if confirmReg == True:
        random.seed()
        balance = random.randint(1000, 10000)
        cursor.execute("insert into [User] ([Loyality_ID], [Email_User], [Password_User], [Balance_User]) values (?, ?, ?, ?)", 
                    loyality, email, password, balance)
        cnxn.commit()
        time.sleep(2)
        print("Аккаунт зарегистрирован.")
        time.sleep(2)
        #Main.mainwindow()
    else:
        print("Такой номер телефона уже зарегистрирован")
        time.sleep(2)
        #Main.mainwindow()