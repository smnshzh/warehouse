from django.contrib import admin
from .models import *


class FirstCategoryAdmin (admin.ModelAdmin):
    list_display = ['name', 'slug']

    prepopulated_fields = {'slug': ('name',)}


admin.site.register (FirstCategory, FirstCategoryAdmin)


class SubCategoryAdmin (admin.ModelAdmin):
    list_display = ('mainCategory', 'name', 'slug')

    prepopulated_fields = {'slug': ('name',)}


admin.site.register (SubCategory, SubCategoryAdmin)


class ProductAdmin (admin.ModelAdmin):
    list_display = ['slug', 'name', 'category', 'salestate', 'description', 'price', 'stock', 'available', 'created',
                    'updated', 'off', 'box']
    list_editable = ['name', 'description', 'price', 'available', 'salestate', 'off']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register (Product, ProductAdmin)


class StateAdmin (admin.ModelAdmin):
    list_display = ('state', 'slug')

    prepopulated_fields = {'slug': ('state',)}


admin.site.register (Product_Sale_State, StateAdmin)

admin.site.register (ProductOff)

admin.site.register (them)

admin.site.register (WareHouseDefinde)
admin.site.register (Inventory)
