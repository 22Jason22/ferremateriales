from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.sales_list, name='sales_list'),
    path('crear/', views.sales_create, name='sales_create'),
    path('<int:pk>/editar/', views.sales_edit, name='sales_edit'),
]
