import socket



def init():
    print('Starting endpoint')
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname) 
    print("Done! Endpoint's ip is: " + IPaddr)

def main():
    init()

if __name__ == "__main__":
    main()