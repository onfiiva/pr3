import pyodbc
from os import system, name
import Main
import Admin
import User
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()
def Auth(phone, password):
    _ = system('cls')
    
    isAuthorized = False
    phone_user, pass_user, phone_admin, pass_admin = [], [], [], []
    for row in cursor.execute("select * from [User]"):
        phone_user.append(row.Phone_User)
        pass_user.append(row.Password_User)
    
    for row in cursor.execute("select * from [Admin]"):
        phone_admin.append(row.Phone_Admin)
        pass_admin.append(row.Password_Admin)
    
    for id in range(len(phone_admin)):
        if phone == phone_admin[id] and password == pass_admin[id]:
            for row in cursor.execute(f"select * from [Admin] where [Phone_Admin] = {phone}"):
                adminId = row.ID_Admin
            isAuthorized = True
            Admin.Admin(adminId)
    for id in range(len(phone_user)):
        if phone == phone_user[id] and password == pass_user[id]:
            for row in cursor.execute(f"select * from [User] where [Phone_User] = {phone}"):
                userId = row.ID_User
            isAuthorized = True
            User.User(userId)
    if isAuthorized == False:
        print("Неправильно введенные данные")
        Main.main()