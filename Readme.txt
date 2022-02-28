# ToolboxAutomatisation

Projet 06 du parcours Administrateur Infrastructure & Cloud d'Openclassrooms

	o	Etudiant AIC OpenClassrooms : Beladra Chérif
	o	Date de création : 15/02/2022
	o	Dernière modification : 27/02/2022
	o	Testé avec : Python 3.8
	o	Projet sous Licence GNU General Public License v3.0


Contexte du Projet P6 AIC
  
 - Ce projet est une démonstration de solution de Toolbox 
   permettant d'appeler plusieurs fonctionnalités automatisées de tâches plutôt complexes 
   mais surtout répétitives d'administration système.
 - Ce programme vise principalement à automatiser des sauvegardes complètes et incrémentielles d'un site Wordpress actif d'un serveur web, 
   de transférer les sauvegardes et logs via FTP sur un serveur de sauvegarde, de supprimer les données sauvegardées en local de plus de X temps
   et d'être notifié par mail de ces actions.
   Le programme permet également d'utiliser quelques autres fonctionnalités comme des tests de débit et de ping de connection, 
   la géolocalisation et l'apport d'informations comme l'ip publique et l'hostname de la machine mais surtout un port scanner 
   afin de connaitre les ports et services ouverts et utilisés, à des fins de sécurité réseau par exemple. 
 - Un menu Toolbox du Script MenuToolbox.py développe un menu 
   des différents scripts d’exécution de tâches.
 - Changement des variables du script selon l'infrastructure et les informations de connection.
 - Le script est initialement dédiée à une petite infrastructure de 2 servers Linux Ubuntu 18+ 
   hébergeant sur le premier serveur un site Wordpress, un serveur ftp et la présence du client 
   smtp "msmtp". Le second server faisant office de serveur de sauvegarde.
 - Cela devrait fonctionner sur d'autres distributions Linux plutôt récentes et proche 
   d'Ubuntu tels que Debian ou d'autres mais pas testé.
 - Doit être exécuté en root pour pouvoir profiter de toutes les fonctionnalités des scripts. (via un sudo sous Ubuntu).


Technologies utilisées

	o   VM VirtualBox
	o   2 Machines Ubuntu server 20.04.3 LTS
	o   Service vsftpd serveur
	o   Service client smtp : "msmtp"
	o   Git Bash
	o   Notepad++
	o   Gmail

Contenu de ce repository

	•   Script Python :   MenuToolbox.py
	•   Script Python :   SaveCompleteWordpress.py
	•   Script Python :   SaveIncrementielWordpress.py
	•   Script Python :   SpeedTestConnection.py
	•   Script Python :   IPAdressLoc.py
	•   Script Python :   PortsScanner.py
	•   maillog.sh
	•   maillog-incre1.sh
	•   readme.txt
	•   README.md

Prérequis : Installation ou présence des modules nécessaires pour l'édition et l'execution des Scripts  

	•   Module "pyfiglet" permettant des affichages en art Ascii (pip install pyfiglet).
	•   Module "os" permettant d’effectuer des opérations courantes liées au système d’exploitation.
	•   Module "sys" fournissant un accès à certaines variables utilisées et maintenues par l'interpréteur, et à des fonctions interagissant fortement avec ce dernier.
	•   Module "time" fournissant différentes fonctions liées au temps.
	•   Module "datetime" fournissant des classes permettant de manipuler les dates et les heures.
	•   Module "dateutil" fournissant de puissantes extensions au module standard datetime. (from dateutil.relativedelta import relativedelta)
	    (apt-get install python-dateutil ou pip install python-dateutil)
	•   Module "subprocess" permettant de lancer de nouveaux processus, les connecter à des tubes d'entrée/sortie/erreur, et d'obtenir leurs codes de retour.
	•   Module "glob" permettant de renvoyer des listes contenant des chemins complets de fichiers ou répertoires contenus dans un path.
	•   Module "ftplib" permettant le transfert de fichiers via le protocol FTP, ainsi que sa connection et son utilisation.
	•   Module "shutil" permettant des opérations sur les fichiers et ensembles de fichiers, telles que des copies et des déplacements de fichiers.
	•   Module "speedtest" permettant de tester sa connection internet. (apt-get install speedtest-cli)
	•   Module "geocoder" permettant de fournir des informations de géolocalisation. (pip install geocoder)
	•   Module "socket" permettant de manipuler les interfaces socket.


Configuration des machines cibles

- Les machines cibles sont deux Ubuntu Server 20.04.3 LTS reliés en local avec ip fixes et accès à une connection internet extérieure afin de rendre accessible le site Wordpress et permettre les notifications mails.
- Un premier serveur est entièrement dédié au stockage des sauvegardes en tant que serveur de sauvegarde et le second serveur héberge un service web Apache Wordpress, un serveur FTP et un client msmtp.
- Les 6 scripts python énumérés plus haut sont placés sur le serveur Wordpress dans le dossier "/home/osboxes" , et les 2 petits scripts bash "maillog.sh" et "maillog-incre1.sh"
sont placés dans le dossier "/home/osboxes/script". Vous avez donc à modifier la configuration et les variables des scripts Python si vous avez une autre configuration ou 
si vous utilisez d'autres chemins d'accès.
- L'adresse gmail dans les deux scripts bash doit également être personnalisée afin de pouvoir recevoir les notifications mail sur votre propre adresse mail, car celle présente dans les deux scripts bash maillog est mon adresse gmail personnelle de test, à modifier donc. 
