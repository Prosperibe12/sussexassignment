from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate

from . import forms 
from . import models

class Index(View):
    """
    This view renders the index page for Webapps2024 Project
    """
    def get(self, request):
        context = {
            "Title": "CoinPouch - Wallet App"
        }
        return render(request, 'web/index.html', context)

class Register(View):
    """
    This view handles the register logic for this application.
    get() method renders the Register page for Webapps2024 Project. 
    post() validates users registration process. 
    """
    form_class = forms.RegisterForm()
    
    def get(self, request):
        context = {
            "Title": "Register",
            "form": self.form_class
        }
        return render(request, 'web/register.html', context)
    
    def post(self, request):
        '''' 
        Accepts post request for account registration
        '''
        # create a form instance and populate it with data from the request:
        form_data = forms.RegisterForm(request.POST or None)
        # validate form data
        if form_data.is_valid():
            
            # get form cleaned data
            username = form_data.cleaned_data.get('username')
            email = form_data.cleaned_data.get('email')
            password = form_data.cleaned_data.get('password')
            full_name = form_data.cleaned_data.get('full_name')
            
            # validate if username and email exists
            user_exists = models.Users.objects.filter(email=email).exists() or models.Users.objects.filter(username=username).exists()
            if user_exists:
                messages.warning(request, 'Username or Email already exist')
                return redirect('register')
            
            # ceate user  
            models.Users.objects.create_user(email=email, password=password,username=username,full_name=full_name)
            messages.success(request, 'Registered Successfully')
            return redirect('login')
        
        return render(request, 'web/register.html')

class LoginPage(View):
    """
    This view renders the Login page for Webapps2024 Project
    """
    def get(self, request):
        context = {
            "Title": "Login Page"
        }
        return render(request, 'web/login.html', context)
    
    def post(self, request):
        # get posted email and password
        username = request.POST.get('email')
        password = request.POST.get('password')
        # authenticate user
        user = authenticate(username=username, password=password)
        # validate user
        if user is not None: 
            login(request, user)
            messages.success(request, 'Logged In Successfully')
            # redirect to dashboard
            return redirect('dashboard') 
                   
        messages.warning(request, 'Invalid Username or Password')
        return redirect('login')
        
class LogoutView(View):
    """
    This view handles logout functionality
    """
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect('login')
