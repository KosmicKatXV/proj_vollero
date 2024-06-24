rm *.db
konsole -e python3 auth_server.py &
konsole -e python3 master.py &
konsole -e python3 slave.py -p 4000 -d "slave1.db" &
konsole -e python3 slave.py -p 4001 -d "slave2.db" &
konsole -e python3 slave.py -p 4002 -d "slave3.db" &
konsole -e python3 endpoint.py &