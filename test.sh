konsole -e python3 auth_server.py &
konsole -e python3 master.py &
konsole -e python3 slave.py -p 4000 &
konsole -e python3 slave.py -p 4001 &
konsole -e python3 slave.py -p 4002 &
konsole -e python3 endpoint.py &