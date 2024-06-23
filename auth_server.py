from flask import Flask, jsonify, request
import socket
import argparse
from itsdangerous import URLSafeTimedSerializer as Serializer
# TimedJSONWebSignatureSerializer is a class that allows us to create and verify a JSON web Token


app = Flask(__name__)
app.config['SECRET_KEY'] = 'p4ssword'
# for enconding and decoding the token

# create instance of Serializer with exp time of 900 secs (15 mins)
s = Serializer(app.config['SECRET_KEY'], expires_in=900)


@app.route('/token', methods=['POST'])  # POST method because sensitive info
def get_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    if auth.password == '4dmin':
        token = s.dumps({'user': auth.username, 'admin': True}).decode('utf-8')
        return jsonify({'token': token, 'message': 'Token created, admin access granted', 'username': auth.username})
    else:
        token = s.dumps({'user': auth.username, 'admin': False}).decode('utf-8')
        return jsonify({'token': token, 'message': 'Token not granted', 'username': auth.username})


def parserInit():
    parser = argparse.ArgumentParser(
                    prog='Endpoint Database 2024',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ',  '--port', type=int, default=5005)
    return parser.parse_args()


def main():
    print('Starting auth server...')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname)
    parser = parserInit()
    print("Done! Auth server's ip is: " + IPaddr)
    app.run(host=IPaddr, port=parser.port)


if __name__ == '__main__':
    main()

# THESE COMMENTS ARE TO CORRECTLT MAKE A REQUEST TO THE AUTH SERVER
"""
To test your auth_server.py follow these steps:  
Run your auth_server.py script. This will start your Flask server.
Open the RESTED extension in your browser.
Set the HTTP method to POST.
In the URL field, enter the URL of your /token endpoint. This will be http://<your-server-ip>:<your-server-port>/token.
In the Headers section, add a new header with the name Authorization and the value Basic <credentials>. 
Replace <credentials> with the Base64-encoded string of your username and password, formatted as username:password. 
For example, if your username is admin and your password is 4dmin, the Base64-encoded string would be YWRtaW46NGRtaW4=.
Click on the Send button to send the request
"""
