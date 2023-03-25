import API

#IP = "10.65.137.254"
#IP = "localhost"
#IP = "10.65.139.243"
#IP = "221.1.1.131"
IP = "0.0.0.0"
PORT = 6521

myapi = API.SoftAPI(IP, PORT)
myapi.create_get("clientes", "RawApiController")
myapi.create_server()
myapi.server_on()
