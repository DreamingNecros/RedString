# fil_rouge/urls.py

from django.contrib import admin
from django.urls import path, include
from cyna_web import views as cyna
from api import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/produits/', views.liste_produits, name='liste_produits'),
    path('api/produits/<int:pk>/', views.produit_detail, name='produit_detail'),
    path('', cyna.Home, name='home'),  # Page d'accueil
]
