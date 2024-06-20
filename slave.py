import socket



def init():
    print('Starting slave database')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    print("Done! Slave's ip is: " + IPaddr)

def main():
    init()

if __name__ == "__main__":
    main()
