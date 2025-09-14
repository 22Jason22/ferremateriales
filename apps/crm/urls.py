from django.urls import path

from .views import clientes, ver_cliente, editar_cliente, historial_cliente

app_name = 'crm'

urlpatterns = [
    path('', clientes, name='clientes'),
    path('<int:cliente_id>/', ver_cliente, name='ver_cliente'),
    path('<int:cliente_id>/editar/', editar_cliente, name='editar_cliente'),
    path('<int:cliente_id>/historial/', historial_cliente, name='historial_cliente'),
]
