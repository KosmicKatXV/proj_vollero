start cmd /k python auth_server.py
start cmd /k python master.py
start cmd /k python slave.py -p 4000
start cmd /k python slave.py -p 4001
start cmd /k python slave.py -p 4002
start cmd /k python endpoint.py