from flask import Flask
import json
import requests

app = Flask(__name__)

import socket

ip_port = []
with open('IP.json') as f:
    data = json.loads(f.read())

for item in data["slaves"]:
    ip_port.append((item["IP"], item["port"]))
print(ip_port)


def init():
    print('Starting endpoint')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    print("Done! Endpoint's ip is: " + IPaddr)

def main():
    init()

if __name__ == "__main__":
    main()