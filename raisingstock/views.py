from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
import datetime
from django.contrib import messages
from Shop.models import *
from accountside.models import *
from django.http import HttpResponse, HttpResponseRedirect
from UserControl.models import *
from cart.models import *
from cart.views import can_access_warehouse
from UserControl.decorators import *
from django.contrib.auth.decorators import login_required

@login_required (login_url='login')
@can_confirm_buy_order
def warehouse_confirm_buy_order(request, id=None):
    form = dict (request.POST)
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warhouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    if id == None:
        if request.method == 'POST':

            for key in form.keys ( ):
                if key != 'csrfmiddlewaretoken':
                    selected_buy_order = Order.objects.get (id=int (key), orderkinde_id__in=[1,4])

                    selected_buy_items = OrderItem.objects.filter (order_id=int (key))
                    for item in selected_buy_items:
                        raising_stock = int (item.quantity)
                        selected_product_forRaising = Inventory.objects.get (product_id=item.product.id,
                                                                             warehouse=selected_buy_order.warhouse)
                        selected_product_forRaising.stock += raising_stock
                        selected_product_forRaising.save ( )
                        selected_product_forRaising.sell_stock += raising_stock
                        selected_product_forRaising.save ( )
                    selected_buy_order.checked_out = True
                    selected_buy_order.save ( )
    buy_orders = Order.objects.filter (checked_out_2='False', warhouse_id__in=warhouse_list, orderkinde_id__in=[1,4])
    buy_ordrersIitems = OrderItem.objects.all ( )
    buy_orders_items_orderId = [item.order.id for item in buy_ordrersIitems]
    tik = 1
    context = {
        "title": "Confirm Buy & Sell-Back Orders",
        'orders': buy_orders,
        'items': buy_ordrersIitems,
        "id_order": buy_orders_items_orderId,
        "tik": tik

    }

    return render (request, 'buyorder.html', context)

@login_required (login_url='login')
@can_delete_buy_order
def delete_buy_order(request):
    form = dict (request.POST)
    if request.method == "POST":
        for key in form.keys ( ):
            if key != 'csrfmiddlewaretoken':
                buy_order_select = Order.objects.get (id=int (key))
                if buy_order_select.checked_out != True:
                    buy_order_select.delete ( )
                elif buy_order_select.checked_out_2 == True:
                    message = messages.warning (request,
                                                f" Order {buy_order_select.id} has been Convereted to "
                                                f"Invoice Number {buy_order_select.code} "
                                                f"you can not delete confirmed invoice "
                                                f"Use back buy function ")
                    context = {
                        "message": message
                    }

                else:
                    message = messages.warning (request,
                                                f" Order {buy_order_select.id} has been confirmed buy warehouse for this "
                                                f"function <a href='/stock/buyInvoice'>Deconfirm</a> Order ")
                    context = {
                        "message": message
                    }
                    return redirect ("show_buy_orders")

    return redirect ('show_buy_orders')

@login_required (login_url='login')
@can_show_confirmed_buy
def show_confirmed_buy(request):
    confirmed = 1
    confirm_buy = Order.objects.filter (checked_out_2=True, orderkinde_id=1).order_by ("fianl_code")

    context = {
        "title": "Views Of Confirmed Buy",
        "orders": confirm_buy,
        "confirmed": confirmed
    }

    return render (request, 'buyorder.html', context)

@can_access_warehouse
@can_deconfirm_buy_order
def deconfirm_buy_order(request, id):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warhouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]

    selected_order = Order.objects.get (id=id)
    selected_buy_items = OrderItem.objects.filter (order_id=id)
    blank_list = []

    if selected_order.orderkinde.id == 3:
        return HttpResponseRedirect(reverse("deconfirm_buy_back",args=[id,]))
    if selected_order.orderkinde.id == 1 or selected_order.orderkinde.id == 4 :
        if selected_order.warhouse.id in warhouse_list and selected_order.checked_out_2 == False:
            for item in selected_buy_items:
                falling_stock = item.quantity
                selected_product_forDeconfirm = Inventory.objects.get (product_id=item.product.id,
                                                                       warehouse=selected_order.warhouse)

                new_stock = selected_product_forDeconfirm.stock - int (falling_stock)
                new_sell_stock = selected_product_forDeconfirm.sell_stock - int (falling_stock)
                if new_stock < 0 or new_sell_stock < 0:
                    blank_list.append (selected_product_forDeconfirm.product.name)

            if len (blank_list) != 0:
                for item in blank_list:
                    message = messages.warning (request, f"You can not Deconfirm , you have sold product of this order"
                                                         f"<p>{item}'s stock is Negative</p>")
                    context = {
                        "message": message
                    }
                return redirect ("warehouse_confirm_buy_order")
            else:
                for item in selected_buy_items:
                    falling_stock = item.quantity
                    selected_product_forDeconfirm = Inventory.objects.get (product_id=item.product.id,
                                                                           warehouse=selected_order.warhouse)

                    new_stock = selected_product_forDeconfirm.stock - int (falling_stock)
                    new_sell_stock = selected_product_forDeconfirm.stock - int (falling_stock)
                    selected_product_forDeconfirm.stock = new_stock
                    selected_product_forDeconfirm.save ( )
                    selected_product_forDeconfirm.sell_stock = new_sell_stock
                    selected_product_forDeconfirm.save ( )
                    selected_order.checked_out = False
                    selected_order.save ( )
                return redirect ("warehouse_confirm_buy_order")

        else:
            message = messages.warning (request, "<p>you can not deconfirm this order because of following Errors:</p>"
                                                 "<ol>"
                                                 "<li>You do not access to this Warehouse</li>"
                                                 "<li>Invoice can not Deconfirmed</li>"
                                                 "</ol>")
            context = {
                "message": message
            }
        return redirect ("warehouse_confirm_buy_order")
    return redirect ("warehouse_confirm_buy_order")

@login_required (login_url='login')
@can_warhouse_confirm_buy_back
def warehouse_confirm_buy_back(request, id=None):
    form = dict (request.POST)
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warhouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]

    if id == None:
        if request.method == 'POST':

            for key in form.keys ( ):
                if key != 'csrfmiddlewaretoken':
                    selected_buy_order = Order.objects.get (id=int (key), orderkinde_id=3)
                    blank_list = []
                    selected_buy_items = OrderItem.objects.filter (order_id=int (key))
                    for item in selected_buy_items:
                        raising_stock = int (item.quantity)
                        selected_product_forRaising = Inventory.objects.get (product_id=item.product.id,
                                                                             warehouse=selected_buy_order.warhouse)

                        if selected_product_forRaising.sell_stock - raising_stock < 0:
                            blank_list.append (item.product.name)
                    if len (blank_list) == 0:

                        for item in selected_buy_items:
                            raising_stock = int (item.quantity)
                            selected_product_forRaising = Inventory.objects.get (product_id=item.product.id,
                                                                                 warehouse=selected_buy_order.warhouse)
                            selected_product_forRaising.stock -= raising_stock
                            selected_product_forRaising.save ( )
                            selected_product_forRaising.sell_stock -= raising_stock
                            selected_product_forRaising.save ( )
                        selected_buy_order.checked_out = True
                        selected_buy_order.save ( )
                    else:
                        for item in blank_list:
                            context = {
                                "message": messages.warning (request, f"{item} has not available stock for back ")
                            }
                        return redirect ("warehouse_confirm_buy_back")
    buy_orders = Order.objects.filter (checked_out_2='False', warhouse_id__in=warhouse_list, orderkinde_id=3)
    buy_ordrersIitems = OrderItem.objects.all ( )
    buy_orders_items_orderId = [item.order.id for item in buy_ordrersIitems]
    tik = 1
    context = {
        "title": "Confirm Buy Back",
        'orders': buy_orders,
        'items': buy_ordrersIitems,
        "id_order": buy_orders_items_orderId,
        "tik": tik

    }

    return render (request, 'buyorder.html', context)

@can_access_warehouse
@login_required (login_url='login')
@can_deconfirm_buy_back
def deconfirm_buy_back(request, id):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]

    selected_order = Order.objects.get (id=id)
    selected_buy_items = OrderItem.objects.filter (order_id=id,order__warhouse_id__in = warehouse_list)
    if selected_order.warhouse.id in warehouse_list and selected_order.checked_out_2 == False:

        for item in selected_buy_items:
            falling_stock = item.quantity
            selected_product_forDeconfirm = Inventory.objects.get (product_id=item.product.id,
                                                                   warehouse=selected_order.warhouse)

            new_stock = selected_product_forDeconfirm.stock + int (falling_stock)
            new_sell_stock = selected_product_forDeconfirm.sell_stock + int (falling_stock)
            selected_product_forDeconfirm.stock = new_stock
            selected_product_forDeconfirm.save ( )
            selected_product_forDeconfirm.sell_stock = new_sell_stock
            selected_product_forDeconfirm.save ( )
            selected_order.checked_out = False
            selected_order.save ( )
        context = {
            "message" : messages.info(request,f"You have deconfirm Buy back request number {selected_order.first_code} ")
        }


    else:
        message = messages.warning (request, "<p>you can not deconfirm this order because of following Errors:</p>"
                                             "<ol>"
                                             "<li>You do not access to this Warehouse</li>"
                                             "<li>Invoice can not Deconfirmed</li>"
                                             "</ol>")
        context = {
            "message": message
        }

    return redirect ("warehouse_confirm_buy_back")