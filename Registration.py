import pyodbc
from os import system, name
import time
import Main
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()
def Reg(phone, password):
    _ = system('cls')
    loyality = 1
    confirmReg = True
    phone_user, phone_admin = [], []
    for row in cursor.execute("select * from [User]"):
        phone_user.append(row.Phone_User)
    
    for row in cursor.execute("select * from [Admin]"):
        phone_admin.append(row.Phone_Admin)

    for id in range(len(phone_admin)):
        if phone == phone_admin[id]:
            confirmReg = False

    for id in range(len(phone_user)):
        if phone == phone_user[id]:
            confirmReg = False
    
    if confirmReg == True:
        random.seed()
        balance = random.randint(1000, 10000)
        cursor.execute("insert into [User] ([Loyality_ID], [Phone_User], [Password_User], [Balance_User]) values (?, ?, ?, ?)", 
                    loyality, phone, password, balance)
        cnxn.commit()
        time.sleep(2)
        print("Аккаунт зарегистрирован.")
        time.sleep(2)
        Main.main()
    else:
        print("Такой номер телефона уже зарегистрирован")
        time.sleep(2)
        Main.main()