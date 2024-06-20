from rest_framework import viewsets, status
from .models import Cart
from .serializers import CartSerializer, CartLengthSerializer
from django.conf import settings
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from shop.models import Product
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.views import APIView




class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects
    serializer_class = CartSerializer
    
    # def __init__(self, request):
    #     self.session = request.session
    #     cart = self.session.get(settings.CART_SESSION_ID)
    #     if not cart:
    #         cart = self.session[settings.CART_SESSION_ID] = {}
    #     self.cart = cart 
      
    @action(detail=False, methods=['post'])   
    def add(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        if not product_id:
             return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, id=product_id, available=True)
       
        cart_item, created = Cart.objects.get_or_create(
            # user=request.user, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # self.session.modified = True
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, {"message": "Product added to cart successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], url_path='remove')
    def remove(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(Product, id=product_id, available=True)
        cart_item = Cart.objects.filter(product=product).first()
        if cart_item:
            cart_item.delete()
            self.session.modified = True
            return Response({"message": "Product removed from cart successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)
    
    
    @action(detail=True, methods=['patch'], url_path='update')
    def update_cart(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk)
        quantity = request.data.get('quantity')
        
        if quantity is None:
            return Response({"error": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Quantity must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    # @action(detail=False, methods=['get'])
    # def list_cart(self, request):
    #     cart_items = Cart.objects.filter(user=request.user)
    #     serializer = CartSerializer(cart_items, many=True)
    #     return Response(serializer.data)
    
    
    @action(detail=False, methods=['get'])
    def cart_length(self, request):
        total_items = Cart.objects.aggregate(total_items=Sum('quantity'))['total_items']
        if total_items is None:
            total_items = 0
            
        serializer = CartLengthSerializer({'total_items': total_items})
        return Response(serializer.data)