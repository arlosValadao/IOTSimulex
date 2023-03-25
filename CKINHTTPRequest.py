'''
Classe que representa em forma de objeto
os atributos mais importantes de uma requisicao
CKINHTTP
'''

class CKINHTTPRequest:
    def __init__(self) -> None:
        self._header: str = None
        self._data: str = None
        self._time: str = None

    def get_header(self) -> str:
        return self._header
    
    def set_header(self, header:str) -> None:
        self._header = header
    
    def get_data(self) -> str:
        return self._data
    
    def set_data(self, data:str) -> None:
        self._data = data
    
    def get_time(self) -> str:
        return self._time
    
    def set_time(self, time) -> None:
        self._time = time