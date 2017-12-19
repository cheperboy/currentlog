---------------------------------
Créer une nouvelle base de données

1. Dans well_model.py ajouter ou décommenter #initialize_db puis appeler le fichier en ldc.
2. Changer le propriétaire du fichier root->pi avec la commande : sudo chown pi mydb.db
 

Erreur
tant qu'aucun objet n'a été ajouté La base de donnée est vide et le script/site renvoi une erreur indiquant que la DB n'existe pas.

----------------------------------
SERVEUR
le serveur apache est lancé au démarrage du PI et redémarré si besoin par SUPERVISOR
pour redémarrer manuellement : sudo supervisorctl restart all

le fichier de conf de supervisor :  cat /etc/supervisor/conf.d/website-flask-serial-usb.conf

le log d'erreur : cat  /var/log/website-flask-serial-usb-err.log


----------------------------------
CRON

les deux commandes suivantes n'appellent pas le même CRON:
sudo crontab -e
crontab -e

le cron qui fonctionne est celui appelé avec sudo et qui n'appelle pas cron.sh mais directement usbtoINO.py


