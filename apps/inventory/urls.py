"""zzz"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    StockMovementViewSet,
    product_list,
    product_add,
    product_edit,
    product_delete,
    catalog,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', product_add, name='product_add'),
    path('<int:pk>/edit/', product_edit, name='product_edit'),
    path('<int:pk>/delete/', product_delete, name='product_delete'),
    path('catalogo/', catalog, name='catalog'),
] + router.urls
