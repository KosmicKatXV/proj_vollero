import socket

def parserInit():
    parser = argparse.ArgumentParser(
                    prog='Slave Database 2024',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-p ',  '--port',      type=int)
    return parser.parse_args()

def init():
    print('Starting master database')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    print("Done! Master's ip is: " + IPaddr)

def main():
    init()

if __name__ == "__main__":
    main()