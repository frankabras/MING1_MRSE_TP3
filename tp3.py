import network, socket, utime
from machine import Pin
from tp3_util import * #Fichier avec fonctions pour le code

"""********************* Configuration GPIO **********************"""
led = Pin(2, Pin.OUT) #Config en sortie de la pin de la led 
led.value(True)       #Mise de la led à l'état bas

"""********************** Configuration Wlan **********************"""
#Configuration du Wlan en mode station
wlan = network.WLAN(network.STA_IF)
#Activation du WiFi
wlan.active(True)
        
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


#Boucle d'envoie des données
start_time = utime.ticks_ms() #Récupération du temps de départ
n = 1
while n <= 20 and sockets_connected == True :
    #Comparaison temps actuel et du temps de départ
    if utime.ticks_diff(utime.ticks_ms(),start_time)>=20: #50Hz
        try:
            #Écriture de la donnée qui ser envoyée
            data = '%d\n' % n
            #Envoie des données successivement via TCP puis UDP
            tcp_socket.send(data.encode())
            udp_socket.send(data.encode())
        except Exception as e:
            print("An exception occurred :", e)
            break
        else:
            #Incrémentation de la variable envoyée
            n=n+1
            #Récupération du nouveau temps initial
            start_time = utime.ticks_ms()

#Fermeture des sockets
tcp_socket.close()
udp_socket.close()