#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ferremateriales.settings')
sys.path.append('.')
django.setup()

from apps.crm.models import Customer
from apps.sales.models import Order

print("=== VERIFICACIÓN DE DATOS ===")

# Verificar clientes
customers = Customer.objects.all()
print(f"Total de clientes: {customers.count()}")

for customer in customers[:5]:  # Solo los primeros 5
    print(f"\nCliente: {customer.name}")
    print(f"  Last Purchase: {customer.last_purchase}")

    # Verificar órdenes del cliente
    orders = Order.objects.filter(customer=customer).order_by('-date')
    print(f"  Órdenes: {orders.count()}")

    if orders.exists():
        last_order = orders.first()
        print(f"  Última orden: {last_order.order_number} - {last_order.date}")
    else:
        print("  No tiene órdenes")

print("\n=== ÓRDENES RECIENTES ===")
recent_orders = Order.objects.all().order_by('-date')[:5]
for order in recent_orders:
    print(f"Orden: {order.order_number} - Cliente: {order.customer.name} - Fecha: {order.date}")
