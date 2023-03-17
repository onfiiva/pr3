import pyodbc
from os import system, name
#import Main
import toAdmin
import toUser
import time
cnxn = pyodbc.connect('Driver={SQL Server};Server=FIIVA\DA;Database=Hachapury;Trusted_Connection=yes;')
cursor = cnxn.cursor()
def Auth(email, password):
    _ = system('cls')
    
    isAuthorized = False
    email_user, pass_user, email_admin, pass_admin = [], [], [], []
    for row in cursor.execute("select * from [User]"):
        email_user.append(row.Email_User)
        pass_user.append(row.Password_User)
    
    for row in cursor.execute("select * from [Admin]"):
        email_admin.append(row.Email_Admin)
        pass_admin.append(row.Password_Admin)
    
    for id in range(len(email_admin)):
        if email == email_admin[id] and password == pass_admin[id]:
            for row in cursor.execute(f"select * from [Admin] where [Email_Admin] = '{email}'"):
                adminId = row.ID_Admin
            isAuthorized = True
            toAdmin.toAdmin(adminId)
    for id in range(len(email_user)):
        if email == email_user[id] and password == pass_user[id]:
            for row in cursor.execute(f"select * from [User] where [Email_User] = '{email}'"):
                userId = row.ID_User
            isAuthorized = True
            toUser.toUser(userId)
    if isAuthorized == False:
        print("Неправильно введенные данные")
        time.sleep(2)
        #Main.mainwindow()