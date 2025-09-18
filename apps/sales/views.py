from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils.timezone import now
from datetime import datetime
from .models import Order
from .forms import OrderForm

def sales_list(request):
    # Filtros
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    customer_id = request.GET.get('customer')
    status = request.GET.get('status')

    sales_qs = Order.objects.all()

    if start_date:
        sales_qs = sales_qs.filter(date__gte=start_date)
    if end_date:
        sales_qs = sales_qs.filter(date__lte=end_date)
    if customer_id and customer_id != 'all':
        sales_qs = sales_qs.filter(customer_id=customer_id)
    if status and status != 'all':
        sales_qs = sales_qs.filter(status=status)

    sales_qs = sales_qs.order_by('-date')

    paginator = Paginator(sales_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Para el filtro de clientes
    from apps.crm.models import Customer
    customers = Customer.objects.all()

    # Estadísticas
    total_amount = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    pending_count = Order.objects.filter(status='pending').count()
    delivered_count = Order.objects.filter(status='delivered').count()

    context = {
        'page_obj': page_obj,
        'customers': customers,
        'statuses': Order.STATUS_CHOICES,
        'filters': {
            'start_date': start_date,
            'end_date': end_date,
            'customer': customer_id,
            'status': status,
        },
        'total_amount': total_amount,
        'pending_count': pending_count,
        'delivered_count': delivered_count,
    }
    return render(request, 'sales/sales_list.html', context)

def sales_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                # For modal, return success response or redirect to list
                return redirect('sales:sales_list')
            return redirect('sales:sales_list')
    else:
        initial = {}
        if 'customer' in request.GET:
            initial['customer'] = request.GET['customer']
        form = OrderForm(initial=initial)
    if request.GET.get('modal') == '1':
        return render(request, 'sales/_sales_form.html', {'form': form})
    return render(request, 'sales/sales_form.html', {'form': form})

def sales_edit(request, pk):
    sale = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                return redirect('sales:sales_list')
            return redirect('sales:sales_list')
    else:
        form = OrderForm(instance=sale)
    if request.GET.get('modal') == '1':
        return render(request, 'sales/_sales_form.html', {'form': form, 'sale': sale})
    return render(request, 'sales/sales_form.html', {'form': form, 'sale': sale})
