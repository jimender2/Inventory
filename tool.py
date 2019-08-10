#!usr/bin/python3
# This project is the beginning of the wifi triangulation problem.

import string
import struct
import socket
import sqlite3
from sqlite3 import Error


"""
SQL FUNCTIONS
-------------
create_connection(db_file)
create_table(conn, create_table_sql)
pcap_table(conn)
create_row(conn, data)

"""


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)#, isolation_level=None)
        conn.execute('pragma journal_mode=wal')
        conn.execute("PRAGMA cache_size = 100000")
        conn.execute("PRAGMA temp_store = MEMORY")
        conn.execute("PRAGMA synchronous = FULL")
        return conn
    except Error as e:
        print(e)
    return None


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def pcap_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS pcap(
                id integer PRIMARY KEY AUTOINCREMENT,
                frame_interface_name text,
                frame_time text,
                wlan_signal_dbm text,
                wlan_ra_resolved text,
                wlan_da text,
                wlan_da_resolved text,
                wlan_ta text,
                wlan_ta_resolved text,
                wlan_bssid text,
                wlan_bssid_resolved text,
                wlan_addr text,
                wlan_addr_resolved text,
                ssid text,
                ip text NOT NULL,
                port integer NOT NULL,
                packet text,
                hash text
                );"""

    if conn is not None:
        create_table(conn, sql)
    else:
        print("Error! cannot create the database table.")


def create_pcap_row(conn, data):
    sql = """ INSERT INTO pcap(frame_interface_name, frame_time,
                wlan_signal_dbm, wlan_ra_resolved, wlan_da, wlan_da_resolved,
                wlan_ta, wlan_ta_resolved, wlan_bssid, wlan_bssid_resolved,
                wlan_addr, wlan_addr_resolved, ssid, ip, port, packet, hash
                )

                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """

    cur = conn.cursor()
    cur.execute('BEGIN TRANSACTION;')
    cur.executemany(sql, data)
    cur.execute('END TRANSACTION;')
    conn.commit()


"""
Socket FUNCTIONS
----------------
find_unused_port_in_range(rangestart, rangeend, host)
is_port_in_use(port, host)
send_msg(sock, msg)
recv_msg(sock)
recvall(sock, n)

"""


def find_unused_port_in_range(rangestart, rangeend, host, ignorelist=[]):
    for i in range(rangestart, rangeend + 1):
        if i not in ignorelist:
            if not is_port_in_use(i, host):
                return i


def is_port_in_use(port, host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def send_msg(sock, msg):
    msg = msg.encode('utf-8')
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(sock, msglen).decode('utf-8')


def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


"""
Misc FUNCTIONS
----------------
randomString(stringLength)

"""


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
