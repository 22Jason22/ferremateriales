# pylint: disable=no-member
"""
Module views.py for inventory app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Min, Max, Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from rest_framework import viewsets

from .models import Product, Category, StockMovement
from .serializers import CategorySerializer, ProductSerializer, StockMovementSerializer
from .forms import ProductForm


def product_list(request):
    """Obtener parámetros de filtro"""
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    # Initialize forms
    add_form = ProductForm(prefix='add')
    
    context = {
        'open_modal': None
    }

    # Handle POST requests
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            add_form = ProductForm(request.POST, request.FILES, prefix='add')
            if add_form.is_valid():
                add_form.save()
                return redirect('inventory:product_list')
            else:
                context['open_modal'] = 'add'
        elif action == 'edit':
            pk = request.POST.get('pk')
            product = get_object_or_404(Product, pk=pk)
            edit_form = ProductForm(request.POST, request.FILES, instance=product, prefix=f'edit-{pk}')
            if edit_form.is_valid():
                edit_form.save()
                return redirect('inventory:product_list')
            else:
                # This part is tricky, as we need to pass the invalid form back to the specific product
                # We will handle this by re-creating the product list and replacing the form for the specific product
                context['open_modal'] = f'edit-{pk}'
                context['invalid_edit_form'] = edit_form
                context['invalid_edit_pk'] = pk

        elif action == 'delete':
            pk = request.POST.get('pk')
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            return redirect('inventory:product_list')

    # Filtrar productos según búsqueda y categoría
    products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    # Filtrar por rango de precios
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Obtener categorías con conteo de productos
    categories = Category.objects.annotate(product_count=Count('product')).all()

    # Obtener rango de precios para slider
    price_range = products.aggregate(min_price=Min('price'), max_price=Max('price'))

    # Calculate stock counts
    out_of_stock_count = Product.objects.filter(current_stock=0).count()
    low_stock_count = Product.objects.filter(current_stock__gt=0, current_stock__lt=5).count()

    # Crear formularios para edición de cada producto
    for product in products:
        if context.get('invalid_edit_pk') == str(product.pk):
            product.edit_form = context['invalid_edit_form']
        else:
            product.edit_form = ProductForm(instance=product, prefix=f'edit-{product.pk}')


    context.update({
        'products': products,
        'categories': categories,
        'price_min': price_range['min_price'] or 0,
        'price_max': price_range['max_price'] or 0,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
        'add_form': add_form,
        'out_of_stock_count': out_of_stock_count,
        'low_stock_count': low_stock_count,
    })
    return render(request, 'inventory/product_list.html', context)


class CategoryViewSet(viewsets.ModelViewSet):
    """zzz"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """zzz"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StockMovementViewSet(viewsets.ModelViewSet):
    """zzz"""
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer


def catalog(request):
    """Vista del catálogo de productos para clientes finales"""
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    page_number = request.GET.get('page', 1)

    # Filtrar productos
    products = Product.objects.order_by('-pk')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Ordenar por relevancia o precio
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'new':
        products = products.order_by('-is_new', 'name')
    else:
        products = products.order_by('name')

    # Paginación
    paginator = Paginator(products, 12)  # 12 productos por página
    page_obj = paginator.get_page(page_number)

    # Obtener categorías con conteo
    categories = Category.objects.annotate(product_count=Count('product')).all()

    # Rango de precios
    price_range = products.aggregate(min_price=Min('price'), max_price=Max('price'))

    context = {
        'products': page_obj,
        'categories': categories,
        'price_min': price_range['min_price'] or 0,
        'price_max': price_range['max_price'] or 1000,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
        'sort_by': sort_by,
        'page_obj': page_obj,
    }
    return render(request, 'catalogo/index.html', context)
