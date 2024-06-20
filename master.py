import socket



def init():
    print('Starting master database')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    print("Done! Master's ip is: " + IPaddr)

def main():
    init()

if __name__ == "__main__":
    main()