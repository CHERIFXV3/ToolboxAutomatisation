#!/usr/bin/python3.8

#import des librairies
import os
import time
import datetime
import sys
import subprocess
import glob
import ftplib
import shutil


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
FILE_SAV_DUMPSQL =  DATEJOUR + "-dumpsql.tar.bz2"
FILE_SAV_WORDPRESS =  DATEJOUR + "-wordpress.tar.bz2"
FILE_SAV_MYSQL =  DATEJOUR + "-mysql.tar.bz2"
FILE_SAV_LAN = DATEJOUR + "-conf-lan.tar.bz2"
FILE_SAV_APACHE_DEFAULT = DATEJOUR + "-apache-default.tar.bz2"
FILE_LOG = DATEJOUR + "-log"

#fonction liste des fichiers du dossier backup
def listdirectory(path):
    fichier=[]
    l = glob.glob(BACKUP_PATH+'*')
    for i in l:
        if os.path.isdir(i): fichier.extend(listdirectory(i))
        else: fichier.append(i)
    return fichier

#fichier pour le log du jour
try:
    f = open(BACKUP_PATH+FILE_LOG)
    # est-ce que le fichier log du jour existe
except IOError:
     f = open(BACKUP_PATH+FILE_LOG,"w+") #si il n'existe pas on le crée
     f.write("Subject: SAUVEGARDE COMPLETE DU ...") #subject: pour l'objet du mail
     f.write(DATETIME) #ecriture de la date et de l'heure
     f.write(" --------------------------\n")
finally:
    f.close() #on ferme le fichier

#*****Début du processus de sauvegarde COMPLETE*****
print ("Le dossier de sauvegarde est:", BACKUP_PATH)
os.path.exists(BACKUP_PATH) #vérifie si le dossier pour la sauvegarde existe, = True ou non
if os.path.exists(BACKUP_PATH) == True:
	print("Le dossier de sauvegarde est présent.")
else:
	os.mkdir(BACKUP_PATH) #crée le dossier pour la sauvegarde
	print("Le dossier de sauvegarde n'existait pas, il a été crée.")

print ("Début de la sauvegarde du dossier du site Wordpress.")
print ("Le fichier: ", FILE_SAV_WORDPRESS)
print ("va être sauvegardé dans: ", BACKUP_PATH)
try:
	subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_WORDPRESS, WEB_PATH])
except ValueError as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  ERREUR sur la sauvegarde LOCALE du dossier Wordpress\n") #ecriture de l'erreur dans le log
	print ("Erreur rencontrée lors de la sauvegarde locale du dossier Wordpress.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Sauvegarde locale Wordpress réalisée\n") #ecriture de la sauvegarde réalisée dans le log
	print ('Sauvegarde du dossier Wordpress réalisée.')

print ("Début de la sauvegarde du dossier Mysql.")
print ("Le fichier: ", FILE_SAV_MYSQL)
print ("va être sauvegardé dans: ", BACKUP_PATH)
try:
	subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_MYSQL, SQL_PATH])
except ValueError as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("   ERREUR sur la sauvegarde LOCALE du dossier Mysql\n") #ecriture de l'erreur dans le log
	print ("Erreur rencontrée lors de la sauvegarde locale du dossier Mysql.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Sauvegarde locale du dossier Mysql réalisée\n") #ecriture de la sauvegarde réalisée dans le log
	print ('Sauvegarde du dossier Mysql réalisée.')

print ("Début du Dump et de la sauvegarde Wordpress_db Mysql.")
print ("Le fichier: ", FILE_SAV_DUMPSQL)
print ("va être sauvegardé dans: ", BACKUP_PATH)
try:
	dumpcmd = "mysqldump -h %s -u %s -p%s %s > %s/%s.sql" % (DB_HOST,DB_USER,DB_USER_PASSWORD,DB_NAME,BACKUP_PATH,DB_NAME,)
	os.system(dumpcmd)
	subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_DUMPSQL, BACKUP_PATH + DB_NAME + ".sql"])
	os.remove (BACKUP_PATH + DB_NAME + ".sql") #on garde le fichier dump compressé et on efface le non compressé
except ValueError as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("   ERREUR sur la sauvegarde LOCALE du dump Wordpress_db\n") #ecriture de l'erreur dans le log
	print ("Erreur rencontrée lors de la sauvegarde locale du dump sql Wordpress_db.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Sauvegarde locale du dump wordpress_db réalisée\n") #ecriture de la sauvegarde réalisée dans le log
	print ('Sauvegarde du dump Wordpress_db réalisée.')

#Sauvegarde de quelques fichiers supplémentaires
#--1ER--sauvegarde config resolv.conf, interfaces, hosts et hostname
print ("Début de la sauvegarde des fichiers resolv.conf, interfaces, hosts et hostname.")
print ("Le fichier: ", FILE_SAV_LAN)
print ("va être sauvegardé dans: ", BACKUP_PATH)
try:
	filePath = shutil.copy('/etc/hostname', BACKUP_PATH)
	filePath = shutil.copy('/etc/hosts', BACKUP_PATH)
	filePath = shutil.copy('/etc/resolv.conf', BACKUP_PATH)
	filePath = shutil.copy('/etc/netplan/50-cloud-init.yaml', BACKUP_PATH)
	subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_LAN, BACKUP_PATH + 'hostname', BACKUP_PATH + 'hosts', BACKUP_PATH + 'resolv.conf', BACKUP_PATH + '50-cloud-init.yaml'])
	os.remove (BACKUP_PATH+"hostname") #on garde le fichier compressé et on efface le non compressé
	os.remove (BACKUP_PATH+"hosts") #on garde le fichier compressé et on efface le non compressé
	os.remove (BACKUP_PATH+"resolv.conf") #on garde le fichier compressé et on efface le non compressé
	os.remove (BACKUP_PATH+"50-cloud-init.yaml") #on garde le fichier compressé et on efface le non compressé
except ValueError as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("   ERREUR sur la sauvegarde LOCALE des fichiers conf lan\n") #ecriture de l'erreur dans le log
	print ("Erreur rencontrée lors de la sauvegarde locale des fichiers conf lan.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Sauvegarde locale des fichiers de conf lan réalisée\n") #ecriture de la sauvegarde réalisée dans le log
	print ('Sauvegarde des fichiers conf lan réalisée.')
#--2EME--sauvegarde 000-default.conf apache
print ("Début de la sauvegarde du fichier 000-default.conf de Apache.")
print ("Le fichier: ", FILE_SAV_APACHE_DEFAULT)
print ("va être sauvegardé dans: ", BACKUP_PATH)
try:
        filePath = shutil.copy('/etc/apache2/sites-available/000-default.conf', BACKUP_PATH)
        subprocess.call(['tar', '-cjf', BACKUP_PATH + FILE_SAV_APACHE_DEFAULT, BACKUP_PATH + '000-default.conf'])
        os.remove (BACKUP_PATH+"000-default.conf") #on garde le fichier compressé et on efface le non compressé
except ValueError as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("   ERREUR sur la sauvegarde LOCALE du fichier 000-default.conf\n") #ecriture de l'erreur dans le log
	print ("Erreur rencontrée lors de la sauvegarde locale du fichier 000-default.conf.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Sauvegarde locale du fichier 000-default.conf réalisée\n") #ecriture de la sauvegarde réalisée dans le log
	print ('Sauvegarde du fichier 000-default.conf réalisée.')

#Fin des sauvegardes et écriture de fin dans le log
with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
	f.write("FIN DE LA SAUVEGARDE LOCALE DU  ...") #ecriture dans le log de la fin des sauvegardes
	f.write(DATETIME) #ecriture dans le log de l'heure et de la date
	f.write("--------------------------\n")

#Suppression des sauvegardes en local de plus de 2mn, changer 120 en 432000 pour 5 jours
print ("Suppression des anciens fichiers du dossier Backup en local de plus de 2 minutes = 120 s")
deux_minutes_ago = time.time() - 432000
os.chdir(BACKUP_PATH)
for somefile in os.listdir('.'):
    mtime=os.path.getmtime(somefile)
    if mtime < deux_minutes_ago:
        os.unlink(somefile)
print ("Nettoyage effectué.")

#Affiche la liste des fichiers sauvegardés en local actuellement
print ("****************************************")
print ("****************************************")
print ("liste des fichiers sauvegardés en local")
print (listdirectory(BACKUP_PATH))
print ("*****************************************")
print ("*****************************************")

#Transfert vers le serveur ftp des sauvegardes
with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
     f.write("-------------------------------\n")
     f.write("le...")
     f.write(DATETIME) #ecriture dans le log de l'heure et de la date
     f.write("  TRANSFERT FTP\n") #ecriture des transferts FTP dans le log

print ("Début des transferts ftp des sauvegardes.")
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
		f.write("   ERREUR sur TRANSFERT FTP de la sauvegarde du dossier Wordpress\n") #ecriture erreur dans log
	print ("Erreur rencontrée lors du transfert ftp de la sauvegarde du dossier Wordpress.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Transfert vers ftp de la sauvegarde du dossier Wordpress réalisé\n") #ecriture du transfert de la sauvegarde via FTP dans le log
	print ('Transfert de la sauvegarde du dossier Wordpress par ftp effectué.')

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
		f.write("   ERREUR sur TRANSFERT FTP de la sauvegarde du dossier Mysql\n") #ecriture erreur dans log
	print ("Erreur rencontrée lors du transfert ftp de la sauvegarde du dossier Mysql.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Transfert vers ftp de la sauvegarde du dossier Mysql réalisé\n") #ecriture du transfert de la sauvegarde via FTP dans le log
	print ('Transfert de la sauvegarde du dossier Mysql par ftp effectué.')

#Transfert de la sauvegarde du dump db Wordpress
try:
	ftp = ftplib.FTP(FTP_IP_SRV)
	ftp.connect(FTP_IP_SRV, FTP_PORT)
	ftp.login(user = FTP_USER, passwd = FTP_PASS)
	ftp.storbinary("STOR " + FILE_SAV_DUMPSQL, open(FILE_SAV_DUMPSQL, 'rb'))
except ftplib.all_errors as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("   ERREUR sur TRANSFERT FTP de la sauvegarde du dump db Wordpress\n") #ecriture erreur dans log
	print ("Erreur rencontrée lors du transfert ftp de la sauvegarde du dump db Wordpress.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Transfert vers ftp de la sauvegarde du dump db Wordpress réalisé\n") #ecriture du transfert de la sauvegarde via FTP dans le log
	print ('Transfert de la sauvegarde du dump db Wordpress par ftp effectué.')

#Transfert des fichiers conf lan
try:
	ftp = ftplib.FTP(FTP_IP_SRV)
	ftp.connect(FTP_IP_SRV, FTP_PORT)
	ftp.login(user = FTP_USER, passwd = FTP_PASS)
	ftp.storbinary("STOR " + FILE_SAV_LAN, open(FILE_SAV_LAN, 'rb'))
except ftplib.all_errors as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("   ERREUR sur TRANSFERT FTP de la sauvegarde des fichiers conf lan\n") #ecriture erreur dans log
	print ("Erreur rencontrée lors du transfert ftp de la sauvegarde des fichiers conf lan.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Transfert vers ftp de la sauvegarde des fichiers conf lan réalisé\n") #ecriture du transfert de la sauvegarde via FTP dans le log
	print ('Transfert de la sauvegarde des fichiers conf lan par ftp effectué.')

#Transfert du fichier default apache
try:
	ftp = ftplib.FTP(FTP_IP_SRV)
	ftp.connect(FTP_IP_SRV, FTP_PORT)
	ftp.login(user = FTP_USER, passwd = FTP_PASS)
	ftp.storbinary("STOR " + FILE_SAV_APACHE_DEFAULT, open(FILE_SAV_APACHE_DEFAULT, 'rb'))
except ftplib.all_errors as e:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("   ERREUR sur TRANSFERT FTP de la sauvegarde du fichier 000-default.conf\n") #ecriture erreur dans log
	print ("Erreur rencontrée lors du transfert ftp de la sauvegarde du fichier 000-default.conf.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Transfert vers ftp de la sauvegarde du fichier 000-default.conf réalisé\n") #ecriture du transfert de la sauvegarde via FTP dans le log
	print ('Transfert de la sauvegarde du fichier 000-default.conf par ftp effectué.')

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
		f.write("   ERREUR sur TRANSFERT FTP du fichier LOG\n") #ecriture erreur dans log
	print ("Erreur rencontrée lors du transfert ftp du fichier de logs.")
	print ( e )
else:
	with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
		f.write("le...")
		f.write(DATETIME) #ecriture dans le log de l'heure et de la date
		f.write("  Transfert vers ftp du fichier LOG réalisé\n") #ecriture du transfert de la sauvegarde via FTP dans le log
	print ('Transfert du fichier de LOG V1 de la sauvegarde Wordpress par ftp effectué.')

with open(BACKUP_PATH+FILE_LOG,'a') as f: #ouverture du fichier log du jour
	f.write("-------------------------------\n")
	f.write("le...")
	f.write(DATETIME) #ecriture dans le log de l'heure et de la date
	f.write(" FIN TRANSFERT FTP\n") #ecriture sauvegarde faite dans log
	f.write("-------------------------------\n")

#Transfert de la dernière ecriture du log
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
	filePath = shutil.copy(FILE_LOG, 'LOG') #fichier log qui sera envoyé par mail
	#filePath = shutil.copy('/etc/apache2/sites-available/000-default.conf', BACKUP_PATH)
	subprocess.call(['sh', '/home/osboxes/script/maillog.sh'])
except ValueError as e:
	print ("Erreur lors de l'envoi du mail de log.")
	print ( e )
else:
	print ("Envoi du mail de log effectué.")

#FIN
print ("Ensemble des sauvegardes effectué.")
print ("Sauvegarde complète terminée.")
