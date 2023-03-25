'''
Controller da rota clientes
'''

class RawApiController:
    def __init__(self) -> None:
        self._data = dict()

    # Cria um novo cliente
    # time -> data e hora
    # uuid -> UUID do cliente
    def create(self, time:str, uuid:str) -> None:
        self._data[uuid] = dict()
        self._data[uuid][time] = 0

    # Insere uma informacao do cliente
    # time -> data e hora
    # uuid -> UUID do medidor
    # value -> consumo do medidor
    def insert(self, time:str, uuid:str, value:str) -> None:
        self._data[uuid][time] = value
    
    # Devolve todos os clientes da rota
    # em forma de dicionario
    def get_all(self) -> dict:
        return self._data

    # Devolve um medidor especifico
    # uuid -> UUID a ser buscado
    def get(self, uuid:str) -> dict:
        return self._data[uuid]

    # Remove um determinado medidor da rota
    # uuid -> uuid do medidor a ser removido
    def remove(self, uuid:str) -> None:
        del self._data[uuid]