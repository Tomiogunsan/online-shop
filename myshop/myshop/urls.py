
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import CategoryViewSet, ProductViewSet
from cart.views import CartViewSet
from orders.views import OrderViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')
# router.register(r'order', CartViewSet, basename='cart')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
]
