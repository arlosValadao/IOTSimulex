from socket import socket, AF_INET, SOCK_STREAM
import consts
import Tools
from HttpHeaderParser import http_response_header_parser

'''
A interface de linha de comando do cliente permite que ele veja o seu consumo atual
Bem como o seu historico de consumo, ver a sua fatura, e alertar o cliente sobre um consumo
excessivo ou quando houver uma grande variacao de valor na conta do usuario

A interface funcionara por meio de requisicoes http para a API, dessa forma
ela tratara as informacoes da API e exibira estas para o usuario
'''

class ComandLineInterface:
    def __init__(self, addr:str, port:int) -> None:
        self._addr:str = addr
        self._port:int = port
        self._socket:socket = None
        self._uuid:str = None
        self._warning:str = None


    # Envia uma mensagem via socket para addr:ip
    # message -> mensagem a ser enviada
    # Devolve a resposta em forma de string
    def _send(self, message:str) -> str:
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.connect((self._addr, self._port))
        self._socket.send(message.encode())
        response = self._socket.recv(consts.MAX_TCP_BYTES).decode()
        self._socket.close()
        return response
    

    # Realiza o login do usuario pedindo o seu UUID
    def _login(self) -> str:
        print('- '*30)
        print('\t\tLOGIN')
        print('- '*30)
        uuid = input("\t[!] - Insira o seu UUID -> ")
        Tools.clear_scr()
        return uuid.strip().lower()
    

    # Exibe o menu principal da interface do usuario
    # e o aviso de consumo exacerbado
    # Devolve a escolha do usuario em forma de inteiro
    def _menu(self) -> str:
        self._get_warning()
        st = '- ' * 10
        print(st*4)
        print('\t\t\tBEM VINDO')
        print(st*4)
        print(self._warning, end='')
        print(st + 'Interface De Usuário ' + st)
        print(st*4)
        print("\t[1] - Histórico de Consumo")
        print("\t[2] - Fatura até o momento")
        print('\t[3] - Sair do programa')
        choice = int(input("\t> "))
        Tools.clear_scr()
        return choice
    

    # Executa todas as funcionalidades da interface
    def start(self) -> None:
        self._uuid = self._login()
        while True:
            self._get_warning()
            choice = self._menu()
            if choice == 1:
                self._show_consumption_history(self._get_consumption_history())
            elif choice == 2:
                self._show_invoice()
            elif choice == 3:
                exit(0)
            else:
                continue


    # Verifica o consumo de self._uuid e altera self._warning
    # indicando um alerta ou ao
    def _get_warning(self) -> None:
        client_consumption = self._get_consumption_history()
        l_client_consumption = tuple(client_consumption.values())
        if len(l_client_consumption) < 6:
            self._warning = ''
        last_consumption = int(l_client_consumption[-1])
        geometric_mean = Tools.geometric_mean(l_client_consumption[-6:-1])
        if (last_consumption - geometric_mean) > 20:
            self._warning = '\t[ ALERTA ] -> O seu consumo está fora do normal! <- [ ALERTA ]\n' + '- '*40 + '\n'
        else:
            self._warning = ''


    # Devolve o historico de consumo do UUID informado
    # em self._login(), em forma de dicionario
    def _get_consumption_history(self) -> dict:
        path = '/' + consts.METER_API_ROUTE
        query = '?uuid=' + self._uuid
        method = consts.HTTP_METHOD_GET
        header_request_http = Tools.make_http_request_header(method, path=path, query=query)
        response = self._send(header_request_http)
        http_parser = http_response_header_parser(response)
        return http_parser.get_data()


    # Exibe na tela o historico de consumo de self._uuid
    # history -> historico de consumo
    def _show_consumption_history(self, history:dict) -> None:
        history_v = list(history.values())[-1]
        print('-'*30)
        print("\t\tSeu consumo Atual -> " + history_v + "KWH")
        print('\t\tHistorico de Consumo')
        print('[Data]\t     [Hora]', end='\t')
        print("  [Consumo]")
        for key, value in history.items():
            data, hora = key.split(' ')
            data = data.replace('-', '/')
            hora = hora.replace('-', ':')
            print(data + '  ' + hora + '\t' + value + ' KWH')
        print('-'*30)
        input('<ENTER>')
        Tools.clear_scr()


    # Devolve a fatura de self._uuid, em forma de dicionario
    def _get_invoice(self) -> dict:
        path = '/faturas'
        query = '?uuid=' + self._uuid
        method = consts.HTTP_METHOD_GET
        header_request_http = Tools.make_http_request_header(method, path=path, query=query)
        response = self._send(header_request_http)
        http_request = http_response_header_parser(response)
        return http_request.get_data()


    # Exibe a fatura de self._uuid na tela
    def _show_invoice(self) -> None:
        invoice = self._get_invoice()
        print('-'*50)
        print('\t\tFatura')
        print('-'*50)
        print('\tID: ' + self._uuid)
        print('\tValor: ' + invoice['valor'] + ' R$')
        print('-'*50)
        input('<ENTER>')
        Tools.clear_scr()