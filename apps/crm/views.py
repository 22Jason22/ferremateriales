from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Customer, Lead
from django.utils.timezone import now
from datetime import timedelta
from .forms import CustomerForm
from django.contrib import messages

def clientes(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('/clientes/')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
            # Keep the form with data and errors to show in modal
    else:
        form = CustomerForm()

    # Obtener filtros desde GET
    nombre = request.GET.get('nombre', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    estado = request.GET.get('estado', '').strip()

    # Query inicial
    clientes_qs = Customer.objects.all()

    # Aplicar filtros
    if nombre:
        clientes_qs = clientes_qs.filter(name__icontains=nombre)
    if tipo:
        clientes_qs = clientes_qs.filter(client_type=tipo)
    if estado:
        clientes_qs = clientes_qs.filter(status=estado)

    # Paginación
    paginator = Paginator(clientes_qs.order_by('name'), 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Estadísticas
    clientes_activos = Customer.objects.filter(status=Customer.Status.ACTIVO).count()
    clientes_morosos = Customer.objects.filter(status=Customer.Status.MOROSO).count()
    nuevos_mes = Customer.objects.filter(
        created_at__gte=now() - timedelta(days=30)
    ).count()

    # Para ventas este mes, asumimos que hay un modelo o método para calcularlo
    # Por ahora lo dejamos en 0 o se puede implementar luego
    ventas_mes = 0

    context = {
        'page_obj': page_obj,
        'stats': {
            'clientes_activos': clientes_activos,
            'clientes_morosos': clientes_morosos,
            'nuevos_mes': nuevos_mes,
            'ventas_mes': ventas_mes,
        },
        'client_types': Customer.ClientType.choices,
        'statuses': Customer.Status.choices,
        'form': form,
    }
    return render(request, 'crm/clientes.html', context)


def ver_cliente(request, cliente_id):
    """
    Vista para ver los detalles de un cliente específico.
    """
    cliente = get_object_or_404(Customer, id=cliente_id)
    context = {
        'cliente': cliente,
        'modal': request.GET.get('modal') == '1',
    }
    return render(request, 'crm/ver_cliente.html', context)


def editar_cliente(request, cliente_id):
    """
    Vista para editar un cliente existente.
    """
    cliente = get_object_or_404(Customer, id=cliente_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            if request.GET.get('modal') == '1':
                # Si es modal, devolver respuesta JSON o redirigir a la lista
                return redirect('crm:clientes')
            else:
                return redirect('crm:ver_cliente', cliente_id=cliente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = CustomerForm(instance=cliente)
    context = {
        'form': form,
        'cliente': cliente,
    }
    if request.GET.get('modal') == '1':
        return render(request, 'crm/_editar_cliente_form.html', context)
    else:
        return render(request, 'crm/editar_cliente.html', context)


def historial_cliente(request, cliente_id):
    """
    Vista para mostrar el historial de un cliente (leads relacionados).
    """
    cliente = get_object_or_404(Customer, id=cliente_id)
    leads = Lead.objects.filter(customer=cliente).order_by('-created_at')
    context = {
        'cliente': cliente,
        'leads': leads,
    }
    return render(request, 'crm/historial_cliente.html', context)
