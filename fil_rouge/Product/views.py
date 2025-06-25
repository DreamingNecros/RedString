#api Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Product.models import CynaProducts
from .serializers import ProductsSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q



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
    
@api_view(['GET'])
def api_recherche(request):
    query = request.GET.get('q', '')
    prix_min = request.GET.get('prix_min')
    prix_max = request.GET.get('prix_max')
    en_stock = request.GET.get('en_stock')

    produits = CynaProducts.objects.all()

    if query:
        produits = produits.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    if prix_min:
        produits = produits.filter(price__gte=prix_min)

    if prix_max:
        produits = produits.filter(price__lte=prix_max)
    
    if en_stock:
        produits = produits.filter(stock__gt=0)

    paginator = PageNumberPagination()
    paginator.page_size = 6
    result_page = paginator.paginate_queryset(produits, request)
    serializer = ProductsSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)