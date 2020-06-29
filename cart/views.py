from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from Shop.models import Product
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from SCM.models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from UserControl.views import logIn
from UserControl.urls import *
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from accountside.filters import *
from accountside.models import *
from django.forms import formset_factory
from django.utils.safestring import mark_safe
import json
from Shop.views import product_off_step_finder
from decimal import *
from UserControl.models import *
from UserControl.decorators import *
from django.core.exceptions import PermissionDenied


def accesse_to_sell(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)
        orderkind_list = [item.name for item in access.orderkind.all ( )]
        print (orderkind_list)
        if "sell" in orderkind_list:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_access_warehouse(function):
    def wrap(request, id):

        order = Order.objects.get (id=id)
        user = request.user
        user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
        warhouse_list = [item.name for item in user_warehouse_access.warehouse.all ( )]
        if order.warhouse.name in warhouse_list:
            return function (request, id)
        else:
            raise PermissionDenied

    return wrap


@login_required (login_url='login')
@accesse_to_sell
def sell(request):
    user = request.user
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warhouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    access_to_visitor = AccsessTo.objects.get(user__user=user)
    access_to_visitor_list = [visitor for visitor in access_to_visitor.visitor.all() if "visitor" in [group.name for group in visitor.groups.all()]]

    if request.method == "POST":
        form = dict (request.POST)
        form.pop ('csrfmiddlewaretoken')

        selected_accountside_id = form['customer_id']
        selected_warehouse = form["warehouse"]
        form.pop ("warehouse")
        warhouse_model_select = WareHouseDefinde.objects.get (name=selected_warehouse[0])

        if form['visitor'][0] != "":
            visitor = User.objects.filter (id=(form['visitor'][0])).first ( )
            form.pop ('visitor')
        else:
            visitor = User.objects.filter (id=1).first ( )
            form.pop ('visitor')

        selected_accountside = accountside.objects.filter (id=selected_accountside_id[0]).first ( )
        form.pop ('customer_id')

        list_of_non_products = []
        for item in form.values ( ):
            product = Product.objects.filter (name=item[0]).first ( )
            inventory = get_object_or_404 (Inventory, warehouse=warhouse_model_select, product=product)
            quantity = int ((float (item[1]))) * product.box

            if inventory.sell_stock < quantity:
                list_of_non_products.append (product.name)
        if len (list_of_non_products) == 0:
            last_first_code = 0
            if Order.objects.filter (orderkinde_id=2).last ( ):
                last_find = Order.objects.filter (orderkinde_id=2).last ( )
                last_first_code = last_find.first_code

            order = Order.objects.create (creation_date=datetime.now ( ), user_craeter=user,
                                          accountside=selected_accountside, warhouse=warhouse_model_select,
                                          orderkinde=OrderKinde.objects.get (code=2), visitor=visitor,
                                          first_code=last_first_code + 1)
            for item in form.values ( ):
                product = Product.objects.filter (name=item[0]).first ( )
                inventory = get_object_or_404 (Inventory, warehouse=warhouse_model_select, product=product)
                quantity = int ((float (item[1]))) * product.box
                product_off = product.off
                product_off_id = product_off.id
                persentage = product_off_step_finder (product_off_id, int ((float (item[1]))) * product.box)

                OrderItem.objects.create (order=order,
                                          quantity=quantity,
                                          unit_price=product.price,
                                          product=product,
                                          vat=product.vat,
                                          off=persentage

                                          )

                inventory.sell_stock -= int ((float (item[1]))) * product.box
                inventory.save ( )
            return redirect ('modify_sell_view')
        else:
            for product in list_of_non_products:
                message = messages.warning (request, f"{product} is not available")

                context = {
                    'message': message
                }
    context = {
        "title": "New Sell Order",
        "warehouses": warhouse_list,
        "sell": 1,
        "visitors":access_to_visitor_list

    }

    return render (request, 'invoicing.html', context)


@login_required (login_url='login')
@can_make_shipment
def modify_sell_view(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    visitor_access = AccsessTo.objects.get(user__user_id=user.id)
    visitor_access_list = [visitor for visitor in visitor_access.visitor.all()]
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    order_set = Order.objects.filter (checked_out=False, warhouse_id__in=warehouse_list, orderkinde_id=2,visitor__in=visitor_access_list)
    modifyCart = OrderItem.objects.filter (order__checked_out=False, order__orderkinde_id=2)

    form = request.POST
    filter = order_filter (request.GET, queryset=modifyCart)
    modifyCart = filter.qs
    sotp = sum ([item.total_price for item in modifyCart])
    # paginator = Paginator (order_set,10 )
    # page= request.GET.get('page')
    # order_set=paginator.get_page(page)

    id_filtered = [id.id for id in order_set]
    dict0 = {}
    for id in id_filtered:
        si = OrderItem.objects.filter (order__id=id)
        dict0[id] = [sum ([i.total_price for i in si]), [i.product.name for i in si]]
    # Modify Recived Order and send for
    formToStr = dict (form)
    if len (formToStr) != 0:
        for item in formToStr:
            try:
                order = Order.objects.get (id=int (item))
                order.checked_out = True
                order.save ( )
            except:
                pass
        return redirect ('modify_sell_view')

    context = {
        "title": "Modify Sell Oder",
        'checkout': 'Confirm',
        'Title': 'Confirm Invoice',
        'modifyCart': modifyCart,
        'order_set': order_set,
        'd': dict0,
        'filter': filter,
        'sotp': sotp,

    }

    return render (request, 'modified.html', context)

@login_required (login_url='login')
@can_access_warehouse
@can_confirm_sell_order
def show_order_items(request, id):


    add_form = request.POST
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    access_to_visitor = AccsessTo.objects.get (user__user=user)
    access_to_visitor_list = [visitor for visitor in access_to_visitor.visitor.all ( ) if
                              "visitor" in [group.name for group in visitor.groups.all ( )]]

    tik = 1
    sell = 1

    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )

    warhouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    warhouse_list_name = [item.name for item in user_warehouse_access.warehouse.all ( )]
    order = Order.objects.filter (id=id).first ( )
    warehouse_in_order = order.warhouse.name

    edit_sell = 1

    selected_order_items = OrderItem.objects.filter (order_id=id)
    products_name_list = [item.product.name for item in selected_order_items]

    if request.method == "POST":
        if not order.shipment:

            form = dict (request.POST)
            new_warehouse = WareHouseDefinde.objects.get (name=form["warehouse"][0])
            visitor = User.objects.get (id=form["visitor"][0])
            print (visitor)
            form.pop ("visitor")
            form.pop ('warehouse')
            form.pop ('csrfmiddlewaretoken')
            if warehouse_in_order != new_warehouse.name:
                message = messages.warning (request, "You can not change Warehouse, Make new Order for New Warehouse")
                context = {
                    "message": message
                }

                return HttpResponseRedirect (reverse ('show_order_items', args=[id]))

            if 'customer_id' in [item for item in form.keys ( )]:
                suplier = form['customer_id']
                if suplier[0] != "":
                    suplier_in_accountside = accountside.objects.filter (id=suplier[0]).first ( )
                    order = Order.objects.filter (id=id).first ( )
                    order.accountside = suplier_in_accountside
                    order.save ( )

                form.pop ('customer_id')

                if visitor:
                    order.visitor = visitor
                    order.save ( )

                else:
                    order.visitor = User.objects.get (id=1)

                for item in form.values ( ):

                    product = Product.objects.filter (name=item[0]).first ( )
                    inventory = get_object_or_404 (Inventory, product=product, warehouse=new_warehouse)
                    product_box = product.box
                    box_quantity = float (item[1])
                    new_quantity = int (box_quantity) * product.box

                    if product.name in products_name_list:

                        product_name_index = products_name_list.index (product.name)
                        products_name_list.pop (product_name_index)

                        selected_order_item_product = OrderItem.objects.filter (order_id=id,
                                                                                product=product).first ( )
                        print (selected_order_item_product)
                        old_quantity = selected_order_item_product.quantity
                        difference_of_quantity = new_quantity - old_quantity
                        if new_quantity != old_quantity and int (inventory.sell_stock) + int (old_quantity) >= int (
                                new_quantity):

                            persentage = product_off_step_finder (product.off.id, int ((float (item[1]))) * product.box)
                            selected_order_item_product.quantity = new_quantity
                            selected_order_item_product.save ( )
                            selected_order_item_product.off = persentage
                            selected_order_item_product.save ( )

                            inventory.sell_stock += int (old_quantity) - int (new_quantity)
                            inventory.save ( )

                            message = messages.success (request, f"{product.name} was changed successfully from "
                                                                 f"<strang>{old_quantity / product.box}</strong> box to "
                                                                 f"<strang>{new_quantity / product.box}</strong> box")
                            context = {
                                'message': message
                            }
                        elif new_quantity != old_quantity and inventory.sell_stock < difference_of_quantity:
                            message = messages.warning (request,
                                                        f"avaialable quantity of {product.name} in {inventory.warehouse.name} "
                                                        f"is {inventory.sell_stock / product.box} box ")
                            context = {
                                "message": message
                            }


                    else:

                        if inventory.sell_stock >= new_quantity:
                            persentage = product_off_step_finder (product.off.id, int ((float (item[1]))) * product.box)
                            quantity = int (float (item[1]) * product_box)
                            OrderItem.objects.create (
                                order=Order.objects.get (id=id),
                                quantity=quantity,
                                unit_price=product.price,
                                product=product,
                                vat=product.vat,
                                off=persentage
                            )
                            inventory.sell_stock -= quantity
                            inventory.save ( )
                            message = messages.success (request, f"{product.name} was added successfully")
                            context = {
                                'message': message
                            }

                        else:
                            message = messages.warning (request,
                                                        f"{inventory.warehouse.name} has not available qunatity "
                                                        f"of {inventory.product.name}")

                            context = {
                                'message': message
                            }

                for product_name in products_name_list:
                    not_pop_product = Product.objects.filter (name=product_name).first ( )
                    inventory = get_object_or_404 (Inventory, product=not_pop_product, warehouse=new_warehouse)
                    not_pop_item = OrderItem.objects.filter (order_id=id, product=not_pop_product).first ( )

                    inventory.sell_stock += not_pop_item.quantity
                    inventory.save ( )
                    not_pop_item.delete ( )

                    message = messages.success (request, f"{not_pop_product.name} was deleted successfully")
                    context = {
                        'message': message
                    }

                return HttpResponseRedirect (reverse ('show_order_items', args=[id]))
        else:

            raise PermissionDenied

    context = {
        'order': order,
        'id': id,
        'warehouses': warhouse_list,
        "edit_sell": edit_sell,
        'cart': selected_order_items,
        'tik': 1,
        'order_id': id,
        'add_form': add_form,
        "sell": 1,
        "title": "Sell",
        "visitors": access_to_visitor_list

    }

    return render (request, 'invoicing.html', context)
@login_required (login_url='login')
@can_make_sell_order
def static_sell_veiw(request, id):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warhouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    warhouse_list_name = [item.name for item in user_warehouse_access.warehouse.all ( )]
    order = Order.objects.filter (id=id).first ( )
    items = OrderItem.objects.filter (order_id=id)

    context = {
        "items": items,
        "order": order,
        "kinde": order.orderkinde.name
    }

    return render (request, "staticView.html", context)
@login_required (login_url='login')
@can_make_sell_back
def new_sell_back_order(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    warehouse_list_name = [item.name for item in user_warehouse_access.warehouse.all ( )]
    form = dict (request.POST)
    if request.method == "POST":
        if form["product_name1"][1]:
            form.pop ("csrfmiddlewaretoken")
            costumer_id = form["customer_id"][0]
            selected_accountside = accountside.objects.get (id=costumer_id)
            form.pop ("customer_id")
            warehouse = form["warehouse"][0]
            warhouse_model_select = WareHouseDefinde.objects.filter (name=warehouse).first ( )
            if not warehouse in warehouse_list_name:
                return PermissionDenied
            form.pop ("warehouse")
            last_first_code = 0
            if Order.objects.filter (orderkinde_id=4).order_by("first_code").last ( ):
                last_find = Order.objects.filter (orderkinde_id=4).last ( )
                last_first_code = last_find.first_code
            sell_back_order = Order.objects.create (creation_date=datetime.now ( ), user_craeter=user,
                                              accountside=selected_accountside, warhouse=warhouse_model_select,
                                              orderkinde=OrderKinde.objects.get (code=4),
                                              first_code=last_first_code + 1)
            for item in form.values ( ):
                product = Product.objects.filter (name=item[0]).first ( )
                inventory = Inventory.objects.filter (product=product, warehouse=WareHouseDefinde.objects.filter (
                    name=warehouse).first ( )).first ( )
                product_box = product.box
                quantity = int (float (item[1]) * product_box)
                price = float (item[2])
                off = float (item[3])
                vat = float (item[4])
                OrderItem.objects.create (
                    order=sell_back_order,
                    vat=vat,
                    off=off,
                    product=product,
                    quantity=quantity,
                    unit_price=price,
                )
        else:
            context = {
                "message": messages.warning (request, "Worng Entery")
            }

    context = {
        "title": "New Sell Back",
        "buy": 1,
        "warehouses": warehouse_list,
    }
    return render (request, "invoicing.html", context)
@login_required (login_url='login')
@can_make_sell_back
def show_sell_back_orders(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    orders = Order.objects.filter (warhouse_id__in=warehouse_list, orderkinde_id=4,checked_out_2=False)
    if request.method == "POST":
        form = dict (request.POST)
        form.pop ("csrfmiddlewaretoken")
        for key in form.keys ( ):
            order = Order.objects.get (id=key)
            if order.checked_out != True:
                order.delete ( )
            else:
                context = {
                    "message": messages.warning (request, f"for deleting sell-back order number {order.first_code} "
                                                          f"warehous should deconfirm "
                                                          f"that ")
                }

    context = {
        "title": "views Sell-Back Orders",
        "orders": orders
    }

    return render (request, "buyorder.html", context)

@login_required (login_url='login')
@can_make_buy_order
def new_buy_order(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    warehouse_list_name = [item.name for item in user_warehouse_access.warehouse.all ( )]
    form = dict (request.POST)
    if request.method == "POST":
        if form["product_name1"][1]:
            form.pop ("csrfmiddlewaretoken")
            costumer_id = form["customer_id"][0]
            selected_accountside = accountside.objects.get (id=costumer_id)
            form.pop ("customer_id")
            warehouse = form["warehouse"][0]
            warhouse_model_select = WareHouseDefinde.objects.filter (name=warehouse).first ( )
            if not warehouse in warehouse_list_name:
                return PermissionDenied
            form.pop ("warehouse")
            last_first_code = 0
            if Order.objects.filter (orderkinde_id=1).last ( ):
                last_find = Order.objects.filter (orderkinde_id=1).last ( )
                last_first_code = last_find.first_code
            buy_order = Order.objects.create (creation_date=datetime.now ( ), user_craeter=user,
                                              accountside=selected_accountside, warhouse=warhouse_model_select,
                                              orderkinde=OrderKinde.objects.get (code=1),
                                              first_code=last_first_code + 1)
            for item in form.values ( ):
                product = Product.objects.filter (name=item[0]).first ( )
                inventory = Inventory.objects.filter (product=product, warehouse=WareHouseDefinde.objects.filter (
                    name=warehouse).first ( )).first ( )
                product_box = product.box
                quantity = int (float (item[1]) * product_box)
                price = float (item[2])
                off = float (item[3])
                vat = float (item[4])
                OrderItem.objects.create (
                    order=buy_order,
                    vat=vat,
                    off=off,
                    product=product,
                    quantity=quantity,
                    unit_price=price,
                )
        else:
            context = {
                "message": messages.warning (request, "Worng Entery")
            }

    context = {
        "title": "New Buy Order",
        "buy": 1,
        "warehouses": warehouse_list,
    }
    return render (request, "invoicing.html", context)



@login_required (login_url='login')
@can_show_buy_orders
def show_buy_orders(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    orders = Order.objects.filter (warhouse_id__in=warehouse_list, orderkinde_id=1,checked_out_2=False)
    if request.method == "POST":
        form = dict (request.POST)
        form.pop ("csrfmiddlewaretoken")
        for key in form.keys ( ):
            order = Order.objects.get (id=key)
            if order.checked_out != True:
                order.delete ( )
            else:
                context = {
                    "message": messages.warning (request, f"for deleting order number {order.first_code} "
                                                          f"warehous should deconfirm "
                                                          f"that ")
                }

    context = {
        "title": "views Buy Orders",
        "orders": orders
    }

    return render (request, "buyorder.html", context)


@can_access_warehouse
@login_required (login_url='login')
@can_show_buy_orders
def show_buy_order_items(request, id):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    warehouse_list_name = [item.name for item in user_warehouse_access.warehouse.all ( )]
    order = Order.objects.get (id=id)
    orde_items = OrderItem.objects.filter (order=order)
    products_list_name = [item.product.name for item in orde_items]
    print (products_list_name)

    if request.method == "POST":
        if order.checked_out:
            context = {
                "message": messages.warning (request, "for editing order deconfirm it"),
            }
            return HttpResponseRedirect (reverse ("show_buy_order_items", args=[id]))
        else:
            form = dict (request.POST)
            form.pop ("csrfmiddlewaretoken")
            costumer_id = form["customer_id"][0]
            selected_accountside = accountside.objects.get (id=costumer_id)
            order.accountside = selected_accountside
            order.save ( )
            form.pop ("customer_id")
            new_warehouse = form["warehouse"][0]
            form.pop ("warehouse")
            print (form)
            if new_warehouse != order.warhouse.name:
                context = {
                    "message": messages.warning (request, "Changing warehouse is not possible"),
                }
                return HttpResponseRedirect (reverse ("show_buy_order_items", args=[id]))

            if not new_warehouse in warehouse_list_name:
                return PermissionDenied
            for item in form.values ( ):
                if item[0] in products_list_name:
                    product = Product.objects.filter (name=item[0]).first ( )
                    order_item = OrderItem.objects.filter (product=product, order=order).first ( )
                    product_box = product.box
                    quantity = int (float (item[1]) * product_box)
                    price = float (item[2])
                    off = float (item[3])
                    vat = float (item[4])
                    order_item.vat = vat
                    order_item.save ( )
                    order_item.quantity = quantity
                    order_item.save ( )
                    order_item.price = price
                    order_item.save ( )
                    order_item.off = off
                    order_item.save ( )
                    index_of_product = products_list_name.index (item[0])
                    products_list_name.pop (index_of_product)

                else:
                    product = Product.objects.filter (name=item[0]).first ( )

                    product_box = product.box
                    quantity = int (float (item[1]) * product_box)
                    price = float (item[2])
                    off = float (item[3])
                    vat = float (item[4])
                    OrderItem.objects.create (
                        order=order,
                        vat=vat,
                        off=off,
                        product=product,
                        quantity=quantity,
                        unit_price=price,
                    )
                    context = {
                        "message": messages.success (request,
                                                     f"{item[1]} box of {product.name} added to order {order.first_code}")
                    }
        if len (products_list_name) > 0:
            for product in products_list_name:
                product = Product.objects.filter (name=product).first ( )
                order_item = OrderItem.objects.filter (product=product, order=order).first ( )
                order_item.delete ( )
                context = {
                    "message": messages.info (request,
                                              f"{order_item.quantity / product.box} box of {product.name} deleted from "
                                              f"order number {order.first_code}")
                }
        return HttpResponseRedirect (reverse ("show_buy_order_items", args=[id]))

    context = {
        "buy": 1,
        "cart": orde_items,
        "tik": 1,
        "order": order,
        "warehouses": warehouse_list

    }

    return render (request, "invoicing.html", context)

@login_required (login_url='login')
@can_make_buy_back
def buy_back(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    warehouse_list_name = [item.name for item in user_warehouse_access.warehouse.all ( )]
    form = dict (request.POST)
    if request.method == "POST":
        if form["product_name1"][1]:
            form.pop ("csrfmiddlewaretoken")
            costumer_id = form["customer_id"][0]
            selected_accountside = accountside.objects.get (id=costumer_id)
            form.pop ("customer_id")
            warehouse = form["warehouse"][0]
            warhouse_model_select = WareHouseDefinde.objects.filter (name=warehouse).first ( )
            if not warehouse in warehouse_list_name:
                return PermissionDenied
            form.pop ("warehouse")
            blank_list = []
            for item in form.values ( ):
                product = Product.objects.filter (name=item[0]).first ( )
                product_box = product.box
                quantity = int (float (item[1]) * product_box)

                if Inventory.objects.filter (product=product, warehouse=warhouse_model_select):
                    inventory = Inventory.objects.filter (product=product, warehouse=warhouse_model_select).first ( )
                    sell_stock = inventory.sell_stock
                    if quantity > sell_stock:
                        blank_list.append (product.name)
            if len (blank_list) != 0:
                for item in blank_list:
                    context = {
                        "message": messages.warning (request, f"{item} is not available in Warehouse")
                    }
                return redirect ("buy_back")

            last_first_code = 0
            if Order.objects.filter (orderkinde_id=3).last ( ):
                last_find = Order.objects.filter (orderkinde_id=3).last ( )
                last_first_code = last_find.first_code
            buy_order = Order.objects.create (creation_date=datetime.now ( ), user_craeter=user,
                                              accountside=selected_accountside, warhouse=warhouse_model_select,
                                              orderkinde=OrderKinde.objects.get (code=3),
                                              first_code=last_first_code + 1)
            for item in form.values ( ):
                product = Product.objects.filter (name=item[0]).first ( )

                product_box = product.box
                quantity = int (float (item[1]) * product_box)
                price = float (item[2])
                off = float (item[3])
                vat = float (item[4])
                OrderItem.objects.create (
                    order=buy_order,
                    vat=vat,
                    off=off,
                    product=product,
                    quantity=quantity,
                    unit_price=price,
                )
        else:
            context = {
                "message": messages.warning (request, "Worng Entery")
            }

    context = {
        "title": "New Buy Back",
        "buy": 1,
        "warehouses": warehouse_list,
    }
    return render (request, "invoicing.html", context)


def remove_order(request, order_id):
    order = Order.objects.get (id=order_id)
    items = OrderItem.objects.filter (order_id=order_id)
    for item in items:
        quantity = item.quantity
        inventory = get_object_or_404 (Inventory, product=item.product, warehouse=order.warhouse)
        inventory.sell_stock += quantity
        inventory.save ( )

    order.delete ( )
    message = messages.success (request, f"Order number {order.first_code} was removed successfully")
    context = {
        "message": message
    }

    return redirect ('modify_sell_view')
@login_required (login_url='login')
@can_confirm_sell_order
def send_for_scm(request, order_id):
    form = SendToWarehouseForm (request.POST or None)

    if request.POST and form.is_valid ( ):
        cd = form.cleaned_data
        order_item = Order.objects.filter (id=order_id)
        print (order_id)
        # order_item.checked_out=cd['select_for_scm']
        # order_item.save()
        # print(cd['select_for_scm'])
        # user=get_user_model()
        # ComeForDelivery.objects.create(
        #      order_number = order_item,
        #      user_modifier = user,
        #      )
    return redirect ('modify_cart_view')
@login_required (login_url='login')
@can_show_buy_back
def show_buy_back(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    orders = Order.objects.filter (warhouse_id__in=warehouse_list, orderkinde_id=3)
    if request.method == "POST":
        form = dict (request.POST)
        form.pop ("csrfmiddlewaretoken")

        for key in form.keys ( ):
            order = Order.objects.get (id=key)
            if order.checked_out != True:
                order.delete ( )
            else:
                context = {
                    "message": messages.warning (request, f"for deleting buy order number {order.first_code} "
                                                          f"warehous should deconfirm "
                                                          f"that ")
                }

    context = {
        "title": "Views Buy Back",
        "orders": orders
    }

    return render (request, "buyorder.html", context)


from UserControl.forms import Disrobuter

@login_required (login_url='login')
@can_make_shipment
def make_shipment(request):
    form = Disrobuter
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item for item in user_warehouse_access.warehouse.all ( )]
    warehouse_list_name = [item.name for item in user_warehouse_access.warehouse.all ( )]
    order_set = Order.objects.filter (checked_out=True, warhouse_id__in=warehouse_list,
                                      orderkinde_id=2, shipment=None)
    modifyCart = OrderItem.objects.filter (order__checked_out=True, order__orderkinde_id=2)
    all_shipment = Shipment.objects.filter (checked_out=False)

    shipment = dict (request.POST)
    blank_list = []
    blank_set = set (blank_list)

    if request.method == "POST" and shipment["Add"][0]:


        shipment.pop ("csrfmiddlewaretoken")
        for item in shipment["sid"]:
            if item:

                oid = item[0:item.find("t")]
                sid = item[item.find("t")+1:item.find("s")]
                add_order_to_shipment(request,int(oid),int(sid))




        return redirect ("make_shipment")

    if request.method == "POST":
        print (shipment)
        shipment.pop ("csrfmiddlewaretoken")
        shipment.pop ("Add")
        if "sid" in shipment.keys():
            shipment.pop ("sid")
        distrobuter = User.objects.get (id=shipment["Distrobuter"][0])
        shipment.pop ("Distrobuter")
        if len (shipment) > 0:
            print (shipment)
            for key in shipment.keys ( ):

                selected_order = Order.objects.get (id=key)
                print (selected_order.first_code)
                warehouse = selected_order.warhouse
                blank_set.add (warehouse.id)
                if not warehouse.name in warehouse_list_name:
                    context = {
                        "message": messages.warning (request, "You Do not Access To This Warehouse."
                                                              "<p>Task sended for administartor</p>")
                    }

        if int (len (blank_set)) == 1:
            warehouse = WareHouseDefinde.objects.get (id=list (blank_set)[0])
            last_shipmnet = Shipment.objects.filter ( ).order_by ("code").last ( )
            new_shipment_code = 1
            if last_shipmnet == None:
                new_shipment_code = 1
            else:
                new_shipment_code += last_shipmnet.code
            new_shipment = Shipment.objects.create (creation_date=datetime.now ( ), user_craeter=user,
                                                    code=int (new_shipment_code), distributeur=distrobuter,
                                                    warehouse=warehouse)

            added = 0
            for key in shipment.keys ( ):

                selected_order = Order.objects.get (id=int (key))
                if selected_order.orderkinde.id == 2:
                    selected_order.shipment = new_shipment
                    selected_order.save ( )
                    added += 1
                else:
                    context = {
                        "message": messages.warning (request, f"{selected_order.orderkinde} can not add to shipment ")
                    }
            if added == 1:
                message = messages.success (request,
                                            f'you have created successfully your'
                                            f' shipment with number{new_shipment.code} with {added} orders')
                context = {
                    'message': message
                }
            if added > 1:
                message = messages.success (request,
                                            f'<h5>you have created successfully your'
                                            f' shipment with number{new_shipment.id} with {added} orders</h5>')
                context = {
                    'message': message
                }

        else:
            context = {
                "message": messages.warning (request, "<p>ERROR</p>"
                                                      "<p>1 - You can not make shipment for diffrent Warehouses</p>"
                                                      "<p>2 - You did not select any order</p>")
            }
    context = {
        "form": form,
        "title": "Make shipment",
        'checkout': 'Make Shipment',
        'modifyCart': modifyCart,
        'order_set': order_set,
        "shipments": all_shipment

    }

    return render (request, 'modified.html', context)

@login_required (login_url='login')
@can_show_shipment_orders
def show_shipment_orders(request, id):
    selected_shipment = Shipment.objects.get (id=id)
    user = request.user
    access = AccsessTo.objects.filter (user__user=user).first ( )
    user_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_access.warehouse.all ( )]
    context = {
        "access": access,
        "Title": f"Shipment {selected_shipment.code}",
        "shipment": selected_shipment
    }

    if selected_shipment.warehouse.id in warehouse_list:
        if access.user.all_shipment_view or selected_shipment.distributeur == user:

            shipment_orders = Order.objects.filter (shipment_id=id, orderkinde__code=2).order_by ("row")
            context["orders"] = shipment_orders

            if request.method == "POST":
                form = request.POST

            return render (request, "showShiomentOrders.html", context)

        else:
            raise PermissionDenied

    else:
        raise PermissionDenied
@login_required (login_url='login')
@can_edit_shipment
def edit_shipment(request, id):
    user = request.user

    delivery = User.objects.filter (groups=2)
    access = AccsessTo.objects.filter (user__user=user).first ( )
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    selected_shipment = Shipment.objects.get (id=id)
    order_in_shipment = Order.objects.filter (shipment_id=id)
    if selected_shipment.warehouse.id in warehouse_list and selected_shipment.checked_out == False:
        shipment_orders = Order.objects.filter (shipment_id=id, orderkinde__code=2).order_by ("row")

        if request.method == "POST":
            form = dict (request.POST)
            form.pop ("csrfmiddlewaretoken")

            deliver = User.objects.get (id=int (form["deliver"][0]))
            descript = form["descript"][0]
            form.pop ("deliver")
            form.pop ("descript")
            selected_shipment.distributeur = deliver
            selected_shipment.save ( )
            selected_shipment.description = descript
            selected_shipment.save ( )
            if "order" in form:
                if len (form["order"]) < len (order_in_shipment):
                    for order_id in form["order"]:
                        order = Order.objects.get (id=int (order_id))
                        order.shipment = None
                        order.save ( )
                else:
                    context = {
                        "message": messages.warning (request, "<h5>you can not make blank shipment</h5>")
                    }
            return HttpResponseRedirect (reverse ("edit_shipment", args=[id, ]))

        context = {
            "orders": shipment_orders,
            "access": access,
            "Title": f"Shipment {selected_shipment.code}",
            "shipment": selected_shipment,
            "edit": 1,
            "delivery": delivery, }

        return render (request, "showShiomentOrders.html", context)

    else:
        raise PermissionDenied

@login_required (login_url='login')
@can_edit_shipment
def add_order_to_shipment(request, oid, sid):
    shipment = Shipment.objects.get (id=sid)
    order = Order.objects.get (id=oid)
    if shipment.warehouse == order.warhouse:

        if not shipment.checked_out:
            order.shipment = shipment
            order.save ( )
            context = {
                "message": messages.info (request, f"<h5>You have Successfully added order"
                                                   f" {order.first_code} to shipment"
                                                   f" {shipment.code}</h5>"
                                                   f"<h5>Make Shipment and Add to Shipment are not working In One Poste</h5>")
            }
        else:
            context = {
                "message": messages.warning (request, f"shipment <h4>{shipment.code}</h4> is on process")
            }
    else:
        context = {
            "message": messages.warning (request, f"Different Warhouses")
        }

@login_required (login_url='login')
@can_deliver_confirm_shipment
def delivery_function_on_order_items(request, id):
    user = request.user
    order = Order.objects.get (id=id)
    if order.shipment.checked_out_3 == False:
        cart = OrderItem.objects.filter (order=order)
        backed = Order.objects.filter (shipment=order.shipment, orderkinde__code=6).first ( )
        order_product_names = [item.product.name for item in cart]

        if request.method == "POST":

            form = dict (request.POST)
            form.pop ("csrfmiddlewaretoken")
            if "return_all" in form:
                if backed is None:
                    last_back_order = Order.objects.last ( )
                    first_code = 1
                    if last_back_order.first_code:
                        first_code += int (last_back_order.first_code)

                    new_order = Order.objects.create (
                        first_code=first_code,
                        user_craeter=f'{user.first_name} {user.last_name}',
                        accountside=order.accountside,
                        shipment=order.shipment,
                        warhouse=order.warhouse,
                        orderkinde=OrderKinde.objects.filter (code=6).first ( ),
                        visitor=user,
                        orderid=id,
                    )
                    for item in cart:
                        OrderItem.objects.create (
                            order=new_order,
                            quantity=item.quantity,
                            unit_price=item.unit_price,
                            product=item.product,
                            vat=item.product.vat,
                            off=item.off
                        )
                        item.quantity = 0
                        item.save ( )
                else:
                    for item in cart:
                        if OrderItem.objects.filter (order=backed, product=item.product):
                            existance = OrderItem.objects.filter (order=backed, product=item.product).first ( )
                            existance.quantity += item.quantity
                            existance.save ( )


                        else:

                            OrderItem.objects.create (
                                order=backed,
                                quantity=item.quantity,
                                unit_price=item.product.price,
                                product=item.product,
                                vat=item.product.vat,
                                off=0
                            )
                        item.quantity = 0
                        item.save ( )
                return HttpResponseRedirect (reverse ("delivery_function_on_order_items", args=[id, ]))

            elif "customer_id" in form:
                form.pop ("customer_id")

                for item in form.values ( ):
                    product = Product.objects.filter (name=item[0]).first ( )
                    new_quantity = float (item[1]) * product.box
                    product_off = product.off
                    product_off_id = product_off.id
                    new_off = product_off_step_finder (product_off.id, int (new_quantity))
                    if product.name in order_product_names:

                        index = order_product_names.index (product.name)
                        order_product_names.pop (index)
                        selected_item = cart.get (product=product)
                        old_quantity = selected_item.quantity
                        old_off = selected_item.off
                        if new_quantity < old_quantity:
                            if backed:
                                if OrderItem.objects.filter (order=backed, product=product):
                                    existance = OrderItem.objects.filter (order=backed, product=product).first ( )
                                    existance.quantity += old_quantity - new_quantity
                                    existance.save ( )

                                else:

                                    OrderItem.objects.create (
                                        order=backed,
                                        quantity=old_quantity - new_quantity,
                                        unit_price=product.price,
                                        product=product,
                                        vat=product.vat,
                                        off=0
                                    )

                            else:
                                last_back_order = Order.objects.last ( )
                                first_code = 1
                                if last_back_order.first_code:
                                    first_code += int (last_back_order.first_code)

                                new_order = Order.objects.create (
                                    first_code=first_code,
                                    user_craeter=f'{user.first_name} {user.last_name}',
                                    accountside=order.accountside,
                                    shipment=order.shipment,
                                    warhouse=order.warhouse,
                                    orderkinde=OrderKinde.objects.filter (code=6).first ( ),
                                    visitor=order.visitor,
                                    orderid=id,
                                )
                                OrderItem.objects.create (
                                    order=new_order,
                                    quantity=old_quantity - new_quantity,
                                    unit_price=product.price,
                                    product=product,
                                    vat=product.vat,
                                    off=new_off
                                )

                            selected_item.quantity = new_quantity
                            selected_item.save ( )
                            selected_item.off = new_off
                            selected_item.save ( )
                        elif new_quantity > old_quantity:
                            if backed:
                                if OrderItem.objects.filter (order=backed, product=product):
                                    raiser_item = OrderItem.objects.filter (order=backed, product=product).first ( )
                                    if raiser_item.quantity >= new_quantity - old_quantity:
                                        raiser_item.quantity -= new_quantity - old_quantity
                                        raiser_item.save ( )
                                        if raiser_item.quantity == 0:
                                            raiser_item.delete ( )

                                        selected_item.quantity = new_quantity
                                        selected_item.save ( )
                                        selected_item.off = new_off
                                        selected_item.save ( )

                            else:
                                context = {
                                    "message": messages.warning (request, "this item is not in your little warehouse")
                                }

                    else:
                        if backed and OrderItem.objects.filter (order=backed, product=product):
                            raiser_item = OrderItem.objects.filter (order=backed, product=product).first ( )
                            if raiser_item.quantity >= new_quantity:
                                OrderItem.objects.create (
                                    order=order,
                                    quantity=new_quantity,
                                    unit_price=product.price,
                                    product=product,
                                    vat=product.vat,
                                    off=new_off
                                )
                                raiser_item.quantity -= new_quantity
                                raiser_item.save ( )
                                if raiser_item.quantity == 0:
                                    raiser_item.delete ( )
                                if order.total_box == 0:
                                    order.delete ( )
                            else:
                                context = {
                                    "message": messages.warning (request, f"NO {product.name} avaiable  ")
                                }

                        else:
                            context = {
                                "message": messages.warning (request, f"NO {product.name} avaiable  ")
                            }

            for name in order_product_names:
                item_pop = cart.get (product__name=name)

                product = Product.objects.filter (name=name).first ( )
                if backed:
                    if OrderItem.objects.filter (order=backed, product=product):
                        existance = OrderItem.objects.filter (order=backed, product=product).first ( )
                        existance.quantity += item_pop.quantity
                        existance.save ( )

                    else:

                        OrderItem.objects.create (
                            order=backed,
                            quantity=item_pop.quantity,
                            unit_price=product.price,
                            product=product,
                            vat=product.vat,
                            off=0
                        )
                else:
                    last_back_order = Order.objects.last ( )
                    first_code = 1
                    if last_back_order.first_code:
                        first_code += int (last_back_order.first_code)

                    new_order = Order.objects.create (
                        first_code=first_code,
                        user_craeter=f'{user.first_name} {user.last_name}',
                        accountside=order.accountside,
                        shipment=order.shipment,
                        warhouse=order.warhouse,
                        orderkinde=OrderKinde.objects.filter (code=6).first ( ),
                        visitor=order.visitor,
                        orderid=id,
                    )
                    OrderItem.objects.create (
                        order=new_order,
                        quantity=item_pop.quantity,
                        unit_price=product.price,
                        product=product,
                        vat=product.vat,
                        off=0)
                item_pop.delete ( )
            return HttpResponseRedirect (reverse ("delivery_function_on_order_items", args=[id, ]))

        context = {
            "tik": 1,
            "delivery": 1,
            "sell": 1,
            "cart": cart,
            "order": order,
            "backed": backed

        }

        return render (request, "invoicing.html", context)
    else:
        raise PermissionDenied

@login_required (login_url='login')
@can_settel_order
def settle_order(request, id):
    user = request.user
    order = Order.objects.get (id=id)
    settles = settlement.objects.all ( )
    access = Access.objects.filter (user=user).first ( )
    banks = BankCheck.objects.all ( )

    reciveds = delivery_settlment.objects.filter (sell_order=order)
    settles = settlement.objects.all ( )

    if order.orderkinde.id == 2 and order.shipment.checked_out_3 == False\
            or order.orderkinde.id == 2 and access.accounting_after_return == True or \
            order.orderkinde.id == 1 and access.make_pay_order == True :

        if request.method == "POST":
            form = dict (request.POST)
            form.pop ("csrfmiddlewaretoken")

            if "delete" in form.keys ( ):
                try:
                    for item in form["revice_id"]:
                        selected = delivery_settlment.objects.get (id=item)
                        if selected.check_out_1 == False:
                            selected.delete ( )
                        else:
                            context = {
                                "message":messages.warning(request,"This settlment was confirmed !!")
                            }

                except:
                    context = {
                        "message": messages.warning (request, "No Settle For Delete")
                    }

            elif len (form) == 1:
                delivery_settlment.objects.create (
                    sell_order=order,
                    amount=form["amount1"][0],
                    settel_kinde=settlement.objects.get (id=1),
                    user=user
                )





            elif len (form) == 4 and "bank_pose" in form:
                delivery_settlment.objects.create (
                    sell_order=order,
                    amount=form["amount1"][0],
                    now_date=form["date"][0],
                    settel_kinde=settlement.objects.get (id=2),
                    bank_pose=BankPose.objects.get (id=form["bank_pose"][0]),
                    serial_num=form["serial"][0],
                    user=user
                )
            elif len (form) == 4 and "usance_date" in form :
                if order.orderkinde == 2:
                    delivery_settlment.objects.create (
                        sell_order=order,
                        amount=form["amount1"][0],
                        settel_kinde=settlement.objects.get (id=3),
                        bank=BankCheck.objects.get (id=form["bank"][0]),
                        serial_num=form["serial"][0],
                        usance_date=form["usance_date"][0],
                        user=user
                    )
                elif  order.orderkinde == 1:
                    delivery_settlment.objects.create (
                        sell_order=order,
                        amount=form["amount1"][0],
                        settel_kinde=settlement.objects.get (id=3),
                        bank_pose=BankPose.objects.get (id=form["bank_pose"][0]),
                        serial_num=form["serial"][0],
                        usance_date=form["usance_date"][0],
                        user=user
                    )

        context = {
            "order": order,
            "settles": settles,
            "access": access,
            "banks": banks,
            "reciveds": reciveds,

        }

        return render (request, "orderSettlment.html", context)
    else:
        raise PermissionDenied




def date_to(request):
    blank = []

    orders = Order.objects.filter (checked_out_2=True,orderkinde__code= 1)
    for order in orders:
        print(order.id)
        journal = OrderJournalRelation.objects.filter (order=order).first ( )
        date = journal.document_number.creation_date
        order.data_convert_invoice = date
        order.save()
        blank.append (order.id)


    return redirect ('index')
