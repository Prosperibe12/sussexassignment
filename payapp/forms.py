from django import forms 
from register import models 
from .models import PaymentRequest

class UserAccountForm(forms.ModelForm):
    phone_number = forms.CharField(label=('Phone Number'), widget=forms.TextInput(attrs={'class':'form-control'}))
    pin = forms.CharField(label=('Pin'), widget=forms.NumberInput(attrs={'class':'form-control'}))
    address = forms.CharField(label=('Address'), widget=forms.Textarea(attrs={'class':'form-control','row':'1'}))
    profile_pix = forms.CharField(label=('Profile Picture'), widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = models.UserAccount
        fields = ['phone_number','profile_pix','pin','currency']
        widgets = {
            'currency': forms.Select(attrs={'class':'form-select'})
        }

class PaymentRequestForm(forms.ModelForm):
    Payer = forms.CharField(label=('Receipient Email'), widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Recipient Email'}))
    amount = forms.CharField(label=('Amount'), widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}))
    request_note = forms.CharField(label=('Request Note'), widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Request Message'}))
    
    class Meta:
        model = PaymentRequest
        fields = ['Payer', 'amount', 'request_note']

class PaymentRequestUpdateForm(forms.ModelForm):
    Payer_approval = forms.BooleanField()
    amount = forms.CharField(label=('Amount'), widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Amount'}))
    payment_note = forms.CharField(label=('Payment Note'), widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Payment Message'}))
    
    class Meta:
        model = PaymentRequest
        fields = ['Payer_approval','payment_note','amount']
        
class RejectPaymentRequestForm(forms.ModelForm):
    payment_note = forms.CharField(label=('Payment Note'), widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Payment Message'}))
    
    class Meta:
        model = PaymentRequest
        fields = ['payment_note']