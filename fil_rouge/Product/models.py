from django.db import models

class CynaDiscounts(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('CynaProducts', models.DO_NOTHING, db_column='product')
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField()
    expiration = models.DateField()

    class Meta:
        managed = False
        db_table = 'cyna_discounts'


class CynaProductCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=24)
    description = models.CharField(max_length=48, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cyna_product_categories'


class CynaProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=24)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(CynaProductCategories, models.DO_NOTHING, db_column='category')
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cyna_products'


class CynaRenewalIntervals(models.Model):
    id = models.BigAutoField(primary_key=True)
    days = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'cyna_renewal_intervals'
