"""zzz"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    StockMovementViewSet,
    product_list,
    catalog,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('', product_list, name='product_list'),
    path('catalogo/', catalog, name='catalog'),
] + router.urls
