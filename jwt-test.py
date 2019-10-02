import jwt
import datetime
import threading

event = threading.Event()
key = '123456'
data = jwt.encode({'name':'yang','age':'28','exp':int(datetime.datetime.now().timestamp()+5)},key)
try:
    while not event.wait(1):
        print(jwt.decode(data,key))
        print(int(datetime.datetime.now().timestamp()))
except jwt.ExpiredSignatureError as e :
    print(e)