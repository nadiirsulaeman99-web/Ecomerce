from .tasks import send_order_email_thank, send_order_email_products
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderCreateForm, OrderPayForm
from .models import OrderItem, Order
from django.conf import settings
from cart.cart import Cart

#PDF
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
import os

from django.contrib.auth.decorators import login_required

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order':order})
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


@login_required(login_url='acounts:login')
def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form_a = OrderCreateForm(request.POST)
        form_b = OrderPayForm(request.POST, cart=cart)
        
        if form_a.is_valid() and form_b.is_valid():
            order_data     = form_a.save()

            payment_data = form_b.save(commit=False)
            payment_data.order = order_data
            payment_data.paid = True
            payment_data.save()
            

            for item in cart:
                OrderItem.objects.create(order=order_data, product=item['product'], price=item['price'], quantity=item['quantity'])

            #send email_of_thank_claint.
            order_id = order_data.order_id
            send_order_email_thank.delay(order_id)

            # clear the sissen
            cart.clear()
            #paid True
            order_data.paid = True
            order_data.save()
            return redirect('orders:order_success', order_id = order_id)
    else:
        form_a = OrderCreateForm()
        form_b = OrderPayForm(cart=cart)
    context ={
        'form_a':form_a,
        'form_b':form_b,
        'cart':cart,
    }
    return render(request, 'orders/order_create.html', context )


def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    send_order_email_products.delay(order_id)

    context = {'order':order}
    return render(request, 'orders/order_success.html', context )























def payment_data_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderPayForm(request.POST)# hadii sawari ama file-kale lasoo dira ya waxad racin halkan 'request.FILES'
        if form.is_valid():
            payment_data = form.save(commit=False)
            payment_data.order = order
            payment_data.paid = True
            payment_data.save()
            return redirect('orders:pyment_success', order_id=order_id)
    else:
        form = OrderPayForm()
    context = {
        'form':form,
        'order':order,
    }
    return render(request, 'order/pyment_success.html', context )






