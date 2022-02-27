#!/usr/bin/python3.8

#import librairies
import os
import time
import sys
import subprocess
import glob
import ftplib
import shutil
from dateutil.relativedelta import relativedelta
# Si pas trouvé, apt-get install python-dateutil ou pip install python-dateutil
from datetime import date
from datetime import datetime


#initialisation des variables
DATETIME = time.strftime('%Y%d%m-%H%M%S')
DATEJOUR =  time.strftime('%Y%d%m')
BACKUP_PATH = '/home/backup/'
WEB_PATH = '/var/www/html/wordpress'
SQL_PATH = '/var/lib/mysql'
DB_HOST = 'localhost'
DB_USER = 'admin'
DB_USER_PASSWORD = 123
DB_NAME = 'wordpress'
FTP_IP_SRV='192.168.2.9'
FTP_PORT=21
FTP_USER='osboxes'
FTP_PASS='osboxes.org'
FILE_SAV_WORDPRESS =  DATEJOUR + "-wordpress-INCRE-1.tar.bz2" # 1iere incrementielle
FILE_SAV_MYSQL =  DATEJOUR + "-mysql-INCRE-1.tar.bz2" # 1iere incrementielle
FILE_LOG = DATEJOUR + "-log-INCRE-1" #log de la 1iere incrementielle
today = time.strftime('%Y%d%m')
print("Date du jour :", today )
hier =  ((datetime.today()- relativedelta(days=1)).strftime('%Y%d%m'))
print("Date d'hier :", hier)
dateStr = hier
#print('Hier dans la variable : ' ,dateStr)
FILE_LOG_COMPLETE = dateStr + "-log"
FILE_SAV_WORDPRESS_HIER =  dateStr + "-wordpress-INCRE-1.tar.bz2" # 1iere incrementielle
FILE_SAV_MYSQL_HIER =  dateStr + "-mysql-INCRE-1.tar.bz2" # 1iere incrementielle
FILE_SAV_LAN_HIER = dateStr + "-conf-lan-INCRE-1.tar.bz2" # 1iere incrementielle
FILE_SAV_APACHE_DEFAULT_HIER = dateStr + "-apache-default-INCRE-1.tar.bz2" # 1iere incrementielle
LASUITE = 'none'

#verifier que la sauvegarde complete J-1 existe en cherchant le log de la complete
try:
	f = open(BACKUP_PATH+FILE_LOG_COMPLETE)
	# est ce que le fichier log du jour existe
	LASUITE = 'ok' #sauvegarde complete J-1 existe
except IOError:
	print ("La sauvegarde complete J-1 est inexistante.")
	LASUITE = 'ko'
else:
	# action
	print ("La sauvegarde complete J-1 est présente. La sauvegarde incrémentielle peut se poursuivre.")

if LASUITE == 'ok': #action car sauvegarde complete J-1 existe
		    #la sauvegarde precedente est la complete et je fais la 1ere  incrementielle
		    #fonction pause
	print ("\nAppuyez sur Entrée pour continuer.")
	def wait():
		e=input()
		print (e)
	wait()

	#fichier pour le log du jour
	try:
		f = open(BACKUP_PATH+FILE_LOG)
		# est-ce que fichier log du jour existe
	except IOError:
		f = open(BACKUP_PATH+FILE_LOG,"w+") #si il n'existe pas on le crée
		f.write("Subject: SAUVEGARDE INCREMENTIELLE N°1 J2 DU ...") #subject: pour l'objet du mail
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("--------------------------\n")
	finally:
		f.close() #on ferme le fichier

	#******Début du processus de sauvegarde INCREMENTIELLE****
	print ("Début de la sauvegarde incrementielle 1 du dossier site Wordpress.")
	print ("Le fichier: ", FILE_SAV_WORDPRESS)
	print ("va être sauvegardé dans: ", BACKUP_PATH)
	try:
		subprocess.call(['tar', '-cvf', BACKUP_PATH + FILE_SAV_WORDPRESS, '-N', BACKUP_PATH + FILE_LOG, WEB_PATH]) #incrementielle differences depuis date du jour de creation du log incrementielle
	except ValueError:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("  ERREUR sur la sauvegarde incrementielle 1 LOCALE de Wordpress\n") #ecriture de l'erreur dans le log
		print ("Erreur rencontrée lors de la sauvegarde incrementielle 1 du dossier Wordpress.")
	else:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("  Sauvegarde locale incrementielle 1 Wordpress realisée\n") #ecriture sauvegarde faite dans log
		print ('Sauvegarde incrementielle 1 du dossier Wordpress réalisée.')

	print ("Début de la sauvegarde incrementielle 1 du dossier Mysql.")
	print ("Le fichier: ", FILE_SAV_MYSQL)
	print ("va être sauvegardé dans: ", BACKUP_PATH)
	try:
		subprocess.call(['tar', '-cvf', BACKUP_PATH + FILE_SAV_MYSQL, '-N', BACKUP_PATH + FILE_LOG, SQL_PATH]) #incrementielle differences depuis date du jour de creation du log incrementielle
	except ValueError:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("   ERREUR sur la sauvegarde incrementielle 1 LOCALE du dossier Mysql\n") #ecriture de l'erreur dans le log
		print ("Erreur rencontrée lors de la sauvegarde incrementielle 1 locale du dossier Mysql.")
	else:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("  Sauvegarde locale incrementielle 1 du dossier Mysql réalisée\n") #ecriture sauvegarde faite dans log
		print ('Sauvegarde incrementielle 1 du dossier Mysql réalisée.')

	#Fin des sauvegardes et écriture de fin dans le log
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("FIN DE LA SAUVEGARDE INCREMENTIELLE 1 LOCALE DU ...") #ecriture fin de sauvegarde
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("--------------------------\n")

	#suppression des sauvegardes en local de plus de 2mn changer 120 en 432000 pour 5 jours
	print ("Suppression des anciens fichiers du dossier Backup en local de plus de 5 jours = 432000 s")
	cinq_jours_ago = time.time() - 432000
	os.chdir(BACKUP_PATH)
	for somefile in os.listdir('.'):
	    mtime=os.path.getmtime(somefile)
	    if mtime < cinq_jours_ago:
	        os.unlink(somefile)
	print ("Nettoyage effectué.")

	#Transfert vers le serveur ftp des sauvegardes
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("-------------------------------\n")
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  TRANSFERT FTP\n") #ecriture des transferts FTP dans le log

	print ("Début des transferts ftp des sauvegardes incrémentielles.")

	#Transfert de la sauvegarde du dossier Wordpress 
	try:
		ftp = ftplib.FTP(FTP_IP_SRV)
		ftp.connect(FTP_IP_SRV, FTP_PORT)
		ftp.login(user = FTP_USER, passwd = FTP_PASS)
		ftp.storbinary("STOR " + FILE_SAV_WORDPRESS, open(FILE_SAV_WORDPRESS, 'rb'))
	except ftplib.all_errors as e:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("   ERREUR sur TRANSFERT FTP de la sauvegarde incrementielle 1 du dossier Wordpress\n") #ecriture erreur dans log
		print ("Erreur rencontrée lors du transfert ftp de la sauvegarde incrementielle 1 du dossier Wordpress.")
		print ( e )
	else:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("  Transfert vers ftp de la sauvegarde incrementielle 1 du dossier Wordpress réalisé\n") #ecriture sauvegarde faite dans log
		print ('Transfert de la sauvegarde incrementielle 1 du dossier Wordpress par ftp effectué.')

	#Transfert de la sauvegarde du dossier mysql
	try:
		ftp = ftplib.FTP(FTP_IP_SRV)
		ftp.connect(FTP_IP_SRV, FTP_PORT)
		ftp.login(user = FTP_USER, passwd = FTP_PASS)
		ftp.storbinary("STOR " + FILE_SAV_MYSQL, open(FILE_SAV_MYSQL, 'rb'))
	except ftplib.all_errors as e:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("   ERREUR sur TRANSFERT FTP de la sauvegarde incrementielle 1 du dossier Mysql\n") #ecriture erreur dans log
		print ("Erreur rencontrée lors du transfert ftp de la sauvegarde du dossier Mysql.")
		print ( e )
	else:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("  Transfert vers ftp de la sauvegarde incrementielle 1 du dossier Mysql réalisé\n") #ecriture sauvegarde faite d$
		print ('Transfert de la sauvegarde incrementielle 1 du dossier Mysql par ftp effectué.')

	#Transfert du log
	try:
		ftp = ftplib.FTP(FTP_IP_SRV)
		ftp.connect(FTP_IP_SRV, FTP_PORT)
		ftp.login(user = FTP_USER, passwd = FTP_PASS)
		ftp.storbinary("STOR " + FILE_LOG, open(FILE_LOG, 'rb'))
	except ftplib.all_errors as e:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("   ERREUR sur TRANSFERT FTP incrementielle 1 du fichier LOG\n") #ecriture erreur dans log
		print ("Erreur rencontrée lors du transfert ftp incrementielle 1 du fichier de logs.")
		print ( e )
	else:
		with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
			f.write("le...")
			f.write(DATETIME) #ecriture dans le log de l'heure et de la date
			f.write("  Transfert vers ftp du fichier LOG incrementielle 1 réalisé\n") #ecriture sauvegarde faite d$
		print ('Transfert du fichier de LOG V1 de la sauvegarde incrementielle 1 Wordpress par ftp effectué.')

	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("-------------------------------\n")
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write(" FIN TRANSFERT FTP\n") #ecriture sauvegarde faite dans log

	##Transfert de la dernière ecriture du log
	try:
		ftp = ftplib.FTP(FTP_IP_SRV)
		ftp.connect(FTP_IP_SRV, FTP_PORT)
		ftp.login(user = FTP_USER, passwd = FTP_PASS)
		ftp.storbinary("STOR " + FILE_LOG, open(FILE_LOG, 'rb'))
		print ("Transfert ftp du LOG final et autres fichiers de sauvegardes finis.")
	except ftplib.all_errors as e:
		print ("Erreur sur le transfert ftp du log final.")
		print ( e )
	else:
		print ("Transfert du log final par ftp effectué.")

	#envoi par mail du rapport (fichier log)
	try:
		filePath = shutil.copy(FILE_LOG, 'LOG-INCRE') #fichier log qui sera envoye par mail
		#filePath = shutil.copy('/etc/apache2/sites-available/000-default.conf', BACKUP_PATH)
		subprocess.call(['sh', '/home/osboxes/script/maillog-incre1.sh'])
	except ValueError:
		print ("Erreur lors de l'envoi du mail de log.")
	else:
		print ("Envoi du mail de log effectué.")

		#FIN
		print ("Ensemble des sauvegardes effectué.")
		print ("Sauvegarde incrementielle terminée.")
else:
	print ("Abandon par ko") #car sauvegarde complete J-1 inexistante
