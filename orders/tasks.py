from django.core.mail import send_mail
from django.conf import settings
from cart.cart import Cart
from .models import Order
from celery import shared_task
#pdf
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint


@shared_task
def send_order_email_thank(order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        #Email conf
        subject = 'Dalabkaaga waa la xaqiijiyay.'
        message = f"Mudane/Marwo {order.get_full_name().upper()},\n\n" \
                f"Waad ku mahadsantahay dalabkaaga. Waxaan si guul leh u helnay dalabkaaga oo\n" \
                f"tixraaciisu yahay #[ID:{order.order_id}]\n\n" \
                f"Waad ku mahadsantahay doorashadaada!"

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [order.email]
        return send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except order.DoesNotExist:
        return f"Order {order_id} lama helin."



@shared_task
def send_order_email_products(order_id):
    order = Order.objects.get(order_id=order_id)
    
    #send email success ordering and payment.
    subject = 'Order Confiramtion'
    message = f'Your order has been created successfuly...\nOrder ID:( {order.order_id} )'
    from_email = settings.DEFAULT_FROM_EMAIL
    user_email = [order.email]

    html = render_to_string('orders/pdf.html', {'order':order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=user_email
    )

    email.attach(f'order_{order.order_id}.pdf', out.getvalue(), 'application/pdf')
    email.send()
    return True



from acounts.models import Acount
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_id, **kwargs):
    instance = Acount.objects.get(id=user_id)
    subject = 'Welcome to DJANGO-ECOM'
    message = (
        f'Hi {instance.get_short_name()},\n'
        f'Ku soo dhawaow [DJANGO-ECOM] Waad ku mahadsan tahay inaad nagu soo biirtay\n'
        f'Waxaan diyaar kuula nahay adeeg hufan, tayo sare, iyo dammaanad buuxda\nKa dukaamayso si badqab leh ^_^'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [instance.email]
    send_mail(subject, message, from_email, recipient_list)



from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

@shared_task
def send_verification_email(user_id, domain_name):
    try:
        user = Acount.objects.get(id=user_id)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://{domain_name}/accounts/activate/{uid}/{token}/"

        subject = 'please activate your acount'
        message = f"Hi {user.username},\n\nFadlan guji link-gan si aad u xaqiijiso Email-kaga:\n{activation_link}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except user.DoesNotExist:
        pass