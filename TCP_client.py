import socket
import select
import threading
import os


def SendData(tcp):
    while True:
        s = input("请输入发送信息")
        tcp.send(s.encode())

def MyNanme():
    s = input("请输入你的名字")
    if not s:
        os._exit(1)
    else:
        return s
myname = MyNanme()

HOST = "192.168.2.107"
PORT = 19870
ADDR = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(ADDR)
tcp.send(myname.encode())

mt = threading.Thread(target = SendData, args = (tcp,))
try:
    mt.start()
    while True:
        data = tcp.recv(1024).decode()
        if not data or data == None:
            break
        else:
            print(data)
except Exception as s:
    print(s)
finally:
    tcp.close()
    os._exit(1)
