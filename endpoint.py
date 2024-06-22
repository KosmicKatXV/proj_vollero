import argparse
from flask import Flask, jsonify, request
import json
import requests
import socket
from itsdangerous import URLSafeTimedSerializer as Serializer,BadSignature, SignatureExpired

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
    token = request.headers.get('token', timeout=timeout)
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return jsonify({'error': 'Invalid or Expired token'}), 401

    if not data['user']:
        return jsonify({'error': 'no user recognized'}), 402

    # if user is recognized, and is either admin or not then it can read from slaves
    else:
        # admins can read from slaves and master
        response = requests.get(f'http://slaveserverIP:port/key/{key}', headers={'token': token}, timeout=timeout)
        return response.json(), response.status_code


@app.route('/key/<string:key>', methods=['POST'])
def insert(key):
    print("func call")
    #  NBB in the header of the request name:'Content-Type' value:'application/json' is required
    data = request.get_json()  # get the json value from the request
    value = data['value']
    replication_f = data['rep']
    print(replication_f)
    token = request.headers.get('token')
    print(token)
    try:
        tok = s.loads(token)   # deserializing token recieved in the request
    except (SignatureExpired, BadSignature):
        print(-1)
        return jsonify({'error': 'Invalid or Expired token'}), 401
    if not tok['admin']:
        print(data['admin'])
        return jsonify({'error': 'Admin access required'}), 402
    else:
        print(data['admin'])
        # NBB Get requests don't have a body so if u need to insert values u are meant to
        # do a request.post or else u will get a 400 bad request error
        response = requests.post(f'http://192.168.56.1:5010/key/{key}', headers={'token': token}, json={'value': value}, timeout=timeout, replication=replication_f)
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