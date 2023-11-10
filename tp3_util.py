import network
import uping
from secrets import * #SSID and PSWD for WiFi

#Fonction de gestion de la connexion
def wlan_connection(wlan, led):        
    for attempt in range(4): #Tente 5x de se connecter au WiFi
        try:
            #Connexion au point d'accès
            wlan.connect(my_secrets["home1_ssid"],my_secrets["home1_pswd"])
            #Ping de google afin de vérifier la connexion
            uping.ping('google.com')
        except:
            #Led éteinte
            led.value(True)
            #Permet de recommencer si le Try échoue
            continue
        else:
            #Affichage informations sur la connexion dans le terminal
            # IP, masque, passerelle et DNS
            print(wlan.ifconfig())
            #Allumage constant de la led
            led.value(False)
            break
    else:
        print("Not connected")
        
