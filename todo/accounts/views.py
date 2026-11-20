from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# Create your views here.

def login_view(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            
            login(request, user)
            return redirect('index')

        
    context = {

        'title': 'Login',
    }
    
    return render(request, 'login.html', context)

def register_view(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect('index')
        
    else:
        form = UserCreationForm()
        
    context = {
        'form': form,
        'title': 'Register',
    }
    
    return render(request, 'register.html', context)