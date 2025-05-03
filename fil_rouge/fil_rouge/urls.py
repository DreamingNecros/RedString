# fil_rouge/urls.py
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from User import views as user
from Product import views as product
from Front_end import views as front

urlpatterns = [
    path('admin/', admin.site.urls),

    # Routes pour les produits
    path('product/', product.list_products, name='list_products'),
    path('product/<int:pk>/', product.product_detail, name='product_detail'),

    # Page d'accueil
    path('', front.Home, name='home'),
]
