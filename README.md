# liaotianshi
聊天室服务端(gevent_server.py)
import gevent
from gevent import monkey
monkey.patch_all()
import socket
import sys


HOST = "192.168.2.107"
PORT = 19870
ADDR = (HOST,PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(5)

def handler(c,addr):
    print("{} Connect Success".format(namedict[addr]))
    for addr1 in tcpdict:
        if tcpdict[addr1] is c:
            pass
        else:
            print("登录提醒发送给",namedict[addr1])
            tcpdict[addr1].send("{} Enter liaotianshi".format(namedict[addr]).encode())
    try:
        while True:
            data = c.recv(1024).decode()
            if not data or data == None:
                qname = namedict[addr]
                print("{}退出".format(qname))
                del namedict[addr]
                del tcpdict[addr]
                c.close()
                for addr1 in tcpdict:
                    tcpdict[addr1].send("{}退出".format(qname).encode())
                break
            else:
                for addr2 in tcpdict:
                    if tcpdict[addr2] is c:
                        pass
                    else:
                        print("发消息送给", namedict[addr2])
                        tcpdict[addr2].send("{0}Say:{1}".format(namedict[addr], data).encode())
    except Exception as e:
        print(e)
        del namedict[addr]
        del tcpdict[addr]
        c.close()

namedict = {}
tcpdict ={}
while True:
    c, addr = s.accept()
    print("Connect Success", addr)
    data = c.recv(1024).decode()
    namedict[addr] = data
    tcpdict[addr] = c
    gevent.spawn(handler,c,addr)
