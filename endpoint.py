import argparse
from flask import Flask, jsonify, request
import json
import requests
import socket
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


"""
ip_port = []

def importIP():
    with open('IP.json') as f:
        data = json.loads(f.read())
    for item in data["slaves"]:
        ip_port.append((item["IP"], item["port"]))
    return ip_port
"""

app = Flask(__name__)
app.config['SECRET_KEY']= 'p4ssword'
s = Serializer(app.config['SECRET_KEY'])


@app.route('/heartbeat')
def heartbeat():
    return jsonify({
        'alive': True
    })


@app.route('/key/<string:key>', methods=['GET'])
def retrieve(key):
    token = request.headers.get('token')
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return jsonify({'error': 'Invalid or Expired token'}), 401

    if not data['user']:
        return jsonify({'error': 'no user recognized'}), 402

    # if user is recognized, and is either admin or not then it can read from slaves
    else:
        # admins can read from slaves and master
        response = requests.get(f'http://slaveserverIP:port/key/{key}', headers={'token': token})
        return response.json(), response.status_code


@app.route('/key/<string:key>', methods=['POST'])
def insert(key):
    value = request.json['value']
    token = request.headers.get('token')
    try:
        data = s.loads(token)   # deserializing token recieved in the request
    except (SignatureExpired, BadSignature):
        return jsonify({'error': 'Invalid or Expired token'}), 401

    if not data['admin']:
        return jsonify({'error': 'Admin access required'}), 402
    else:
        response = requests.get(f'http://masterserverIP:port/key/{key}', headers={'token': token}, json={'value': value})
        return response.json(), response.status_code


def parserInit():
    parser = argparse.ArgumentParser(
                    prog='Endpoint Database 2024',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ',  '--port', type=int, default=5000)
    parser.add_argument('-f ',  '--replicationfactor', type=int, default=3)
    return parser.parse_args()


def main():
    print('Starting endpoint')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    parser = parserInit()
    print("Done! Endpoint's ip is: " + IPaddr)
    app.run(host=IPaddr, port=parser.port)


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