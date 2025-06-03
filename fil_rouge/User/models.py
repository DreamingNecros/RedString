from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d’utilisateur est requis")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.date_joined = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", 1)
        extra_fields.setdefault("is_superuser", 1)
        extra_fields.setdefault("is_active", 1)
        return self.create_user(username, email, password, **extra_fields)

class AuthUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    phone = models.CharField(max_length=16)
    mfa_secret = models.TextField(blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] 
    
    class Meta:
        managed = False
        db_table = 'auth_user'


class CynaAddresses(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.CharField(max_length=8)
    street = models.CharField(max_length=64)
    complement = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=8)
    country = models.ForeignKey('CynaCountries', models.DO_NOTHING, db_column='country')

    class Meta:
        managed = False
        db_table = 'cyna_addresses'


class CynaCardTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=16)
    description = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cyna_card_types'


class CynaCards(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.CharField(max_length=16)
    expiration = models.DateField()
    last_name = models.CharField(max_length=16)
    first_name = models.CharField(max_length=16)
    ccv = models.CharField(max_length=3)
    type = models.ForeignKey(CynaCardTypes, models.DO_NOTHING, db_column='type')

    class Meta:
        managed = False
        db_table = 'cyna_cards'


class CynaCountries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=48)

    class Meta:
        managed = False
        db_table = 'cyna_countries'


class CynaOrderFulfillment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=16)
    description = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cyna_order_fulfillment'


class CynaOrders(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    product = models.ForeignKey('Product.CynaProducts', models.DO_NOTHING, db_column='product')
    quantity = models.IntegerField()
    fulfillment = models.ForeignKey(CynaOrderFulfillment, models.DO_NOTHING, db_column='fulfillment')
    order_date = models.DateTimeField()
    renewal = models.ForeignKey('Product.CynaRenewalIntervals', models.DO_NOTHING, db_column='renewal')
    is_renewed = models.IntegerField()
    card = models.ForeignKey(CynaCards, models.DO_NOTHING, db_column='card')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'cyna_orders'


class CynaRelUserCard(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    card = models.ForeignKey(CynaCards, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cyna_rel_user_card'
