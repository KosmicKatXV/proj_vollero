import socket
import argparse
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/hearbeat', methods=['GET'])
def heartbeat():
    return jsonify({"alive": True})


@app.route('/key/<string:key>', methods=['POST'])
def insert(key):
    print("func call")
    print(request.json)
    value = request.json['value']
    conn = sqlite3.connect('master.db')
    cur = conn.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS keyvalue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL)   """)
    conn.commit()
    conn.close()
    return jsonify({'success': True})
    """if value is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'value': value.format()
    })"""



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
            cur.execute("CREATE TABLE IF NOT EXISTS "+"master"+" (key text PRIMARY KEY, value text)")
            # key text means that the first column is type text and named key
            # PRIMARY KEY means that the key column acts as the primary key of the table
            # value text means that the second column is type text and named value
            conn.commit()
            conn.close()

def parserInit():
    parser = argparse.ArgumentParser(
        prog='Master Database 2024',
        epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ', '--port', type=int, default=5010)
    return parser.parse_args()

def init():
    print('Starting master database')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname)
    print("Done! Master's ip is: " + IPaddr)
    return IPaddr

def main():
    args = parserInit()
    dbInit('master.db')
    IPaddr = init()
    app.run(host=IPaddr, port=args.port)


if __name__ == "__main__":
    main()

