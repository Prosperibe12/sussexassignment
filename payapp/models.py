import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models

from register.models import HelperModel, Users

class Transaction(HelperModel,models.Model):
    """
    All Transaction related record will be stored in this table. 
    """
    status = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    )
    choice = (
        ('Credit', 'Credit'),
        ('Debit', 'Debit')
    )
    Transaction_id = models.BigAutoField(primary_key=True)
    amount = models.IntegerField(blank=False, null=False)
    Initiator = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="transaction_initiator",null=True,blank=True)
    Receiver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="transaction_receiver",null=True,blank=True)
    transaction_ref = models.CharField(max_length=100,blank=False,null=False)
    payment_note = models.CharField(max_length=250,blank=True,null=True)
    Transaction_status = models.CharField(choices=status, max_length=200, blank=False, null=False)
    Initiator_type = models.CharField(choices=choice, blank=False, null=False, max_length=200)
    Receiver_type = models.CharField(choices=choice, blank=False, null=False,max_length=200)
    
    def __str__(self) -> str:
        return f'{self.Transaction_id}'
    
    # generate transaction_ref code
    def save(self, *args, **kwargs):
        while not self.transaction_ref:
            ref = secrets.token_urlsafe(25)
            obj_with_sm_ref = Transaction.objects.filter(transaction_ref=ref)
            if not obj_with_sm_ref:
                self.transaction_ref = ref 
        super().save(*args, **kwargs)

class PaymentRequest(HelperModel,models.Model):
    """
    PaymentRequest transaction related record will be stored in this table. 
    """
    status = (
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed')
    )
    Request_id = models.BigAutoField(primary_key=True)
    amount = models.IntegerField(blank=False, null=False)
    Initiator = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="request_initiator",null=True,blank=True)
    Payer = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="request_payer",null=True,blank=True)
    transaction_ref = models.CharField(max_length=100,blank=False,null=False)
    Payer_approval = models.BooleanField(default=False,blank=True,null=True)
    request_note = models.TextField(blank=True, null=True)
    payment_note = models.TextField(max_length=250,blank=True,null=True)
    Transaction_status = models.CharField(choices=status, max_length=200, blank=False, null=False, default='Pending')

    # generate transaction_ref code
    def save(self, *args, **kwargs):
        while not self.transaction_ref:
            ref = secrets.token_urlsafe(20)
            obj_with_sm_ref = PaymentRequest.objects.filter(transaction_ref=ref)
            if not obj_with_sm_ref:
                self.transaction_ref = ref 
        super().save(*args, **kwargs)