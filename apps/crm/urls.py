from django.urls import path
from .views import clientes, ver_cliente, editar_cliente, historial_cliente, proveedores, ver_proveedor, editar_proveedor, historial_proveedor, supplier_list

app_name = 'crm'

urlpatterns = [
    path('', clientes, name='clientes'),
    path('clientes/', clientes, name='clientes'),
    path('clientes/<int:cliente_id>/', ver_cliente, name='ver_cliente'),
    path('clientes/<int:cliente_id>/editar/', editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/historial/', historial_cliente, name='historial_cliente'),
    path('proveedores/', proveedores, name='proveedores'),
    path('proveedores/<int:proveedor_id>/', ver_proveedor, name='ver_proveedor'),
    path('proveedores/<int:proveedor_id>/editar/', editar_proveedor, name='editar_proveedor'),
    path('proveedores/<int:proveedor_id>/historial/', historial_proveedor, name='historial_proveedor'),
    path('supplier_list/', supplier_list, name='supplier_list_adap'),  # Keep old one for adap
]
