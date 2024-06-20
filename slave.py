import socket
import argparse

def parserInit():
    parser = argparse.ArgumentParser(
                    prog='Slave Database 2024',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ',  '--port',      type=int)
    return parser.parse_args()

def prinTinit():
    app = Flask(__name__)
    print('Starting slave database')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    print("Done! Slave's ip is: " + IPaddr)

def main():
    printInit()

@app.route('/key/<string:key>',methods=['GET'])
def retrieve(key):
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
