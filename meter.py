import Medidor
import threading

#IP = "10.65.137.254" #UEFS VISITANTES
#IP = "localhost"
#IP = "10.65.139.243"
#IP = "127.0.0.1"
IP = "172.16.103.7"
PORT = 6521

mymeter = Medidor.Medidor(IP, PORT)
t1 = threading.Thread(target=mymeter.start)
t2 = threading.Thread(target=mymeter.meter_interface)

t1.start()
t2.start()

t1.join()
t2.join()
