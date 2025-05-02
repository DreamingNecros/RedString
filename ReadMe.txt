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
