from django import forms 
from register import models

class RegisterForm(forms.ModelForm):
    
    email = forms.CharField(label=('Email'), widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(label=('username'), widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=('Password'), widget=forms.PasswordInput(attrs={'class':'form-control'}))
    full_name = forms.CharField(label=('Full Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
        
    class Meta:
        model = models.Users
        exclude = ['date_joined','is_staff','is_active']
        