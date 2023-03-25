from socket import socket, SOCK_STREAM, AF_INET
import consts
import Tools
from random import random, uniform, randint
from time import sleep
from sys import exit


'''
Representa um medidor e todas as suas funcionalidades
Cadastro
Envio de consumo
Interface
'''


class Medidor:
    def __init__(self, addr, port) -> None:
        self._socket:socket = None
        self._addr:str = addr
        self._port:int = port
        self._uuid:str = None
        self._consumption:int = 0
        self._consumption_factor:int = 1
        sleep(random())
        self._self_register()

    
    # Fecha uma conexao TCP previamente estabelecida
    def _close_connection(self) -> None:
        self._socket.close()


    # Cria uma conexao TCP socket na porta e endereco especificados
    # em __init__
    def _connect(self) -> None:
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.connect((self._addr, self._port))


    # Envia uma requisicao CKINHTTP Insert para a API
    # Devolve o cabecalho de resposta em forma de string
    def _send_insert_ckinhttp(self) -> str:
        now = Tools.now()
        ckinhttp_insert_header = self._uuid + ': ' + str(self._consumption) + '\nTime: ' + now
        self._connect()
        self._socket.send(ckinhttp_insert_header.encode())
        recv = self._socket.recv(consts.DEFAULT_TCP_BYTES).decode()
        self._close_connection()
        return recv

    # Envia uma requisicao CKINHTTP Init (registro)
    # Devolve o cabecalho de resposta em forma de string
    def _send_init_ckinhttp(self) -> str:
        now = Tools.now()
        ckinttp_register_header = consts.CKINHTTP_CREATE_HEADER + 'Time: ' + now
        self._connect()
        self._socket.send(ckinttp_register_header.encode())
        recv = self._socket.recv(consts.DEFAULT_TCP_BYTES).decode()
        self._close_connection()
        return recv
    

    # Faz um auto-registro com base no UUID devolvido pela API
    def _self_register(self) -> None:
        ckinhttp_response = self._send_init_ckinhttp()
        print("RESPOSTA", ckinhttp_response)
        self._uuid = ckinhttp_response.split('\n')[1][6:]
        print(ckinhttp_response.split('\n')[1][6:])
    
    # getter
    def get_uuid(self) -> str:
        return self._uuid
    
    # Simula o consumo e o envio do consumo para o
    # servidor
    def start(self) -> None:
        print(self._uuid)
        while 1:
            self.detect_consumption()
            self._send_consumption()

    
    # Envia o consumo do medidor por meio
    # de uma requisicao CKINHTTP 
    # um apelido para uma messagem simples usando socket
    # Ver -> self._send_insert_ckinhttp
    def _send_consumption(self) -> None:
        self._send_insert_ckinhttp()


    # Simula o consumo do cliente por meio do uso de funcoes
    # de geracao de numeros pseudos aleatorios
    def detect_consumption(self) -> None:
        sleep(uniform(0.0, 3))
        self._consumption += self._consumption_factor


    # getter
    def get_consumption(self) -> int:
        return self._consumption


    # Interface do medidor que permite o incremento
    # e decremento do consumo em runtime
    def meter_interface(self) -> None:
        while True:
            choice = self._interface_menu()
            if choice == 1:
                consumption_factor = randint(6, 10)
                print("\t\t\tAumentando o consumo...")
                self._consumption_factor = consumption_factor
            elif choice == 2:
                self._consumption_factor -= 1
                if self._consumption_factor < 0:
                    self._consumption_factor = 0
                print("\t\tReduzindo o consumo...")
            sleep(1)
            Tools.clear_scr()


    # Menu a ser exibido ao iniciar a interface
    # do medidor
    def _interface_menu(self) -> None:
        print('\t\t' + '-------------[!] - Interface Medidor - [!]-------------')
        print('\t\t[1] - Aumentar consumo')
        print('\t\t[2] - Reduzir consumo')
        return int(input("\t\t> "))