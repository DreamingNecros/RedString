LA MAIN BRANCH EST PAS LA BONNE IL FAUT ALLER SUR LA BRANCH PREP

Il faut ces choses dans l'environement pour que à marche
-pip install requests (pour faire des requests a l'api)
-pip install mysqlclient (pour mysql)
-pip install djangorestframework (pour l'api)
-pip install django (pour django)
-pip install qrcode (pour genere des qrcode )
-pip install pyotp (pour gere authentificator)
-pip install djangorestframework-simplejwt (pour avoir des token de connection)

pour lancer l'environement sur windows		sur linux/Mac
	
.\nom de l'env\Scripts\activate			    source/nom environement/bin/activate

pour lancer le serv il faut faire :

python manage.py runserver

quand on rajoute des table dans le fichier model.py

python manage.py makemigrations
python manage.py migrate

verifier dans setting.py que la partie Database est bonne pour vous

Découpage :
Le dossier User contient toute la partie Api qui gere la partie utilisateur
Le dossier Product contient toute la partie Api qui gere la partie Produit
Le dossier Front_end contient toute la partie Front_end c'est a dire les fichier html, les images, le js ...
Le dossier fil_rouge contient les setting de Django et les url 
