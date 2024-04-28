from django.shortcuts import render, redirect, get_object_or_404
from django.views import View 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db import transaction

from register import models 
from .models import (Transaction, PaymentRequest)
from . import forms 
from . import utils as u

class DashBoard(LoginRequiredMixin, View):
    """
    This view renders the default page of the dashboard. 81 42 45 58 98 38
    """
    login_url = "login"
    redirect_field_name = "login"
    
    def get(self, request):
        # validates if user has updated profile page or send to profile page
        try:
            user_updated = models.UserAccount.objects.get(user=request.user)
        except:
        # if not user_updated:
            return redirect('profile')

        # get user transactions
        trans = Transaction.objects.filter(Q(Initiator=request.user) | Q(Receiver=request.user)).order_by('-Transaction_id')[:10]
        # get payment requests
        payments = PaymentRequest.objects.filter(Q(Initiator=request.user) | Q(Payer=request.user)).order_by('-Request_id')
        payment = payments.filter(Transaction_status='Pending')[:10]
        notification = payments.filter(Q(Transaction_status='Rejected') | Q(Transaction_status='Completed'),Initiator=request.user)[:6]
        context = {
            "Title": "Dashboard",
            "acct": user_updated,
            "trans": trans,
            "payments": payment,
            "chats": notification
        }
        return render(request, 'dashboard/adminindex.html', context)
    
class Userprofile(LoginRequiredMixin, View):
    """
    This view renders the profile page
    Users are required to update their profile upon sign up.
    """
    login_url = "login"
    redirect_field_name = "login"
    form_class = forms.UserAccountForm()
    
    def get(self, request):

        context = {
            "Title": "Profile",
            "form": self.form_class
        }
        return render(request, 'dashboard/profile.html', context)
    
    def post(self, request):
        '''
        create user account details
        '''
        # create a form form instance from HTTP request data
        form = forms.UserAccountForm(request.POST, request.FILES)
        
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            pin = form.cleaned_data.get('pin')
            currency = form.cleaned_data.get('currency')
            address = form.cleaned_data.get('address')
            profile_pix = form.cleaned_data.get('profile_pix')
            balance = u.convert_currency(currency)
            models.UserAccount.objects.create(
                user = request.user,
                phone_number = phone_number,
                balance = balance,
                pin = pin,
                currency = currency,
                address = address,
                profile_pix = profile_pix,
                is_updated = True
            )
            messages.success(request, 'Account Updated Successfully')
            return redirect('dashboard')
        
        return render(request, 'dashboard/adminindex.html')

class AddFunds(LoginRequiredMixin, View):
    """
    This view handles logic for users adding funds in account. 
    It only increases the users default account balance. This can be connected to external source(out of scope for this assignment)
    """
    login_url = "login"
    redirect_field_name = "login"
    
    def get(self, request):
        # get user acct profile
        user_acct = request.user.useraccount
        context = {
            "Title": "Transfer Funds",
            "acct": user_acct
        }
        return render(request, 'dashboard/addfunds.html', context)
    
    def post(sellf, request):
        # get http params 
        amount = int(request.POST.get('amount'))
        # get account details 
        try:
            account = models.UserAccount.objects.get(user=request.user)
        except models.UserAccount.DoesNotExist:
            messages.warning(request,'Cannot Add money')
            return redirect('add')
        
        # update account amount
        account.balance +=amount
        account.save()
        messages.success(request,'Credited Sucessfully')
        return redirect('dashboard')
        
class TransferFunds(LoginRequiredMixin,View):
    """
    All transfer funds logic are handles in this view.
    """
    login_url = "login"
    redirect_field_name = "login"
    
    def get(self, request):
        # get user acct profile
        user_acct = request.user.useraccount
        context = {
            "Title": "Transfer Funds",
            "acct": user_acct
        }
        return render(request, 'dashboard/transfer.html', context)
    
    def post(self, request):
        # get http params
        receipient = request.POST.get('receipient')
        amount = int(request.POST.get('amount'))
        pin = int(request.POST.get('pin'))
        sender = request.user.email
        '''
        I have decided to abstract the core functionalities of sending money. 
        the makes the view more readable and the SendMoney class easy to maintain
        '''
        # Instantiate the SendMoney class
        send_money_command = u.SendMoney(sender, receipient, amount, pin)
        # execute method to perform transaction
        output = send_money_command.execute()
        if output is True:
            messages.success(request,"Transferred Successfully.")
            # Redirect to dashboard
            return redirect('dashboard')
        messages.warning(request, output)
        return redirect("transfer")

class RequestFunds(LoginRequiredMixin,View):
    """
    All payment request logic are handles in this view.
    Methods:
        get(): returns default page.
        post(): accepts http params and perfom logic for payment request. 
    """
    login_url = "login"
    redirect_field_name = "login"
    form_class = forms.PaymentRequestForm()
    
    def get(self, request):
        # get user acct profile
        user_acct = request.user.useraccount
        context = {
            "Title": "Request Funds",
            "acct": user_acct,
            "form": self.form_class
        }
        return render(request, 'dashboard/request.html', context)
    
    def post(self, request):
        '''
        The method will handle logic for payment request
        '''        
        # # get http params
        payer = request.POST.get('payer')
        amount = request.POST.get('amount')
        request_note = request.POST.get('message')
        
        # validate that the payer exist
        try:
            check_payer = models.Users.objects.get(email=payer)
        except models.Users.DoesNotExist:
            messages.warning(request, 'User Does not exist.')
            return redirect('request')
        
        if check_payer is not None:
            # create a payment request
            '''I have used atomicity within a context manager 
                This will guarantee ACID properties.
            '''
            with transaction.atomic():
                try:
                    PaymentRequest.objects.create(
                        amount=amount,
                        Initiator=request.user,
                        Payer=check_payer,
                        request_note=request_note,
                        Transaction_status='Pending'
                    )
                    # send a notification to payer, this will be offloaded as a background task
                    messages.success(request,'Payment Request sent. Wait for Appproval')
                    return redirect('dashboard')
                except:
                    messages.warning(request, 'Please try again')
                    return redirect('request')
                
class ConfirmPaymentRequest(LoginRequiredMixin,View):
    """
    This view allows for confirming payment request. 
    """
    login_url = "login"
    redirect_field_name = "login"
    
    def get(self, request, id):
        # get user acct profile
        user_acct = request.user 
        # get paymentrequest details 
        pay = get_object_or_404(PaymentRequest, Request_id=id)
        # pass payment instance to form
        form_class = forms.PaymentRequestUpdateForm(instance=pay)

        context = {
            "Title": "Confirm Payment",
            "acct": user_acct,
            "form": form_class
        }
        return render(request, 'dashboard/payment.html', context)
    
    def post(self, request, id):
        '''
        Confirm payment request 
        The view updates the PaymentRequest resource by getting the id from url params:
            1. get instance of PaymentRequest class 
            2. get form values, validate and update. 
            3.  Instatiate the SendMoney class
        '''
        pay = get_object_or_404(PaymentRequest, Request_id=id)
        # create a form form instance from HTTP request data
        form = forms.PaymentRequestUpdateForm(request.POST, instance=pay)
        
        # validate form
        if form.is_valid():
            # get validated data
            amount = int(form.cleaned_data.get('amount'))
            pin = request.user.useraccount.pin
            pay.Transaction_status = 'Completed'
            form.save()
            # Instantiate the SendMoney class
            send_money_command = u.SendMoney(pay.Payer, pay.Initiator, amount, pin)
            # execute method to perform transaction
            output = send_money_command.execute()
            if output is True:
                # send notification to Initiator that payment has been made(use celery)
                messages.success(request,"Transferred Successfully.")
                # Redirect to dashboard
                return redirect('dashboard')
            messages.warning(request, output)
            return redirect("dashboard")
        return render(request, 'dashboard/payment.html')
    
class RejectPaymentRequest(LoginRequiredMixin,View):
    """
    I have decided that a different view handle PaymentRequest rejection. 
    This is so that each view is responsible for a single functionality
    """
    login_url = "login"
    redirect_field_name = "login"
    
    def get(self, request, id):
        # get user acct profile
        user_acct = request.user 
        # get paymentrequest details 
        pay = get_object_or_404(PaymentRequest, Request_id=id)
        # pass payment instance to form
        form_class = forms.RejectPaymentRequestForm(instance=pay)

        context = {
            "Title": "Reject Payment",
            "acct": user_acct,
            "form": form_class
        }
        return render(request, 'dashboard/rejection.html', context)
    
    def post(self, request, id):
        """
        Reject payment request
        """
        pay = get_object_or_404(PaymentRequest, Request_id=id)
        # create a form form instance from HTTP request data
        form = forms.RejectPaymentRequestForm(request.POST, instance=pay)
        # validate form
        if form.is_valid():
            pay.Transaction_status = 'Rejected'
            form.save()
            # send notification to Initiator that payment was rejected
            messages.success(request,'Payment Rejected Sucessfully')
            return redirect('dashboard')
        return render(request, 'dashboard/rejection.html')