from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Store.models import Product
from coupons.froms import CouponForm
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required



@require_POST 
@login_required(login_url='acounts:login')
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        return redirect('cart:cart_detail') # 1. Halkan wuu ku laabanayaa haddii foomku sax yahay
        
    # ====== KAN AYAA REEBAY ERROR-KA (Haddii foomku xumaado) ======
    # Haddii foomku sax noqon waayo, dib ugu celi boggii uu ka yimid (Home ama Detail)
    return redirect(request.META.get('HTTP_REFERER', 'Store:home'))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, status = Product.Status.AVAILABLE)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required(login_url='acounts:login')
def cart_detial(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item['quantity'],
            'override':True
        })

    coupon_form = CouponForm()
    context = {
        'cart':cart,
        'coupon_form':coupon_form,
               
        }
    return render(request, 'cart/cart_detail.html', context )