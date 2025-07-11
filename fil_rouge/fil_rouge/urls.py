# fil_rouge/urls.py
from django.contrib import admin

from django.urls import path
from User import views as user
from Product import views as product
from Front_end import views as front

urlpatterns = [
    # Page d'accueil
    path('', front.Home, name='home'),

    #partie admin
    path('admin/', admin.site.urls),

    #API verif (connecter ou pas)
    path("api/verify-token/", user.verify_token, name="verify_token"),
    
    #API User
    path('api/login/', user.login, name='api_login'),
    path("api/register/", user.register, name="api_register"),
    path("api/profile/", user.profile, name="api_profile"),
    path("api/profile/update/", user.update_profile, name="api_update_profile"),

    #Page User
    path('login/', front.LoginForm.as_view(), name ='login'),
    path('register/', front.RegisterForm.as_view(), name='register'),
    path('compte/', front.CompteView.as_view(), name='compte'),
    path('edit_profile/', front.EditProfileView.as_view(), name='edit_profile'),
    path("logout/", front.logout_view, name="logout"),

    #API produit
    path('api/product/', product.list_products, name='list_products'),
    path('api/product/<int:pk>/', product.product_detail, name='product_detail'),

    #Page produit
    path('products/', front.ProductView.as_view(), name='products'),
    path('product/detail/', front.ProductDetailView.as_view(), name='product_detail'),  
    path('cart/', front.CartView.as_view(), name='cart'),
    path('paye',front.PayeView.as_view(), name='paye'),

    #API Recherche
    path('api/recherche/', product.api_recherche, name='api_recherche')

]
