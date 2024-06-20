from flask import Flask
import json
import requests
import socket

app = Flask(__name__)

ip_port = []

def importIP():
    with open('IP.json') as f:
        data = json.loads(f.read())
    for item in data["slaves"]:
        ip_port.append((item["IP"], item["port"]))
    return ip_port

def parserInit():
    parser = argparse.ArgumentParser(
                    prog='Endpoint Database 2024',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ',  '--port',      type=int)
    parser.add_argument('-f ',  '--replicationfactor',    type=int,default=3)
    return parser.parse_args()

def main():
    app = Flask(__name__)
    print('Starting endpoint')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    parser = parserInit()
    print("Done! Endpoint's ip is: " + IPaddr)
    
@app.route('/heartbeat')
def heartbeat():
    return jsonify({
        'alive': True
    })

@app.route('/keys')
@app.route('/key/<string:key>',methods=['GET'])
def retrieve(key):    
    return jsonify({
        'success': True,
        'value': 12})

@app.route('/key/<string:key>',methods=['POST'])
def insert(key):
    value = requests.post(url_master, json=new_data)
    return value

if __name__ == "__main__":
    main()