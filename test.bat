:: This is a batch file to start all the servers. It has to be run on CMD not on PS

del /S *.db
start cmd /k python auth_server.py
start cmd /k python master.py
start cmd /k python slave.py -p 4000 -d "slave1.db"
start cmd /k python slave.py -p 4001 -d "slave2.db"
start cmd /k python slave.py -p 4002 -d "slave3.db"

timeout /t 10 /nobreak >nul
start cmd /k python endpoint.py -f 1
start cmd /k python client.py