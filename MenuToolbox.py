#!/usr/bin/python3.8

import pyfiglet
#pip install pyfiglet (module Ascii)

ascii_banner = pyfiglet.figlet_format("            Toolbox multifonction")
print(ascii_banner)

def menu():
    print("\n               Bienvenue dans la Toolbox multifonction automatisée =)\n")

    print("[1] Sauvegarde Complète Wordpress")
    print("(Données Wordpress + Fichiers de Conf + SQL + Logs + Transferts FTP + Notification Mail)\n")

    print("[2] Sauvegarde Incrémentielle")
    print("(Nécessite une sauvegarde Complète afin de pouvoir sauvegarder uniquement les modifications)\n")

    print("[3] Speed Test")
    print("(Fournit les débits de Download, Upload ou le ping de la connection)\n")

    print("[4] IP & Localisation")
    print("(Fournit l'IP publique, la ville ainsi que la latitude et longitude du server)\n")

    print("[5] Ports Scanner")
    print("(Scan l'utilisation et l'état des ports utilisés sur un host)\n")

    print("[0] Quitter le programme!\n")

menu()
option = int(input("Entre le numéro de la fonction choisie afin de l'executer: "))

while option != (0):
	if option == 1:
		#Ajouter les fonctions de l'option 1
		print("\nL'option 1 de Sauvegarde Complète a été choisie.\n")
		exec(open('SaveCompleteWordpress.py').read())
		print("\nAppuyez sur Entrée pour relancer le menu de la Toolbox.")
		def wait():
			e=input()
			print (e)
		wait()
	elif option == 2:
        	#Ajouter les fonctions de l'option 2
		print("\nL'option 2 de Sauvegarde Incrémentielle a été choisie.\n")
		exec(open('SaveIncrementielWordpress.py').read())
		print("\nAppuyez sur Entrée pour relancer le menu de la Toolbox.")
		def wait():
			e=input()
			print (e)
		wait()
	elif option == 3:
		#Ajouter les fonctions de l'option 3
		print("\nL'option 3 de Speed Test a été choisie.\n")
		exec(open('SpeedTestConnection.py').read())
		print("\nAppuyez sur Entrée pour relancer le menu de la Toolbox.")
		def wait():
			e=input()
			print (e)
		wait()
	elif option == 4:
		#Ajouter les fonctions de l'option 4
		print("\nL'option 4 d'IP & Localisation a été choisie.\n")
		exec(open('IPAdressLoc.py').read())
		print("\nAppuyez sur Entrée pour relancer le menu de la Toolbox.")
		def wait():
			e=input()
			print (e)
		wait()
	elif option == 5:
		#Ajouter les fonctions de l'option 5
		print("\nL'option 5 de Port Scanner a été choisie.\n")
		exec(open('PortsScanner.py').read())
		print("\nAppuyez sur Entrée pour relancer le menu de la Toolbox.")
		def wait():
			e=input()
			print (e)
		wait()
	else:
		print("Option invalide.")
		print("\nAppuyez sur Entrée pour relancer le menu de la Toolbox.")

		def wait():
			e=input()
			print (e)
		wait()

	print()
	menu()
	option = int(input("Entrez à nouveau votre numéro d'option: "))

print("\nMerci d'avoir utilisé cette Toolbox multifonction!")
print("On espère qu'elle vous aura simplifié la vie d'admin, paresseux que vous êtes! =p\n")
