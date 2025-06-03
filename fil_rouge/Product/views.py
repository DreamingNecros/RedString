#api Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Product.models import CynaProducts
from .serializers import ProductsSerializer
import json


@api_view(['GET'])
def list_products(request):
    products = CynaProducts.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = CynaProducts.objects.get(pk=pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)
    except CynaProducts.DoesNotExist:
        return Response({'error': 'Produit non trouvé'}, status=404)