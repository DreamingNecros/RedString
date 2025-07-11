#api Product
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from Product.models import CynaProducts
from .serializers import ProductsSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

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

@api_view(["POST"])
def payment(request):
    try:
        cart = request.data.get('cart', [])
        if not cart:
            return Response({'success': False, 'error': 'Panier vide.'}, status=400)

        total_cents = 0

        for item in cart:
            product_id = item.get('id')
            quantity = int(item.get('quantity', 0))
            if not product_id or quantity <= 0:
                return Response({'success': False, 'error': 'Données panier invalides.'}, status=400)
            
            try:
                product = CynaProducts.objects.get(id=product_id)
            except CynaProducts.DoesNotExist:
                return Response({'success': False, 'error': f'Produit {product_id} introuvable.'}, status=404)

            price_cents = int(Decimal(product.price) * 100)
            total_cents += price_cents * quantity

        if total_cents == 0:
            return Response({'success': False, 'error': 'Montant total nul.'}, status=400)

        # Créer le PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=total_cents,
            currency='eur',
            metadata={'user_id': request.user.id}
        )

        return Response({
            'success': True,
            'clientSecret': intent.client_secret,
            'amount': total_cents / 100  # pour affichage
        })

    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)