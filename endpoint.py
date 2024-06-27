import argparse
from flask import Flask, jsonify, request
import json
import requests
import socket
import random
import hashlib
import time
from apscheduler.schedulers.background import BackgroundScheduler

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
        if (master not in masters): masters.append(master)
    return jsonify({"alive": True})


@app.route('/slaves', methods=['POST'])
def getSlavesList():
    s = request.json['slaves']
    for slave in s:
        if (slave not in slaves): slaves.append(slave)
    return jsonify({"alive": True})


@app.route('/masters', methods=['DELETE'])
def delMasterList():
    m = request.json['masters']
    for master in m:
        if (master in masters): masters.remove(master)
    return jsonify({"alive": True})


@app.route('/slaves', methods=['DELETE'])
def delSlavesList():
    s = request.json['slaves']
    for slave in s:
        if (slave in slaves): slaves.remove(slave)
    print(slaves)
    return jsonify({"alive": True})

@app.route('/key/<string:key>', methods=['GET'])
def retrieve(key):
    global slaves
    print("func call")
    sorted_hashes, server_hashes = hash_and_sort_servers(slaves)
    server_hashes_where_resource_is_to_be_found = find_correct_server(key, sorted_hashes, repFactor)
    servers_for_search = [server_hashes[s_h] for s_h in server_hashes_where_resource_is_to_be_found]
    print(servers_for_search)
    for server in servers_for_search:
        try:
            response = requests.get(f'http://{server}/key/{key}', timeout=timeout)
            if response.status_code == 200:
                print(f"data successfully retrieved from {server}")
                return response.json(), response.status_code
        except:
            healthCheck(server,"s")

    return jsonify({'error': 'No updated data found'}), 404


@app.route('/key/<string:key>', methods=['POST'])
def insert(key):
    global repFactor
    print("func call")
    #  NBB important il CONTENT-TYPE deve essere application/json
    #  NBB in the header of the request name:'Content-Type' value:'application/json' is required
    data = request.get_json()  # get the json value from the request
    # value = data['value']
    # replication_f = data['rep']
    token = request.headers.get('token')
    # print(token,replication_f,value)
    try:
        tok = s.loads(token)  # deserializing token recieved in the request
    except (SignatureExpired, BadSignature):
        return jsonify({'error': 'Invalid or Expired token'}), 401
    if not tok['admin']:
        #print(tok['admin'])
        return jsonify({'error': 'Admin access required'}), 402
    else:
        #print(tok['admin'])
        sorted_hashes, server_hashes = hash_and_sort_servers(slaves)
        print(server_hashes)
        print(sorted_hashes)
        server_hashes_for_replication = find_correct_server(key, sorted_hashes, repFactor)
        # At this point servers for replication contains the hashes of the servers that need to replicate the data
        servers_for_replication = [server_hashes[s_h] for s_h in server_hashes_for_replication]
        print(servers_for_replication)
        # transform servers_for_replication into a string to send it into the body
        sfr = ' '.join(servers_for_replication)
        # NBB Get requests don't have a body so if u need to insert values u are meant to
        # do a request.post or else u will get a 400 bad request error
        try:
            response = requests.post(f'http://{masters[0]}/key/{key}', headers={'token': token},
                                     json={'value': data['value'], 'servers': sfr}, timeout=timeout)
        except:
            healthCheck(masters[0],"m")
        return response.json(), response.status_code


def hash_and_sort_servers(servers):
    # creating a dict where the key is the hash of the server and the value is the server
    server_hashes = {hashlib.sha256(server.encode('ascii')).hexdigest(): server for server in servers}
    sorted_hashes = sorted(server_hashes.keys())
    return sorted_hashes, server_hashes


def hash_key(key):
    return hashlib.sha256(key.encode('ascii')).hexdigest()


def grab_elements_around(lst, i, r):
    #  this function is used to get the servers that need to replicate the data
    #  it also handles the case in which the server chosen to start replicating is at the end
    #  of the list of servers and the end_idx = i + r is greater than the length of the list
    n = len(lst)
    end_idx = i + r

    if end_idx < n:  # simple case
        return lst[i:end_idx + 1]

    else:
        overflow = end_idx + 1 - n  # special case
        return lst[i - overflow:i] + lst[i:]


def find_correct_server(key, sorted_hashes, repFactor):
    #  this code handles the occasional case where the sliced list is smaller than the repFactor
    #  in that case we need to get the remaining servers from "under" the initial slice
    key_hash = hash_key(key)
    servers_for_replication = []
    for i, server_hash in enumerate(sorted_hashes):  # server_hashes is a dictionary mapping hash to server_hash
        #print(key_hash < server_hash)
        if key_hash < server_hash:
            return grab_elements_around(sorted_hashes, i, repFactor)
    return grab_elements_around(sorted_hashes, len(sorted_hashes)-1, repFactor)

def importIP():
    output = []
    output2 = []
    with open('IP.json') as f:
        data = json.loads(f.read())
    for item in data["slaves"]:
        output.append((item["IP"] + ':' + item["port"]))
    for item in data["masters"]:
        output2.append((item["IP"] + ':' + item["port"]))
    return output, output2


def sendJson(json, receiverList, path):
    for receiver in receiverList:
        try:
            response = requests.post(f'http://' + receiver + path, headers={'Content-Type': 'application/json'},
                                     json=json, timeout=timeout)
        except:
            healthCheck(receiver,"s")

def healthCheck(target=None,label=None):
    if(target != None):
        try:
            response = requests.get(f'http://{target}/heartbeat/', timeout=timeout)
        except:
            fallen[target] = label
        else:
            if(label == "m" and target not in masters): masters.append(target)
            if(label == "s" and target not in slaves): slaves.append(target)
            if(fallen.get(target) != None): fallen.pop(target)
    else:
        for f,l in fallen.copy().items():
            healthCheck(f,l)
        for s in slaves:
            healthCheck(s,"s")
        for m in masters:
            healthCheck(m,"m")
        for f,l in fallen.copy().items():
            if(l == "m" and f in masters): masters.remove(f)
            if(l == "s" and f in slaves): slaves.remove(f)
        print("Slaves list:", slaves)
        print("Masters list:", masters)
        print("Fallen list:",fallen)

def parserInit():
    parser = argparse.ArgumentParser(
        prog='Endpoint Database 2024',
        epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ', '--port', type=int, default=3000)
    parser.add_argument('-f ', '--replicationfactor', type=int, default=1)
    parser.add_argument('-t ', '--timeout', type=int, default=5)
    parser.add_argument('-s ', '--seconds', type=int, default=30)
    return parser.parse_args()

def main():
    global slaves
    global masters
    global fallen
    global timeout
    global keys
    global repFactor
    print('Starting endpoint...')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname)
    args = parserInit()
    timeout = args.timeout
    repFactor = args.replicationfactor
    slaves, masters = importIP()
    fallen = {}
    healthCheck()
    print("Done! Endpoint's ip is: " + IPaddr)
    print("Sending info to masters and slaves...")
    sendJson({'slaves': slaves}, masters, '/slaves')
    sendJson({'masters': masters}, slaves, '/masters')
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(healthCheck, 'interval', seconds=args.seconds)
    scheduler.start()
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
