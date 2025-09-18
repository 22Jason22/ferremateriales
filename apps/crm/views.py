"""zzz"""
import traceback
import logging
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Supplier
from .forms import CustomerForm, SupplierForm

def clientes(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                return redirect('crm:clientes')
            return redirect('crm:clientes')
        else:
            # If form is invalid and modal, render form with errors
            if request.GET.get('modal') == '1':
                return render(request, 'crm/_nuevo_cliente.html', {'form': form})
    else:
        form = CustomerForm()

    # Filtros
    nombre = request.GET.get('nombre')
    tipo = request.GET.get('tipo')
    estado = request.GET.get('estado')

    customers_qs = Customer.objects.all()

    if nombre:
        customers_qs = customers_qs.filter(name__icontains=nombre)
    if tipo and tipo != '':
        customers_qs = customers_qs.filter(client_type=tipo)
    if estado and estado != '':
        customers_qs = customers_qs.filter(status=estado)

    # Agregar información de última orden a cada cliente
    customers_with_last_order = []
    for customer in customers_qs:
        last_order = customer.order_set.order_by('-date').first()
        customer.last_order = last_order
        customers_with_last_order.append(customer)

    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(customers_with_last_order, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Estadísticas
    stats = {
        'clientes_activos': Customer.objects.filter(status='active').count(),
        'ventas_mes': 0,  # Placeholder
        'clientes_morosos': Customer.objects.filter(status='delinquent').count(),
        'nuevos_mes': Customer.objects.filter(created_at__month=timezone.now().month).count(),
    }

    client_types = Customer.ClientType.choices
    statuses = Customer.Status.choices

    context = {
        'customers': page_obj,  # Cambiar a page_obj para paginación
        'page_obj': page_obj,
        'form': form,
        'stats': stats,
        'client_types': client_types,
        'statuses': statuses,
    }
    return render(request, 'crm/clientes.html', context)

def ver_cliente(request, cliente_id):
    customer = get_object_or_404(Customer, pk=cliente_id)
    if request.GET.get('modal') == '1':
        return render(request, 'crm/_cliente_detail.html', {'cliente': customer, 'modal': True})
    return render(request, 'crm/ver_cliente.html', {'cliente': customer, 'modal': False})

def editar_cliente(request, cliente_id):
    customer = get_object_or_404(Customer, pk=cliente_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                return redirect('crm:clientes')
            return redirect('crm:ver_cliente', cliente_id=cliente_id)
    else:
        form = CustomerForm(instance=customer)
    if request.GET.get('modal') == '1':
        return render(request, 'crm/_editar_cliente.html', {'customer': customer, 'form': form})
    return render(request, 'crm/editar_cliente.html', {'customer': customer, 'form': form})

from apps.sales.models import Order, Quote
from apps.invoicing.models import Invoice
from django.db.models import Sum

def historial_cliente(request, cliente_id):
    customer = get_object_or_404(Customer, pk=cliente_id)
    orders = Order.objects.filter(customer=customer).order_by('-date')
    quotes = Quote.objects.filter(customer=customer).order_by('-date')
    invoices = Invoice.objects.filter(customer=customer).order_by('-date_issued')
    total_amount = invoices.aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'customer': customer,
        'orders': orders,
        'quotes': quotes,
        'invoices': invoices,
        'total_amount': total_amount,
    }

    if request.GET.get('modal') == '1':
        return render(request, 'crm/_historial_cliente.html', context)
    return render(request, 'crm/historial_cliente.html', context)

def proveedores(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                return redirect('crm:proveedores')
            return redirect('crm:proveedores')
        else:
            # If form is invalid and modal, render form with errors
            if request.GET.get('modal') == '1':
                return render(request, 'crm/_nuevo_proveedor.html', {'form': form})
    else:
        form = SupplierForm()
    suppliers = Supplier.objects.all()
    # Stats for suppliers
    stats = {
        'proveedores_activos': Supplier.objects.filter(estado='activo').count(),
        'ordenes_mes': 0,  # Placeholder, need to implement
        'pendientes_pago': 0,  # Placeholder
        'con_alertas': 0,  # Placeholder
    }
    rubros = Supplier.Rubro.choices
    estados = Supplier.Estado.choices
    return render(request, 'crm/proveedores.html', {
        'suppliers': suppliers,
        'form': form,
        'stats': stats,
        'rubros': rubros,
        'estados': estados
    })

def ver_proveedor(request, proveedor_id):
    supplier = get_object_or_404(Supplier, pk=proveedor_id)
    return render(request, 'crm/ver_proveedor.html', {'supplier': supplier})

def editar_proveedor(request, proveedor_id):
    supplier = get_object_or_404(Supplier, pk=proveedor_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                return redirect('crm:proveedores')
            return redirect('crm:ver_proveedor', proveedor_id=proveedor_id)
    else:
        form = SupplierForm(instance=supplier)
    if request.GET.get('modal') == '1':
        return render(request, 'crm/_editar_proveedor.html', {'supplier': supplier, 'form': form})
    return render(request, 'crm/editar_proveedor.html', {'supplier': supplier, 'form': form})

def historial_proveedor(request, proveedor_id):
    supplier = get_object_or_404(Supplier, pk=proveedor_id)
    # TODO: Get purchase history
    history = []  # Placeholder
    return render(request, 'crm/ver_proveedor.html', {'supplier': supplier, 'history': history})

def supplier_list(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crm:proveedores')
    else:
        form = SupplierForm()
    suppliers = Supplier.objects.all()
    return render(request, 'crm/proveedores.html', {'suppliers': suppliers, 'form': form})
