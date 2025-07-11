import requests
from django.shortcuts import render, redirect
from django.views import View
from .decorators import jwt_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Product.models import CynaProducts
from urllib.parse import urlencode
from django.db.models import Q
import math
from django.conf import settings
from urllib.parse import urlparse

def logout_view(request):
    request.session.flush()
    return redirect("home")

def Home(request):
    produits = list(CynaProducts.objects.all()[:4])  
    
    product1 = produits[0] if len(produits) > 0 else None
    product2 = produits[1] if len(produits) > 1 else None
    product3 = produits[2] if len(produits) > 2 else None
    product4 = produits[3] if len(produits) > 3 else None

    context = {
        'product1': product1,
        'product2': product2,
        'product3': product3,
        'product4': product4,
    }
    return render(request, 'Home/Home.html', context)


class LoginForm(View):
    def get(self, request):
        referer = request.META.get("HTTP_REFERER")
        if referer and "/login" not in referer:
            path = urlparse(referer).path
            request.session["next"] = path
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

            token = data.get("access")
            next_url = request.session.pop("next", "home")

            redirect_url = f"{next_url}?token={token}"

            if data.get("is_superuser"):
                return redirect("/admin/") 
            else:
                return redirect(redirect_url)
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
        
        

from django.views import View
from django.shortcuts import render
import requests

class ProductView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        prix_min = request.GET.get('prix_min', '')
        prix_max = request.GET.get('prix_max', '')
        en_stock = request.GET.get('en_stock', '')
        page = request.GET.get('page', 1)

        produits = CynaProducts.objects.all()

        if q:
                produits = produits.filter(
                Q(name__icontains=q) |
                Q(category__name__icontains=q)
            )
        try:
            if prix_min:
                produits = produits.filter(price__gte=float(prix_min))
            if prix_max:
                produits = produits.filter(price__lte=float(prix_max))
        except ValueError:
            pass  # ignorer les valeurs non valides

        if en_stock.lower() == 'true':
            produits = produits.filter(stock__gt=0)

        paginator = Paginator(produits, 6)

        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)

        query_params = {}
        if q:
            query_params['q'] = q
        if prix_min:
            query_params['prix_min'] = prix_min
        if prix_max:
            query_params['prix_max'] = prix_max
        if en_stock:
            query_params['en_stock'] = en_stock

        base_query = urlencode(query_params)

        context = {
            "products": produits_page.object_list,
            "current_page": produits_page.number,
            "total_pages": paginator.num_pages,
            "has_previous": produits_page.has_previous(),
            "has_next": produits_page.has_next(),
            "previous_page_number": produits_page.previous_page_number() if produits_page.has_previous() else None,
            "next_page_number": produits_page.next_page_number() if produits_page.has_next() else None,
            "page_range": range(1, paginator.num_pages + 1),
            "base_query": base_query,
            "q": q,
            "prix_min": prix_min,
            "prix_max": prix_max,
            "en_stock": en_stock,
        }
        return render(request, "Product/all.html", context)
    
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

@method_decorator(jwt_required, name='dispatch')
@method_decorator(jwt_required, name='dispatch')
class PayeView(View):
    def get(self, request):
        return render(request, 'Product/paye.html', {
            'stripe_pub_key': settings.STRIPE_PUBLIC_KEY,
            'access_token': request.session.get('access_token', '')
        })