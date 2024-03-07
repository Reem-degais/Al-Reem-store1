from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from cart.models import Cart, CartItem
import requests
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from orders.models import Order, OrderProducts


#registration of new user 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = first_name + ' ' + last_name
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()

            #Activate user account  
            current_site = get_current_site(request)
            mail_subject = 'Activaite your account'
            message = render_to_string('verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_address = email
            send_email = EmailMessage(mail_subject, message, to=[email_address])
            send_email.send()

           # messages.success(request, 'Registration seccessful.')
            return redirect('/accounts/login/?command=verification&email='+email)
        
           

        
            
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
    }

    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
                
            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you logged out')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(ValueError, TypeError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'dashboard.html')


def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('resetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_address = email
            send_email = EmailMessage(mail_subject, message, to=[email_address])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgetPassword')
    return render(request, 'forgetPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'resetPassword.html')
    
@login_required(login_url= 'login')
def my_order(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    counter =1
    context = {
        'orders': orders,
        'counter': counter,
    }
    return render(request, 'my_orders.html', context)

@login_required(login_url= 'login')
def my_order_details(request, order_id):
    order_details = OrderProducts.objects.filter(order__order_number=order_id )
    order = Order.objects.get(order_number=order_id)
    total = 0
    for item in order_details:
        total += item.product_price * item.quantity
    context = {
        'order_details': order_details,
        'order': order,
        'total': total,
    }
    return render (request, 'my_order_details.html', context)

def changepassword(request):
    if request.method == 'POST':
        user = Account.objects.get(username__iexact=request.user.username)
        current_password = request.POST['current_password']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        checkPassword = user.check_password(current_password)
        
        if password == confirm_password:
            if checkPassword:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return redirect('changepassword')
            else:
                messages.error(request, 'enter valid password!')
                return redirect('changepassword') 
        else:
            messages.error(request, 'Password do not match!')
            return redirect('changepassword')
    else:
         return render(request, 'changepassword.html')
    