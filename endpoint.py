import argparse
from flask import Flask, jsonify, request
import json
import requests
import socket
import random
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'p4ssword'
s = Serializer(app.config['SECRET_KEY'])


@app.route('/heartbeat')
def heartbeat():
    return jsonify({
        'alive': True
    })


@app.route('/masters', methods=['POST'])
def getMasterList():
    m = request.json['masters']
    for master in m:
        if(master not in masters): masters.append(master)
    return jsonify({"alive": True})


@app.route('/slaves', methods=['POST'])
def getSlavesList():
    s = request.json['slaves']
    for slave in s:
        if(slave not in slaves): slaves.append(slave)
    return jsonify({"alive": True})


@app.route('/masters', methods=['DELETE'])
def delMasterList():
    m = request.json['masters']
    for master in m:
        if(master in masters): masters.remove(master)
    return jsonify({"alive": True})


@app.route('/slaves', methods=['DELETE'])
def delSlavesList():
    s = request.json['slaves']
    for slave in s:
        if(slave in slaves): slaves.remove(slave)
    print(slaves)
    return jsonify({"alive": True})


@app.route('/key/<string:key>', methods=['GET'])
def retrieve(key):
    global slaves
    print("func call")
    random.shuffle(slaves)
    for slave in slaves:
        try:
            response = requests.get(f'http://{slave}/key/{key}', timeout=timeout)
            if response.status_code == 200:
                return response.json(), response.status_code
                # we need to find a way to search in the db wether the information is there
        except requests.exceptions.RequestException:
            continue

    return jsonify({'error': 'No updated data found'}), 404


@app.route('/key/<string:key>', methods=['POST'])
def insert(key):
    print("func call")
    #  NBB important il CONTENT-TYPE deve essere application/json
    #  NBB in the header of the request name:'Content-Type' value:'application/json' is required
    data = request.get_json()  # get the json value from the request
    #value = data['value']
    #replication_f = data['rep']
    token = request.headers.get('token')
    #print(token,replication_f,value)
    try:
        tok = s.loads(token)   # deserializing token recieved in the request
    except (SignatureExpired, BadSignature):
        return jsonify({'error': 'Invalid or Expired token'}), 401
    if not tok['admin']:
        print(tok['admin'])
        return jsonify({'error': 'Admin access required'}), 402
    else:
        print(tok['admin'])
        # NBB Get requests don't have a body so if u need to insert values u are meant to
        # do a request.post or else u will get a 400 bad request error
        print(masters[0])
        response = requests.post(f'http://{masters[0]}/key/{key}', headers={'token': token}, json={'value': data['value'], 'replication': data['rep']}, timeout=timeout)
        return response.json(), response.status_code



def importIP():
    output = []
    output2 = []
    with open('IP.json') as f:
        data = json.loads(f.read())
    for item in data["slaves"]:
        output.append((item["IP"]+':'+item["port"]))
    for item in data["masters"]:
        output2.append((item["IP"]+':'+item["port"]))
    return output,output2

def sendJson(json,receiverList,path):
    for receiver in receiverList:
        try:
            response = requests.post(f'http://'+receiver+path, headers={'Content-Type': 'application/json'}, json=json, timeout=timeout)
        except:
            fallen.append(receiver)

def parserInit():
    parser = argparse.ArgumentParser(
                    prog='Endpoint Database 2024',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ',  '--port', type=int, default=3000)
    parser.add_argument('-f ',  '--replicationfactor', type=int, default=3)
    parser.add_argument('-t ',  '--timeout', type=int, default=5)
    return parser.parse_args()


def main():
    global slaves
    global masters
    global fallen
    global timeout
    global keys
    print('Starting endpoint...')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    args = parserInit()
    timeout = args.timeout
    slaves,masters = importIP()
    fallen = []
    print("Done! Endpoint's ip is: " + IPaddr)
    print("Sending info to masters and slaves...")
    sendJson({'slaves':slaves},masters,'/slaves')
    sendJson({'masters':masters},slaves,'/masters')
    app.run(host=IPaddr, port=args.port)


if __name__ == "__main__":
    main()

    # THESE COMMENTS ARE TO CORRECTLT MAKE A REQUEST TO THE ENDPOINT
    """
    To test your endpoint.py follow these steps:  
    Run your endpoint.py script. This will start your Flask server.
    Open the RESTED extension in your browser.
    Set the HTTP method to either GET or POST depending on the request 
    In the URL field, enter the URL of your endpoint. This will be http://<your-server-ip>:<your-server-port>/key/<your-key>.
    In the Headers section, add a new header with the name token and the value as the token you received from the auth server.
    If you're making a POST request, you can enter the data you want to send in the Body section.
    Click on the Send button to send the request.
    """