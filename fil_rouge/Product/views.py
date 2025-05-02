# Product/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CynaProducts as Product
from .serializers import ProductSerializer

@api_view(['GET'])
def list_products(request):
    Products = Product.objects.all()
    serializer = ProductSerializer(Products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        Product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Produit non trouvé'}, status=404)

    serializer = ProductSerializer(Product)
    return Response(serializer.data)
