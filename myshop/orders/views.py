from rest_framework import viewsets, status
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.decorators import action
from cart.models import Cart
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects
    serializer_class = OrderSerializer
    
    
    @action(detail=False, methods=['post'])
    def create_orders(self, request):
        # user = request.user
        # cart_items = Cart.objects.filter(user=request.user)
        cart_items = Cart.objects.all()
        
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_cost = sum(items.product.price * items.quantity for items in cart_items)
        
        order_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'address': request.data.get('address'),
            'postal_code': request.data.get('postal_code'),
            'city': request.data.get('city'),
            'paid': request.data.get('paid', False),
            'total_cost': total_cost
        }
        
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
                cart_item.delete()
                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
      
    
    

