# #!/usr/bin/env python3

# import socket programming library
import time
import socket
import tool
import json
import hashlib
from sqlite3 import Error

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()


# thread fuction
def threaded(conn, addr):
    global i
    while True:

        # data received from client
        try:
            dat = tool.recv_msg(conn)
            data = json.loads(dat)
            print(data)
            print(data["user"])
            if data["user"] == "jj":
                if data["password"] == "jj":

                    # Generate token
                    token = tool.randomString(15)

                    # Encode and Send token back to client
                    msg = {}
                    msg["token"] = token
                    tool.send_msg(msg)

                    while True:

                        dat = tool.recv_msg(conn)
                        data = json.loads(dat)

                        if data["token"] != token:
                            break

                        if data["command"] == "checkout":
                            checkout()
                        elif data["command"] == "checkin":
                            checkin()
                        elif data["command"] == "IDK":
                            idk()
                        else:
                            tool.send_msg("Error. Something was wrong with your command.")

            print("Fail")
            conn.close()

            # print_lock.acquire()
            # tool.create_pcap_row(db, values)
            # print_lock.release()
            # print(addr)
        except Error as e:
            print("Error")
            print(e)

    # connection closed
    conn.close()


def Main():

    #Get client settings such as server ip and port
    with open('clientSettings.json') as json_file:
        data = json.load(json_file)
        for p in data:
#            server = p["server"]
            PORT = p["port"]
    HOST = ''

    global db
    db = tool.create_connection("pcap.db")
    tool.pcap_table(db)

    # a forever loop until client wants to exit
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        print("socket binded to port", PORT)

        # put the socket into listening mode
        s.listen(5)
        print("socket is listening")

        # establish connection with client
        c, addr = s.accept()

        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c, addr, ))

    s.close()


if __name__ == '__main__':
    Main()
