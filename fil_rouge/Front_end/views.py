import requests
from django.shortcuts import render, redirect
from django.views import View
from .decorators import jwt_required
from django.utils.decorators import method_decorator

def logout_view(request):
    request.session.flush()
    return redirect("home")

def Home(request):
    return render(request, 'Home/Home.html')

class LoginForm(View):
    def get(self, request):
        referer = request.META.get("HTTP_REFERER")
        if referer and "/login" not in referer:  # éviter de stocker login comme origine
            request.session["next"] = referer
        return render(request, "User/login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Appel API backend
        response = requests.post("http://localhost:8000/api/login/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            request.session["access_token"] = data.get("access")
            request.session["refresh_token"] = data.get("refresh")
            request.session["is_superuser"] = data.get("is_superuser")

            if data.get("is_superuser"):
                return redirect("/admin/") 
            else:
                return redirect(request.session.pop("next", "home"))
        else:
            return render(request, "User/login.html", {"error": "Identifiants incorrects"})
        

class RegisterForm(View):
    def get(self, request):
        return render(request, "User/register.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        first_name =request.POST.get("first")
        last_name =request.POST.get("last")

        try:
            response = requests.post("http://localhost:8000/api/register/", json={
                "username": username,
                "password": password,
                "email": email,
                "phone": phone,
                "first": first_name,
                "last": last_name
            })

            # Vérifie si la réponse est au format JSON
            if response.headers.get("Content-Type") == "application/json":
                data = response.json()
            else:
                data = {"error": "Réponse invalide du serveur"}

            if response.status_code == 201:
                return redirect("login")
            else:
                return render(request, "User/register.html", {"error": data.get("error", "Erreur inconnue")})

        except requests.exceptions.RequestException as e:
            return render(request, "User/register.html", {"error": "Erreur serveur API : " + str(e)})

@method_decorator(jwt_required, name='dispatch')
class CompteView(View):
    def get(self, request):
        token = request.session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get("http://localhost:8000/api/profile/", headers=headers)

            if response.status_code == 200:
                user_data = response.json()
                return render(request, "User/compte.html", {"user": user_data})
            else:
                return render(request, "User/compte.html", {"error": "Impossible de récupérer les données utilisateur."})

        except requests.exceptions.RequestException:
            return render(request, "User/compte.html", {"error": "Erreur lors de la connexion à l'API."})

@method_decorator(jwt_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        token = request.session.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://localhost:8000/api/profile/", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            return render(request, "User/edit.html", {"user": user_data})
        else:
            return render(request, "User/edit.html", {"error": "Impossible de charger les données utilisateur."})

    def post(self, request):
        token = request.session.get("access_token")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {
            "username":request.POST.get("username"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone")
        }

        response = requests.put("http://localhost:8000/api/profile/update/", json=data, headers=headers)

        if response.status_code == 200:
            return redirect("compte")
        else:
            return render(request, "User/edit.html", {
                "user": data,
                "error": "Erreur lors de la mise à jour "
                "u profil"
            })


class ProductView(View):
    def get(self, request):
        try:
            response = requests.get("http://localhost:8000/api/product/")

            if response.status_code == 200:
                products_data = response.json()
                return render(request, "Product/all.html", {"products": products_data})
            else:
                return render(request, "Product/all.html", {"error": "Aucun produit."})

        except requests.exceptions.RequestException:
            return render(request, "Product/all.htm", {"error": "Erreur lors de la connexion à l'API."})

    
class ProductDetailView(View):
    def get(self, request):
        product_id = request.GET.get("id")
        if not product_id:
            return render(request, "Product/detail.html", {"error": "Aucun produit spécifié."})

        try:
            response = requests.get(f"http://localhost:8000/api/product/{product_id}/")

            if response.status_code == 200:
                product_data = response.json()
                return render(request, "Product/detail.html", {"product": product_data})
            else:
                return render(request, "Product/detail.html", {"error": "Produit introuvable."})
        except requests.exceptions.RequestException:
            return render(request, "Product/detail.html", {"error": "Erreur lors de la connexion à l'API."})


class CartView(View):
    def get(self, request):
        return render(request, 'Product/cart.html')

class PayeView(View):
    def get(self, request):
        return render(request, 'Product/paye.html')
