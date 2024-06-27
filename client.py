import requests
import base64
import json

auth_server_url = 'http://192.168.56.1:5005/token'
endpoint_url = 'http://192.168.56.1:3000/key/'

# auth server
username = input('Enter your username: ')
password = input('Enter your password: ')
string = username + ':' + password
string_bytes = string.encode('ascii')
string_bytes_b64 = base64.b64encode(string_bytes)
string_b64 = string_bytes_b64.decode('ascii')

headers = {'Authorization': f'Basic {string_b64}'}
auth_response = requests.post(auth_server_url, headers=headers)
print(auth_response.json())

while (True):
    option = input('Do you want to put or receive a file? (p/r): ')
    match option:
        case "p":
            # endpoint POST
            token = auth_response.json()['token']
            key = input('Enter the key: ')
            value = input('Enter the value: ')
            headers = {'Content-Type': 'application/json', 'token': token}
            body = {'value': value}

            endpoint_response = requests.post(endpoint_url + f'{key}', headers=headers, json=body)
            print(endpoint_response.json())

        case "r":
            # endpoint GET
            key = input('Enter the key: ')
            headers = {'Content-Type': 'application/json'}

            endpoint_response = requests.get(endpoint_url + f'{key}', headers=headers)
            print(endpoint_response.json())

        case "q":
            exit(-1)

        case _:
            continue
