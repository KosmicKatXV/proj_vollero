import socket
import argparse
import sqlite3
import hashlib
from flask import Flask, abort,jsonify, request, Response

app = Flask(__name__)

@app.route('/key/<string:key>',methods=['GET'])
def retrieve(key):
    hashedKey = hashlib.sha256((key).encode('ascii')).hexdigest()
    conn = sqlite3.connect('slave.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM "+"slave"+" WHERE key='"+hashedKey+"'")
    res = cursor.fetchall()
    conn.close()
    if(res == []):  return jsonify(res),404
    else:           return jsonify(res),200

@app.route('/key/<string:key>',methods=['POST'])
def insert(key):
    value = request.json['value']
    hashedKey = hashlib.sha256((key).encode('ascii')).hexdigest()
    conn = sqlite3.connect('slave.db')
    cursor = conn.cursor()
    query = "Replace into "+"slave"+" values('"+hashedKey+"','"+value+"')"
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()
    return Response(status=200)

def dbInit(dbName):
    conn = None
    try:
        conn = sqlite3.connect(dbName)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS "+"slave"+" (key VARCHAR(65) PRIMARY KEY, value VARCHAR(255))")
            conn.commit()
            conn.close()

def parserInit():
    parser = argparse.ArgumentParser(
                    prog='Slave Database 2024',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ', '--port', type=int, default=4001)
    parser.add_argument('-db ', '--database', type=str,default="slave.db")
    return parser.parse_args()

def main():
    print('Starting slave')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    parser = parserInit()
    dbInit(parser.database)
    print("Done! Slave's ip is: " + IPaddr)
    app.run(host=IPaddr, port=parser.port)

if __name__ == "__main__":
    main()
