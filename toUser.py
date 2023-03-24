import User
import time
def toUser(adminId, userId):
    print("Выход в меню пользователя..")
    time.sleep(1)
    User.Users(adminId, userId)