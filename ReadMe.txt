pour ce projet il est préférable d'utiliser un environement de developement

pour le créer il faut d'abord verifier si on a python
bash                            
python --version ou python3 -m venv env

ensuite on créer l'environement
Sous Windows                        Sous linux/Mac:
python -m venv env                  python3 -m venv env

enfin on l'active (a chaque fois qu'on lance l'apli):
Sous Windows                        Sous Linux/Mac
.\env\Scripts\Activate.ps1          source env/bin/activate

on tape cette ligne pour installer toutes les dépendance

pip install requests mysqlclient djangorestframework django qrcode pyotp djangorestframework-simplejwt stripe

Il faut ces choses dans l'environement pour que à marche
requests (pour faire des requests a l'api)
mysqlclient (pour mysql)
djangorestframework (pour l'api)
django (pour django)
qrcode (pour genere des qrcode )
pyotp (pour gere authentificator)
djangorestframework-simplejwt (pour avoir des token de connection)
stripe (utilisation de l'api stripe)

pour lancer le serv il faut faire :

python manage.py runserver

verifier dans setting.py que la partie Database est bonne pour vous

Découpage :
Le dossier User contient toute la partie Api qui gere la partie utilisateur
Le dossier Product contient toute la partie Api qui gere la partie Produit
Le dossier Front_end contient toute la partie Front_end c'est a dire les fichier html, les images, le js ...
Le dossier fil_rouge contient les setting de Django et les url 