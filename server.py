import socket
import json

HOST = '192.168.15.148'
PORT = 12000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print('Waiting connection...')

while True:
  conn, addr = server.accept()
  print('Connected in {}'.format(addr))

  while True:
    data = conn.recv(1024).decode()
    if data == 'send_json':
      break

  with open('data.json', 'r') as file:
    json_data = json.load(file)

  json_str = json.dumps(json_data).encode('utf-8')
  conn.sendall(json_str)
  conn.close()
  print('Message sent successfully!')

