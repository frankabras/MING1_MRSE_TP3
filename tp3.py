import network, socket
from machine import Pin, Timer
from time import sleep
from tp3_util import * #Fichier avec fonctions pour le code

"""********************* Configuration GPIO **********************"""
led = Pin(2, Pin.OUT) #Config en sortie de la pin de la led 
led.value(True)       #Mise de la led à l'état bas

"""********************** Configuration Wlan **********************"""
#Configuration du Wlan en mode station
wlan = network.WLAN(network.STA_IF)
#Activation du WiFi
wlan.active(True)

"""********************* Configuration Timer **********************"""
#Création d'un objet Timer
timer = Timer(0)
new_data_submission = False
#Fonction d'interruption du Timer
def new_data_to_be_send(timer):
    global new_data_submission
    new_data_submission = True
        
"""************************ Main program **************************"""
#Connexion au WiFi
wlan_connection(wlan, led)

#Node-RED - http://127.0.0.1:1880/ui
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    tcp_socket.connect(('192.168.0.148', 8585))
    udp_socket.connect(('192.168.0.148', 8586))
except Exception as e:
    sockets_connected = False
    print("An exception occurred:", e)
else:
    sockets_connected = True
    #Initialisation de la fréquence d'interruption du timer (en Hz)
    timer.init(freq=5, mode=Timer.PERIODIC, callback=new_data_to_be_send)


#Boucle d'envoie des données
n = 1
while n <= 20 and sockets_connected == True :
    if new_data_submission == True:
        try:
            tcp_socket.send(bytes('%s' % (str(n)), 'utf8'))
            udp_socket.send(bytes('%s' % (str(n)), 'utf8'))
        except Exception as e:
            print("An exception occurred before the end of operations:", e)
            print("Number of subssion :",(n-1))
            tcp_socket.close()
            udp_socket.close()
            break
        else:
            n=n+1
            new_data_submission = False
