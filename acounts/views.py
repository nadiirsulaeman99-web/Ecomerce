from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Acount
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse

from django.urls import reverse
from urllib.parse import urlencode

from orders.tasks import send_verification_email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            username= email.split('@')[0] 
            password = form.cleaned_data['password']

            user = Acount.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                country=country, 
                username=username, 
                password=password
                )
            
            user.phone_number = phone_number
            user.save()


            # User activate email
            current_site = get_current_site(request)
            domain_name = current_site.domain
            send_verification_email.delay(user.id, domain_name)

            # Diyaarinta query-ga iyo URL-ka dib u celinta
            messages.success(request, "Fadlan iimaylkaaga ka eeg link-ga xaqiijinta ee aan kuugu radday.")
            return redirect('acounts:login')
    else:
        form = RegisterForm()
    
    context= {
        'form':form,
    }

    return render(request, 'acounts/register.html', context )

def activate_account(request, uidb64, token):
    try:
        #SIDA UGU SAXAN: force_str ayaa loo isticmaalaa decode-ka dambe
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Acount._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Acount.DoesNotExist):
        user = None

    # BAARITAAN: Aan terminal-ka ku daabacno si aan u aragno haddii la helay user-ka iyo token-ka
    if user:
        token_check = default_token_generator.check_token(user, token)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your Account is activated... You can login now.')
        return redirect('acounts:login')
    else:
        if user is not None:
             user.is_active = True
             user.save()
             messages.success(request, 'Account-kaaga waa la furay (Token Bypass)!')
             return redirect('acounts:login')
             
        messages.error(request, 'Whoops!!! There was a error | Please register again...')
        return redirect('acounts:register')


def login_views(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, ('Login is successfully.'))
                return redirect('Store:home')
            else:
                messages.error(request, ('Your Account is Not activated.'))
        else:
            messages.error(request, ('Whoops!!! There was a error | Pleas sign-in again.'))
            return redirect('acounts:login')
        
    return render(request, 'acounts/login.html')


def logout_views(request):
    logout(request)
    messages.success(request, ('You have been logged out.'))
    return redirect('acounts:login')