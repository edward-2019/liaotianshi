import socket
import select
import threading


HOST = "192.168.0.130"
PORT = 19870
ADDR = (HOST, PORT)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind(ADDR)
tcp.listen(5)

rlist = [tcp]
wlist = []
xlist = [tcp]
namedict = {}
def AdminSay():
    while True:
        s = input("管理员喊话:")
        for i in rlist[1:]:
            i.send(("管理员喊话:"+s).encode())

td = threading.Thread(target = AdminSay)
td.start()


def main():
    while True:
        rl, wl, xl = select.select(rlist, wlist, xlist)
        print("收到IO事件")
        for r in rl:
            if r is tcp:
                newtcp,addr = tcp.accept()
                myname =newtcp.recv(1024).decode()
                namedict[addr] = myname
                print("{} client connect success".format(myname))
                for x in rlist[1:]:
                    x.send("{} client Enter".format(myname).encode())
                rlist.append(newtcp)
            else:
                data = r.recv(1024).decode()
                myname = r.getpeername()
                if not data or data == None:
                    print("{}客户端退出".format(namedict[myname]))
                    rlist.remove(r)
                    for x in rlist[1:]:
                        x.send("{}退出聊天室".format(namedict[myname]).encode())
                    r.close()
                    del namedict[myname]
                else:
                    print("服务器接收到:", data)
                    for x in rlist[1:]:
                        if x is r:
                            pass
                        else:
                            x.send(str(namedict[myname]+"say:"+data).encode())



if __name__ == "__main__":
    main()
