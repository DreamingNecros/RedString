# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Produit
from .serializers import ProduitSerializer

@api_view(['GET'])
def liste_produits(request):
    produits = Produit.objects.all()
    serializer = ProduitSerializer(produits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def produit_detail(request, pk):
    try:
        produit = Produit.objects.get(pk=pk)
    except Produit.DoesNotExist:
        return Response({'error': 'Produit non trouvé'}, status=404)

    serializer = ProduitSerializer(produit)
    return Response(serializer.data)
