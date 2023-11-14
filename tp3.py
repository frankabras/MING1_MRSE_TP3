import network, socket
from machine import Pin, Timer
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

#Initialisation des sockets TCP et UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Tentative de connection vers node-red
try:
    tcp_socket.connect(('192.168.0.148', 8585))
    udp_socket.connect(('192.168.0.148', 8586))
except Exception as e:
    sockets_connected = False
    print("An exception occurred:", e)
else:
    sockets_connected = True
    #Initialisation de la fréquence d'interruption du timer (en Hz)
    timer.init(freq=50, mode=Timer.PERIODIC, callback=new_data_to_be_send)


#Boucle d'envoie des données
n = 1
while n <= 40 and sockets_connected == True :
    if new_data_submission == True:
        data = '%s\n' % (str(n))
        try:
            #Envoie des données successivement via TCP puis UDP
            tcp_socket.send(bytes(data, 'utf8'))
            udp_socket.send(bytes(data, 'utf8'))
        except Exception as e:
            print("An exception occurred :", e)
            break
        else:
            n=n+1
            data = ""
            new_data_submission = False

#Fermeture des sockets      
tcp_socket.close()
udp_socket.close()