from cart.views import *
from django.shortcuts import render,get_object_or_404
from cart import forms
from cart import filters
from django.contrib.auth.decorators import login_required
import requests
from django.core.paginator import Paginator
from .models import *
import json
import pandas as pd
from random import *
from raisingstock.models import *
from django.contrib import messages
from UserControl.models import *
from UserControl.decorators import *

def product_off_step_finder(product_off_id,quantity):

    selected_product_off = ProductOff.objects.filter(id = product_off_id).first()

    if quantity< selected_product_off.minQ_1 :
        return 0
    if quantity >= selected_product_off.minQ_1 and quantity<selected_product_off.maxQ_1 :
        return selected_product_off.off_persentage_1
    if quantity >= selected_product_off.minQ_2 and quantity < selected_product_off.maxQ_2:
        return selected_product_off.off_persentage_2
    if quantity >= selected_product_off.minQ_3 and quantity < selected_product_off.maxQ_3:
        return selected_product_off.off_persentage_3
    if quantity >= selected_product_off.minQ_4 and quantity < selected_product_off.maxQ_4:
        return selected_product_off.off_persentage_4


@can_product_view
@login_required (login_url='login')
def product_views(request):
    user = request.user
    slelect_all_products = Product.objects.all ( )
    select_all_warehouse = WareHouseDefinde.objects.last ( )
    access = Access.objects.get(user = user)

    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warhouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    inventory = Inventory.objects.filter (warehouse_id__in = warhouse_list)
    context = {
        'inventory': inventory,
        "accsess":access
    }

    return render (request, 'inventory.html', context)


@login_required (login_url='login')
@can_products_detail
def product_detail(request, id):
    product = Product.objects.get (id=id)
    maincategory = FirstCategory.objects.all ( )


    context = {
        'product': product,
        'maincategory': maincategory,

    }

    return render (request, 'products.html', context)

@login_required (login_url='login')
@can_products_detail
def sub_category(request, sub):
    products = Product.objects.filter (slug=sub)

    context = {
        'products': products,
    }

    return render (request, 'index.html', context)

@login_required (login_url='login')
def index (request):

    page = them.objects.all ( )
    context = {
        'them' : page
    }

    return render(request,'index.html',context)


def randomData(request):

    # data = pd.read_csv("Shop/MOCK_DATA.csv",sep='delimiter', header=None)
    # r = range(1,200)
    # price = range(1,11)
    # vat = 9
    # off = ProductOff.objects.first()
    # box=[5,10,12,20]
    # category = SubCategory.objects.all()
    # stock = 0
    # sell_stock = 0
    #
    # for index , row in data.iterrows() :
    #     print(row.values[0])
    #
    #     Product.objects.create(
    #         category=choice(category),
    #         name=row.values[0],
    #         slug=row.values[0],
    #         price= randrange(1,11),
    #         stock=stock,
    #         sell_stock=sell_stock,
    #         available=True,
    #         vat=vat,
    #         off=off,
    #         box=randrange(0,21,5),
    #     )
    data = Product.objects.filter(box = 0)
    for item in data:
        item.box = 12
        item.save()

    context = {
        'data' : data,

    }

    return render(request,'table.html',context)
@login_required (login_url='login')
@can_auto_inventory_maker
def auto_inventory_maker(request):
    slelect_all_products = Product.objects.all()
    select_all_warehouse = WareHouseDefinde.objects.last()
    if request.method == "POST":
        blank_list = []
        added = 0
        for product in slelect_all_products:

            if  not Inventory.objects.filter(product = product,warehouse = select_all_warehouse):
                Inventory.objects.create(
                    product=product,
                    warehouse=select_all_warehouse,
                    sell_quantity=0,
                    quantity=0,
                )
                added+=1
            else :
                blank_list.append(product.name)
        message = messages.success(request,f"{added} was made succesfuly, {len(blank_list)} are made before  ")

    inventory = Inventory.objects.all()
    context = {
        'inventory' : inventory
    }

    return render(request,'inventory.html',context)
@login_required (login_url='login')
@can_products_detail
def cartext(request,id):

    inventory = Inventory.objects.get(id = id)


    context = {

        "inventory": inventory
    }


    return render(request,'cartext.html',context)