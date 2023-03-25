from CKINHTTPRequest import CKINHTTPRequest

# Realiza o parsing em uma requisicao CKINHTTP
# ckinhttp_header -> requisicao CKINHTTP
# Devolve um objeto CKINHTTPRequest
def ckinhttp_header_parser(ckinhttp_header:str) -> CKINHTTPRequest:
    print(ckinhttp_header)
    ckinhttp_request = CKINHTTPRequest()
    lst_ckinhttp_header = ckinhttp_header.split('\n')
    print(lst_ckinhttp_header)
    header, data = lst_ckinhttp_header[0].split(': ')
    ckinhttp_request.set_header(header)
    ckinhttp_request.set_data(data)
    ckinhttp_request.set_time(lst_ckinhttp_header[1].split(": ")[1])
    return ckinhttp_request