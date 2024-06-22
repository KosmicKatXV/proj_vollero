import socket
import argparse
import sqlite3
import hashlib
from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/hearbeat', methods=['GET'])
def heartbeat():
    return jsonify({"alive": True})

@app.route('/slaves', methods=['POST'])
def getSlavesList():
    slaves = request.json['slaves']
    for slave in slaves:
        if(slave not in slavesList): slavesList.append(slave)
    print(slavesList)
    return jsonify({"alive": True})

@app.route('/slaves', methods=['DELETE'])
def delSlavesList():
    slaves = request.json['slaves']
    for slave in slaves:
        if(slave not in slavesList): slavesList.remove(slave)
    return jsonify({"alive": True})

@app.route('/key/<string:key>', methods=['POST'])
def insert(key):
    value = request.json['value']
    hashedKey = hashlib.sha256((key).encode('ascii')).hexdigest()
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    query = "Replace into "+dbName[:-3]+" values('"+hashedKey+"','"+value+"')"
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    return Response(status=200)


def dbInit(dbName):
    conn = None
    try:
        conn = sqlite3.connect(dbName)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS "+dbName[:-3]+" (key VARCHAR(65) PRIMARY KEY, value VARCHAR(255))")
            conn.commit()
            conn.close()

def parserInit():
    parser = argparse.ArgumentParser(
        prog='Master Database 2024',
        epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ', '--port', type=int, default=5000)
    parser.add_argument('-db ', '--database', type=str,default="master.db")
    return parser.parse_args()

def init():
    print('Starting master database')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname)
    print("Done! Master's ip is: " + IPaddr)
    return IPaddr

def main():
    global dbName
    global slavesList
    slavesList = []
    args = parserInit()
    dbName = args.database
    dbInit(dbName)
    IPaddr = init()
    app.run(host=IPaddr, port=args.port)


if __name__ == "__main__":
    main()

