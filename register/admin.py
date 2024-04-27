from django.contrib import admin
from register import models

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'username',
        'is_staff',
        'is_active',
    )
admin.site.register(models.Users, UserAdmin)

class UserAccountAdmin(admin.ModelAdmin):
        list_display = (
        'user',
        'currency',
        'balance',
        'phone_number',
        'address',
        'is_updated',
    )
admin.site.register(models.UserAccount, UserAccountAdmin)