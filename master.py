import socket
import argparse
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/hearbeat', methods=['GET'])
def heartbeat():
    return jsonify({"alive": True})


def parserInit():
    parser = argparse.ArgumentParser(
        prog='Master Database 2024',
        epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ', '--port', type=int, default=5000)
    return parser.parse_args()


def init():
    app = Flask(__name__)
    print('Starting master database')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname)
    print("Done! Master's ip is: " + IPaddr)
    return IPaddr


def main():
    args = parserInit()
    IPaddr = init()
    app.run(host=IPaddr, port=args.port)

@app.route('/key/<string:key>',methods=['POST'])
def insert(key):
    value = value.query.filter(User.id == user_id).one_or_none()        
    if value is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'value': value.format()
    })


if __name__ == "__main__":
    main()
