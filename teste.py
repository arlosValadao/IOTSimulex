from socket import socket, AF_INET, SOCK_STREAM
import HttpHeaderParser

teste2 = 'HTTP/1.1 200 OK\r\n \
        Access-Control-Allow-Origin: *\r\n \
        Content-Type: application/json; charset=utf-8\r\n\r\n \
        {\n\t"teste":"Oi"\n}'

teste3 = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 19\r\n\r\n{\n\t"Teste": "oi"\n}'

teste4 = 'HTTP/1.1 200 OK\r\n\r\n'

HOST = "localhost"
PORT = 8888
MAX_CONNECTIONS = 1

from json import loads

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_CONNECTIONS)
print("listenning on port", PORT)
conn, addr = server.accept()
print(type(conn))
content = conn.recv(1024).decode()
http_parser = HttpHeaderParser.http_header_parser(content)
print(http_parser.get_method())
print(http_parser.get_path())
print(http_parser.get_query_params())