from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','product', 'quantity', 'created_at', 'total_price']
        
    def get_total_price(self, obj):
        return obj.quantity * obj.product.price
    
    
    
class CartLengthSerializer(serializers.Serializer):
    total_items = serializers.IntegerField()