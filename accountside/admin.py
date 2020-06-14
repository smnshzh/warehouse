from django.contrib import admin
from .models import *


class RegionAdmin(admin.ModelAdmin):
    list_display = ['city' ,
    'local_name',
    'local_code',
    ]


admin.site.register(local_id_def,RegionAdmin)

class AccountsideAdmin(admin.ModelAdmin):

    list_display = ['slug','name' ,
    'telephonnumber',
    'region' ,
    'address' ,
    'credit' ,
    'property',
    'area' ,
    'id_code',
    ]

    list_editable = ['name',
    'telephonnumber',
    'region' ,
    'address' ,
    'credit' ,
    'property',
    'area' ,
    'id_code', ]

    prepopulated_fields = {'slug': ('name',)}

admin.site.register(accountside,AccountsideAdmin)


class KindAdmin(admin.ModelAdmin):
    list_display = [

        'type_code',
        'type_name'
    ]
admin.site.register(kind,KindAdmin)


class AccountGroupAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'name'

    ]

class TotalAccountsAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'name',
        "account_group"
    ]

admin.site.register(TotalAccounts,TotalAccountsAdmin)

class DifinitAccountsAdmin(admin.ModelAdmin):
    list_display = [

        'code',
        'name',

    ]

class SafeBoxAdmin(admin.ModelAdmin):
    list_display = [

        'id',
        'code',
        'name',

    ]



admin.site.register(AccountGroup,AccountGroupAdmin)
admin.site.register(DifinitAccounts,DifinitAccountsAdmin)
admin.site.register(DocumentNumber)
admin.site.register(Document)
admin.site.register(AutoJoournalFields)
admin.site.register(BankPose)
admin.site.register(BankCheck)
admin.site.register(Safe_Box,SafeBoxAdmin)
