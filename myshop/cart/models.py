from django.db import models
from shop.models import Product
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-created_at']
        # unique_together = ('user', 'product')

    # def __str__(self):
    #     return f'Cart {self.id}'

    # def get_total_price(self):
    #     return self.quantity * self.product.price