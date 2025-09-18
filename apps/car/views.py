from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from urllib.parse import quote
from .models import Cart, CartItem
from apps.inventory.models import Product

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = cart.get_total_price()
    total_items = cart.get_total_items()
    
    # Build WhatsApp message
    message = "Hola, quiero concretar la venta.\n\nCarrito:\n"
    for item in items:
        message += f"- {item.quantity} x {item.product.name} = ${item.get_total_price()}\n"
    message += f"\nTotal: ${total_price}"
    whatsapp_message = quote(message)
    
    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
        'whatsapp_message': whatsapp_message,
    }
    return render(request, 'car/cart_detail.html', context)

@login_required
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    
    cart_item_count = cart.get_total_items()
    return JsonResponse({
        'success': True,
        'cartItemCount': cart_item_count,
        'message': f'{product.name} agregado al carrito.'
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('cart:cart_detail')

@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    item_removed = False

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        message = 'Cantidad actualizada.'
    else:
        cart_item.delete()
        message = 'Producto eliminado del carrito.'
        item_removed = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        
        response_data = {
            'success': True,
            'message': message,
            'cart_total': cart.get_total_price(),
            'total_items': cart.get_total_items(),
            'item_id': item_id,
            'item_removed': item_removed,
        }

        if not item_removed:
            response_data['item_total'] = cart_item.get_total_price()
            response_data['quantity'] = cart_item.quantity

        return JsonResponse(response_data)
    
    messages.success(request, message)
    return redirect('cart:cart_detail')
