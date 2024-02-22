from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account

# Create your views here.

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
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
    }

    return render(request, 'register.html', context)

def login(request):
    return render(request, 'login.html')

def logout(request):
    return 