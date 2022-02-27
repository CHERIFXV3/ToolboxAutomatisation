#!/usr/bin/python3.8

import pyfiglet
import sys
import socket
from datetime import datetime

ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Définir une cible

target = input("Quel host souhaitez-vous scanner? : ")

	# traduction du nom d'hôte en IPv4
target_ip = socket.gethostbyname(target)
print("Début du scan de l'host : ", target)

# Ajout de Banner
print("-" * 50)
print("Cible à scanner : " + target_ip)
# L'heure a laquelle le scan a commencé
t1 = datetime.now()
print("Le Scan a commencé à : " + str(datetime.now()))
print("-" * 50)

try:

	# On va scanner les ports de 1 à 65535.
	for port in range(1,65535):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)

		# renvoie un indicateur d'erreur
		result = s.connect_ex((target,port))
		if result ==0:
			print("Le port {} est ouvert".format(port))
		s.close()

except KeyboardInterrupt:
		print("\nSortie du programme !!!!")
		sys.exit()
except socket.gaierror:
		print("\nLe nom d'hôte n'a pas pu être résolu !!!!")
		sys.exit()
except socket.error:
		print("\Le serveur ne répond pas !!!!")
		sys.exit()

#Check du temps à nouveau
t2 = datetime.now()

#Calcul de la différence de temps, pour voir combien de temps a pris le scan de ports
total = t2 - t1

#Affichage du temps pris par le scan
print("-" * 50)
print ("Scan des ports complété en :", total)
print("-" * 50)
