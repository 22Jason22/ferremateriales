from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils.timezone import now
from datetime import datetime
from .models import PurchaseOrder
from .forms import PurchaseOrderForm

def purchases_list(request):
    # Filtros
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    supplier_id = request.GET.get('supplier')
    status = request.GET.get('status')

    purchases_qs = PurchaseOrder.objects.all()

    if start_date:
        purchases_qs = purchases_qs.filter(date__gte=start_date)
    if end_date:
        purchases_qs = purchases_qs.filter(date__lte=end_date)
    if supplier_id and supplier_id != 'all':
        purchases_qs = purchases_qs.filter(supplier_id=supplier_id)
    if status and status != 'all':
        purchases_qs = purchases_qs.filter(status=status)

    purchases_qs = purchases_qs.order_by('-date')

    paginator = Paginator(purchases_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Para el filtro de proveedores
    from apps.crm.models import Supplier
    suppliers = Supplier.objects.all()

    # Estadísticas
    total_amount = PurchaseOrder.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    draft_count = PurchaseOrder.objects.filter(status='draft').count()
    confirmed_count = PurchaseOrder.objects.filter(status='confirmed').count()

    context = {
        'purchases': page_obj,
        'suppliers': suppliers,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
        'filters': {
            'start_date': start_date,
            'end_date': end_date,
            'supplier': supplier_id,
            'status': status,
        },
        'total_amount': total_amount,
        'draft_count': draft_count,
        'confirmed_count': confirmed_count,
    }
    return render(request, 'purchases/purchase_list.html', context)

def purchases_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                return redirect('purchases:purchase_list')
            return redirect('purchases:purchase_list')
    else:
        initial = {}
        if 'supplier' in request.GET:
            initial['supplier'] = request.GET['supplier']
        form = PurchaseOrderForm(initial=initial)
    if request.GET.get('modal') == '1':
        return render(request, 'purchases/_purchase_form.html', {'form': form})
    return render(request, 'purchases/purchase_form.html', {'form': form})

def purchases_edit(request, pk):
    purchase = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            if request.GET.get('modal') == '1':
                return redirect('purchases:purchase_list')
            return redirect('purchases:purchase_list')
    else:
        form = PurchaseOrderForm(instance=purchase)
    if request.GET.get('modal') == '1':
        return render(request, 'purchases/_purchase_form.html', {'form': form, 'purchase': purchase})
    return render(request, 'purchases/purchase_form.html', {'form': form, 'purchase': purchase})

def purchase_detail(request, pk):
    purchase = get_object_or_404(PurchaseOrder, pk=pk)
    items = purchase.items.all()
    receipts = purchase.goodsreceipt_set.all()
    context = {
        'purchase': purchase,
        'items': items,
        'receipts': receipts,
    }
    if request.GET.get('modal') == '1':
        return render(request, 'purchases/_purchase_detail.html', context)
    return render(request, 'purchases/purchase_detail.html', context)

def goods_receipt_create(request, pk):
    purchase = get_object_or_404(PurchaseOrder, pk=pk)
    # Simple implementation, assuming GoodsReceiptForm exists
    if request.method == 'POST':
        # For now, just redirect
        return redirect('purchases:purchase_detail', pk=pk)
    return render(request, 'purchases/goods_receipt_form.html', {'purchase': purchase})
