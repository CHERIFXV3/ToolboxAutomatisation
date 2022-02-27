#!/usr/bin/python3.8

# le package utilisé est speedtest-cli(c'est le seul package qu'on a besoin) apt-get install speedtest-cli
import speedtest
import pyfiglet
from time import sleep
speed=speedtest.Speedtest()

ascii_banner = pyfiglet.figlet_format("SpeedTest Connection")
print(ascii_banner)

option=int(input('''
Que voulez-vous savoir:
1) La vitesse de Download
2) La vitesse d'Upload
3) La vitesse de Download et d'Upload à la fois
4) Le Ping
Ton choix: '''))

if option<1 or option>4:
    sleep(2)
    print('\nVous avez entré un mauvais choix!\nVeuillez donc svp entrer à nouveau votre choix avec une valeur comprise entre 1 et 4\n')
else:
    sleep(1)
    print()
    print('Veuillez attendre svp, test en cours...')
    print()
    down_speed=round(speed.download()/1000000,3)
    up_speed=round(speed.upload()/1000000,3)
    print('Une seconde de plus svp...')
    sleep(2.5)
    print()
    if option == 1:
        print('Votre vitesse de Download est de: ',down_speed,'Mbps')
    elif option == 2:
        print('Votre vitesse de Upload est de: ',up_speed,'Mbps')
    elif option == 3:
        print('Votre vitesse de Download est de : ',down_speed,'Mbps',end=" ")
        print('et votre vitesse de Upload est de : ',up_speed,'Mbps')

    elif option == 4:
        s=[]
        speed.get_servers(s)
        print(speed.results.ping,'ms')
    else:
        print('Désolé, quelquechose ne va pas, svp essayez encore...')

