import requests
from django.shortcuts import render

def Home(request):
    # Effectue une requête HTTP GET vers ton API pour récupérer les produits
    response = requests.get("http://127.0.0.1:8000/api/produits/")
    
    # Vérifie si la requête a bien réussi (code 200)
    if response.status_code == 200:
        produits = response.json()  # On récupère les produits sous forme de JSON
    else:
        produits = []  # Si l'API ne répond pas, on passe une liste vide

    # Passe les produits au template
    return render(request, 'home page/Home.html', {'produits': produits})


