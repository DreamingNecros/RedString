#facilite la partie transformation en json + permet de valider les donnée
from rest_framework import serializers
from Product.models import CynaProducts

class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = CynaProducts
        fields = ['id','name', 'description', 'price', 'stock', 'category']