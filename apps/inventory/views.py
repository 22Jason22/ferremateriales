# pylint: disable=no-member
"""
Module views.py for inventory app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Min, Max, Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from .models import Product, Category, StockMovement
from .serializers import CategorySerializer, ProductSerializer, StockMovementSerializer
from .forms import ProductForm


def product_list(request):
    """Obtener parámetros de filtro"""
    if request.user.role == 'cliente':
        return redirect('catalog')
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

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

    context = {
        'products': products,
        'categories': categories,
        'price_min': price_range['min_price'] or 0,
        'price_max': price_range['max_price'] or 0,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
        'out_of_stock_count': out_of_stock_count,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'inventory/product_list.html', context)


def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado correctamente.')
            return redirect('inventory:product_list')
    else:
        form = ProductForm()

    context = {
        'form': form
    }

    if request.GET.get('modal') == '1':
        return render(request, 'inventory/_product_form.html', context)
    
    return render(request, 'inventory/product_add.html', context)


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product
    }

    if request.GET.get('modal') == '1':
        return render(request, 'inventory/_product_form.html', context)

    return render(request, 'inventory/product_edit.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('inventory:product_list')
    
    context = {
        'product': product
    }

    if request.GET.get('modal') == '1':
        return render(request, 'inventory/product_confirm_delete.html', context)
    
    return render(request, 'inventory/product_confirm_delete.html', context)


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


@login_required
def catalog(request):
    """Vista del catálogo de productos para clientes finales"""
    if request.user.role not in ['cliente', 'admin']:
        return redirect('inventory:product_list')

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
