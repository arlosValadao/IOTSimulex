from typing import Final

'''
Este arquivo define constantes relacionadas aos protrocolos
HTTP e CKINHTTP que sao utilizadas em API.py e em Medidor.py
'''

DEFAULT_TCP_BYTES: Final = 1024
MAX_TCP_BYTES: Final = 65535
HTTP_HEADER_RESPONSE: Final = 'HTTP/1.1 200 OK\r\n\r\n'
#HTTP_HEADER_REQUEST: Final = 'GET / HTTP/1.1\r\n \
#                            Host: localhost:8888\r\n \
#                            User-Agent: PBL_REDES_P1/2023.1\r\n \
#                            Accept: */*\r\n\r\n'

# Versao do HTTP aceita pela API
ACCEPT_HTTP_VERSION: Final = 1.1

# Metodos HTTP
HTTP_METHOD_GET: Final = "GET"
HTTP_METHOD_POST: Final = "POST"
HTTP_METHOD_PUT: Final = "PUT"
HTTP_METHOD_DELETE: Final = "DELETE"
INVALID_HTTP_METHOD: Final = "UNKNOW"

# Nome protocolo HTTP
HTTP_PROTOCOL: Final = "HTTP"

# Rota que guarda as faturas de todos os
# clientes
METER_TAX: Final = "faturas"

# Protocolo CKINHTTP
CKINHTTP_PROTOCOL: Final = "CKINHTTP"
CKINHTTP_CREATE: Final = "Init"
CKINHTTP_INSERT: Final = "Insert"

# Cabecalho de init de CKINHTTP
CKINHTTP_CREATE_HEADER: Final = "Init: <>\n"

# WARNING: do not touch this if you don't have no idea what do
# Os dados vindouros dos medidores serao depositados nesta rota,
METER_API_ROUTE: Final = "clientes"