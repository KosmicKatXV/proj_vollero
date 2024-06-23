import socket
import argparse
import sqlite3
import hashlib
import requests
from flask import Flask, jsonify, request, Response
import random

app = Flask(__name__)


@app.route('/hearbeat', methods=['GET'])
def heartbeat():
    return jsonify({"alive": True})


@app.route('/slaves', methods=['POST'])
def getSlavesList():
    slaves = request.json['slaves']
    for s in slaves:
        slavesList.append(s)
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
    replication_factor = request.json['replication']
    hashedKey = hashlib.sha256((key).encode('ascii')).hexdigest()
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    query = "Replace into "+dbName[:-3]+" values('"+hashedKey+"','"+str(value)+"')"
    print(query)
    cursor.execute(query)
    conn.commit()
    # now i need to write the same thing in the slaves using the replication factor
    replicate_to_slaves(key, value, replication_factor)
    # synchronous replication. Master waits for all slaves to replicate the data and then sends a response
    conn.close()
    # i need a responde that can contain json data
    return jsonify({"message": "Insertion successful"}), 200


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


def replicate_to_slaves(key, value, replication_factor):
    r = random.sample(range(len(slavesList)), min(replication_factor,len(slavesList)))
    for i in range(len(r)):
        response = requests.post(f'http://{slavesList[r[i]]}/key/{key}', headers={'Content-Type': 'application/json'}, json={'value': value}, timeout=5)
        #response = requests.post(f'http://{slavesList[r[i]]}/key/{key}', headers={'token': token,'Content-Type': 'application/json'}, json={'value': data['value'], 'replication': data['rep']}, timeout=timeout)
        
        if response.status_code != 200:
            return jsonify({"error": f"Failed to replicate to slave at + {slavesList[r[i]]}"})
        else:
            return jsonify({"message": f"Replication successful at + {slavesList[r[i]]}"})


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

