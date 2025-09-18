from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.purchases_list, name='purchase_list'),
    path('crear/', views.purchases_create, name='purchase_create'),
    path('<int:pk>/', views.purchase_detail, name='purchase_detail'),
    path('<int:pk>/editar/', views.purchases_edit, name='purchase_edit'),
    path('<int:pk>/recepcion/', views.goods_receipt_create, name='goods_receipt_create'),
]
