---------------------------------
Cr�er une nouvelle base de donn�es

1. Dans well_model.py ajouter ou d�commenter #initialize_db puis appeler le fichier en ldc.
2. Changer le propri�taire du fichier root->pi avec la commande : sudo chown pi mydb.db
 

Erreur
tant qu'aucun objet n'a �t� ajout� La base de donn�e est vide et le script/site renvoi une erreur indiquant que la DB n'existe pas.

----------------------------------
SERVEUR
le serveur apache est lanc� au d�marrage du PI et red�marr� si besoin par SUPERVISOR
pour red�marrer manuellement : sudo supervisorctl restart all

le fichier de conf de supervisor :  cat /etc/supervisor/conf.d/website-flask-serial-usb.conf

le log d'erreur : cat  /var/log/website-flask-serial-usb-err.log


----------------------------------
CRON

les deux commandes suivantes n'appellent pas le m�me CRON:
sudo crontab -e
crontab -e

le cron qui fonctionne est celui appel� avec sudo et qui n'appelle pas cron.sh mais directement usbtoINO.py


