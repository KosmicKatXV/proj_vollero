# Project Title: Distributed Database System

This project is a distributed database system with consistent hashing implemented in Python. It consists of multiple components including an authentication server, master server, slave servers, and a client. The system uses Flask for handling HTTP requests and SQLite for database management.

## Components

### Authentication Server (`auth_server.py`)
This server handles user authentication and token generation. It is responsible for verifying the user's credentials and issuing a token that must be included in all subsequent requests.

### Master Server (`master.py`)
The master server manages the slave servers and handles data replication. It receives write requests from the client, writes the data to its own database, and then sends the data to the appropriate slave servers for replication.

- `heartbeat()`: This function responds to a GET request to confirm that the server is running.
- `getSlavesList()`: This function updates the list of slave servers when a POST request is received.
- `delSlavesList()`: This function removes servers from the list of slave servers when a DELETE request is received.
- `insert()`: This function handles POST requests to insert data into the database and replicate it to the slave servers.

### Slave Servers (`slave.py`)
These servers store the actual data and handle read/write requests from the client. They receive data from the master server for replication and serve data to the client for read requests.

### Client (`client.py`)
The client interacts with the system by sending HTTP requests via the endpoint. The client must first authenticate with the authentication server to receive a token. This token must be included in all subsequent requests.

- The client script prompts the user for their username and password, then sends a POST request to the authentication server to receive a token.
- The client then prompts the user to either put or receive a file. Depending on the user's choice, it sends a POST or GET request to the endpoint server.

### Endpoint (`endpoint.py`)
The endpoint is responsible for handling the client's requests and directing them to the appropriate servers. It uses a consistent hashing mechanism to determine which servers should store a given piece of data. When a write request is received, the endpoint hashes the key of the data item and uses this hash to determine which servers should store the data. The data is then sent to these servers for replication. The endpoint also periodically performs a health check on all servers to ensure they are functioning correctly.

- `heartbeat()`: This function responds to a GET request to confirm that the server is running.
- `getMasterList()`, `getSlavesList()`: These functions update the list of master and slave servers when a POST request is received.
- `delMasterList()`, `delSlavesList()`: These functions remove servers from the list of master and slave servers when a DELETE request is received.
- `retrieve()`: This function handles GET requests to retrieve data from the appropriate slave server.
- `insert()`: This function handles POST requests to insert data into the database and replicate it to the appropriate slave servers.

## Database Handling

The system uses SQLite databases for data storage. Each server (master and slaves) has its own database. When a write request is received, the data is written to the master server's database and then replicated to the appropriate slave servers' databases. When a read request is received, the data is retrieved from the appropriate slave server's database.

## Hashing and Replication

The endpoint uses a consistent hashing mechanism to determine which servers should store a given piece of data. When a write request is received, the endpoint hashes the key of the data item and uses this hash to determine which servers should store the data. The data is then sent to these servers for replication. This ensures that data is evenly distributed across all servers and that the system can continue to function even if some servers fail.

## Health Check

The endpoint periodically performs a health check on all servers to ensure they are functioning correctly. If a server fails the health check, it is removed from the list of active servers. If a server passes the health check, it is added back to the list of active servers. This ensures that the system can continue to function even if some servers fail.

## Admin Responsibilities

The admin is responsible for monitoring the endpoint for any potential errors. Since the endpoint is the intermediary between the client and the rest of the system, it is crucial for the admin to ensure that the endpoint is functioning correctly. The admin should regularly check the endpoint's logs and handle any errors that may occur. The admin should also ensure that the endpoint is correctly directing requests to the appropriate servers and that data is being correctly replicated across the servers.
