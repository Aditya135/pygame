from networking import communicate
from threading import Thread
from time import sleep



com2 = communicate(("127.0.0.1",12346),"XYZ",12345)

def handle_com1():
    com1 = communicate(("127.0.0.1",12345),"Aditya",12346)
    if com1.wait_connection():
        print("connected")
    else:
        print("no connectiion!")
        com1.closeconnection()
        return 0
    print(com1.get_connection_status())
    while True:
        if not com1.is_connected:
            break
        com1.send_data("Hi this is Aditya98")
        print(com1.get_data())
        sleep(2)

thread = Thread(target=handle_com1)
thread.start()
com2.createConnection()
print(com2.get_connection_status())

try:
    while True:
        if not com2.is_connected:
            break
        print(com2.get_data())
        com2.send_data("Hi this is xyz")
        sleep(2)
except:
        com2.closeconnection()
        print("connection closed")


    
    
