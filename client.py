#!usr/bin/python3

import tool
import json
import socket

with open('clientSettings.json') as json_file:
    data = json.load(json_file)
    for p in data:
        server = p["server"]
        port = p["port"]


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server, port))
        while True:
            tool.send_msg(s, "test")
