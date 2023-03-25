from json import dumps
import consts
from socket import socket, AF_INET, SOCK_STREAM
import Tools
import HttpHeaderParser
import CKINHTTPParser
import CKINHTTPRequest
from uuid import uuid4
import HTTPRequest
from ControllerRawAPI import RawApiController
import threading


'''
Classe que representa uma API utilizada em uma rede IOT
de medidores. Capaz de lidar com conexoes simultaneas
e que se comporta como REST e não-rest.
Alem de conexoes HTTP a API lida com requisicoes CKINHTTP
'''


class SoftAPI:
    def __init__(self, addr:str, port:int) -> None:
        self._addr:str = addr
        self._port:int = port
        self._socket:socket = None
        self._routes:dict = dict()
        self._boxes = dict()
        self._raw_api_controller:RawApiController = RawApiController()

    
    # Responde uma mensagem no estilo CKINHTTP
    # ckinhttp_request -> mensagem do tipo CKINHTTP
    # conn -> conexao do cliente
    def response_ckisnhttp(self,ckinhttp_request: CKINHTTPRequest.CKINHTTPRequest, conn:socket) -> None:
        ckinhttp_request_header = ckinhttp_request.get_header()
        if ckinhttp_request_header == consts.CKINHTTP_CREATE:
            uuid = str(uuid4())
            header_response_create = 'OK\n' + 'UUID: ' + uuid
            self.register_meter(uuid, ckinhttp_request.get_time())
            conn.send(header_response_create.encode())
            return
        return self.insert_meter_data(
            ckinhttp_request_header,
            ckinhttp_request.get_data(),
            ckinhttp_request.get_time()
        )

    # Instancia um socket TCP do tipo server
    def create_server(self) -> None:
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind((self._addr, self._port))
        self._socket.listen()

    # Torna disponível a API 
    def server_on(self) -> None:
        print("listenning on", self._port)
        client_socket, addr = self._socket.accept()
        print("someone connect")
        threading.Thread(target=self.server_on).start()
        client_request = client_socket.recv(consts.DEFAULT_TCP_BYTES).decode()
        if Tools.request_type(client_request) == consts.CKINHTTP_PROTOCOL:
            return self.response_ckisnhttp(CKINHTTPParser.ckinhttp_header_parser(client_request), client_socket)
        return self.response_http(HttpHeaderParser.http_header_parser(client_request), client_socket)
    
    # Cria uma rota que suporta o metodo HTTP GET
    # new_route -> rota a ser criada
    # controller -> controller da rota
    def create_get(self, new_route:str, controller:str) -> None:
        self._routes[new_route] = ([consts.HTTP_METHOD_GET], eval(controller + '()'))


    # Cria uma rota que suporta o metodo HTTP POST
    # new_route -> rota a ser criada
    # controller -> controller da rota
    def create_post(self, new_route:str, controller:str) -> None:
        self._post_routes[new_route] = ([consts.HTTP_METHOD_POST], eval(controller + '()'))

    # Registra um medidor
    # uuid -> UUID do medidor
    # time -> data e hora do registro do medidor
    def register_meter(self, uuid:str, time:str) -> None:
        meter_controller = self._get_controller(consts.METER_API_ROUTE)
        meter_controller.create(time, uuid)

    # Insere informacoes provindas do medidor
    # uuid -> UUID do medidor
    # consumption -> consumo do medidor
    # time -> data e hora do envio da requisicao
    def insert_meter_data(self, uuid:str, consumption:str, time:str) -> None:
        meter_controller = self._get_controller(consts.METER_API_ROUTE)
        meter_controller.insert(time, uuid, consumption)
        print(meter_controller.get(uuid))
              

    # Retorna o controller de uma determinada rota
    # route -> rota donde o controller sera extraido
    def _get_controller(self, route:str) -> object:
        routes = self._routes[route]
        print(route)
        return routes[1]


    # Responde uma requisicao HTTP de forma adequada
    # http_request -> requisicao HTTP
    # client_socket -> conexao do cliente
    def response_http(self, http_request:HTTPRequest.SimpleHttpRequest, client_socket:socket) -> None:
        http_method = http_request.get_method()
        if http_request.get_path() == 'faturas':
            path = 'clientes'
        else:
            path = http_request.get_path()
        if http_method in self._supported_http_methods(path):
            match http_method:
                case consts.HTTP_METHOD_GET:
                    return self._response_http_get(http_request, client_socket)
                case consts.HTTP_METHOD_POST:
                    return
                case consts.HTTP_METHOD_PUT:
                    return
                case consts.HTTP_METHOD_DELETE:
                    return


    # Retornatodos os metodos que determinada rota suporta
    # route -> rota a ser verificada
    def _supported_http_methods(self, route:str) -> list:
        print(self._routes[route][0])
        return self._routes[route][0]

    # 9000 in 29000 out

    # Responde uma requisicao HTTP GET de forma adequada
    # http_request -> requisicao HTTP GET
    # client_socket -> conexao do cliente
    def _response_http_get(self, http_request:HTTPRequest.SimpleHttpRequest, client_socket:socket) -> None:
        route = http_request.get_path()
        query_params = http_request.get_query_params()
        print(route)
        if route == 'faturas':
            route = 'clientes'
        route_controller = self._get_controller(route)
        if query_params:
            client_uuid = query_params.split('=')[1]
            client_data = route_controller.get(client_uuid)
            if http_request.get_path() ==  'faturas':
                #chamar a funcao de calcular a fatura
                price = self._generate_price(client_data)
                response_json = '{\n\t"uuid": ' + f'"{client_uuid}"' + ',\n\t"valor": ' + f'"{price}"' + '\n}'
            else:
                response_json = Tools.format_http_json(client_data)
            client_socket.send((consts.HTTP_HEADER_RESPONSE + response_json).encode())
            return
        client_data = route_controller.get_all()
        response_json = Tools.r_format_http_json(client_data)
        client_socket.send((consts.HTTP_HEADER_RESPONSE + response_json).encode())            


    # Verifica se uma determinada rota aceita um determinado metodo http
    # routes -> rotas disponiveis na API
    # route -> rota a ser verificada
    # http_method -> metodo http a ser verificado
    # True caso route em routes suporte http_method. False caso contrario
    def route_accepts(self, routes:dict, route:str, http_method:str) -> bool:
        route_methods = routes.get(route, False)
        if route_methods and http_method in route_methods:
            return True
        return False

    # Retorna a rota de path
    # path -> rota correspondente a path
    def _get_route(self, path:str) -> dict:
        return self._routes.get(path, {})
    
    # Calcula o valor da fatura do cliente, ate o momento
    def _generate_price(self, consumptions:dict) -> str:
        return str(int(list(consumptions.values())[-1]) * 4)