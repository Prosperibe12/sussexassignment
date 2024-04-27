from django.contrib import admin
from payapp import models

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'Transaction_id',
        'amount',
        'Initiator',
        'Receiver',
        'transaction_ref',
        'Transaction_status',
        'Initiator_type',
        'Receiver_type',
    )
admin.site.register(models.Transaction, TransactionAdmin)

class PaymentRequestAdmin(admin.ModelAdmin):
        list_display = (
        'Request_id',
        'transaction_ref',
        'amount',
        'Initiator',
        'Payer',
        'Payer_approval',
        'Transaction_status',
    )
admin.site.register(models.PaymentRequest, PaymentRequestAdmin)