# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('product_detail', pk=pk)

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for pk, qty in cart.items():
        prod = get_object_or_404(Product, pk=int(pk))
        products.append({'product': prod, 'quantity': qty})
        total += prod.price * qty
    return render(request, 'shop/cart.html', {'products': products, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')
    order = Order.objects.create(user=request.user)
    for pk, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pk))
        OrderItem.objects.create(order=order, product=product, quantity=qty)
    request.session['cart'] = {}
    return render(request, 'shop/order.html', {'order': order})