import ClienteComandLineInterface

#IP = "localhost"
#IP = "10.65.139.243"
IP = "172.16.103.7"
PORT = 6521

client_cli = ClienteComandLineInterface.ComandLineInterface(IP, PORT)
client_cli.start()
