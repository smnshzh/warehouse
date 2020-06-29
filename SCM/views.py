from django.shortcuts import render, redirect
from cart.forms import *
from django.core.paginator import Paginator
from cart.forms import *
from cart.filters import *
from cart.models import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datetime import datetime
from django.contrib import messages
from UserControl.models import Access
from UserControl.forms import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from UserControl.decorators import *

@login_required (login_url='login')
def shipment_overall(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    all_shipment = Shipment.objects.filter (warehouse_id__in=warehouse_list)
    access = AccsessTo.objects.all ( )

    if request.method == "POST":
        form = dict (request.POST)
        form.pop ('csrfmiddlewaretoken')
        for key in form.keys ( ):
            selected_shipment = Shipment.objects.get (id=key)
            if selected_shipment.warehouse.id in warehouse_list:
                if selected_shipment.checked_out == False:
                    selected_shipment.delete ( )
                elif selected_shipment.checked_out == True and selected_shipment.checked_out_2 == False:
                    context = {
                        "message": f"shipment Number {selected_shipment.code} is processed by Warehouse"
                                   f"For deleting Warhouse must return it"
                    }
                elif selected_shipment.checked_out == True and selected_shipment.checked_out_2 == False:
                    context = {
                        "message": f"shipment Number {selected_shipment.code} is sended"
                                   f"deleting is impossible"
                    }
            else:
                return PermissionError

    form = Disrobuter
    context = {
        'all_shipment': all_shipment,
        "form": form,
        "overall": 1
    }

    return render (request, 'manageShipments.html', context)

@login_required (login_url='login')
@can_recieve_and_send_shipments
def recieve_and_send_shipments(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    all_shipment = Shipment.objects.filter (warehouse_id__in=warehouse_list, checked_out_2=False)
    shipment_back = Shipment.objects.filter (warehouse_id__in=warehouse_list, checked_out_2=True)

    if request.method == "POST":

        form = dict (request.POST)
        for key in form.keys ( ):
            selected_shipment = Shipment.objects.get (id=key)
            warehouse = selected_shipment.warehouse
            if selected_shipment.checked_out == False and user_warehouse_access.recieve_shipments:
                selected_shipment.checked_out = True
                selected_shipment.save ( )
                return redirect ("recieve_and_send_shipments")
            if selected_shipment.checked_out == True and selected_shipment.checked_out_2 == False and user_warehouse_access.send_shipments:

                items = OrderItem.objects.filter (order__shipment_id=key)

                for item in items:
                    OrderItemBackup.objects.create (
                        order=item.order,
                        vat=item.vat,
                        off=item.off,
                        product=item.product,
                        quantity=item.quantity,
                        unit_price=item.unit_price
                    )
                    inventory = Inventory.objects.filter (product=item.product, warehouse=warehouse).first ( )
                    quantity = item.quantity
                    inventory.stock -= quantity
                    inventory.save ( )

                selected_shipment.checked_out_2 = True
                selected_shipment.save ( )
                return redirect ("recieve_and_send_shipments")

    context = {
        'warehouse': 1,
        "all_shipment": all_shipment,
        "shipment_back": shipment_back,
        "RS": 1
    }

    return render (request, 'manageShipments.html', context)

@login_required (login_url='login')
@can_cancle_sending
def cancle_sending(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    all_shipment = Shipment.objects.filter (warehouse_id__in=warehouse_list, checked_out_2=True)

    if request.method == "POST":

        form = dict (request.POST)
        for key in form.keys ( ):
            selected_shipment = Shipment.objects.get (id=key)
            warehouse = selected_shipment.warehouse
            if selected_shipment.checked_out == True and selected_shipment.checked_out_2 == True:
                if selected_shipment.checked_out_3 == False:

                    items = OrderItem.objects.filter (order__shipment_id=key)
                    if not Order.objects.filter (shipment=selected_shipment, orderkinde=6):

                        for item in items:
                            back_up = OrderItemBackup.objects.filter (order=item.order, product=item.product).first ( )
                            back_up.delete ( )
                            inventory = Inventory.objects.filter (product=item.product, warehouse=warehouse).first ( )
                            quantity = item.quantity
                            inventory.stock += quantity
                            inventory.save ( )

                        selected_shipment.checked_out_2 = False
                        selected_shipment.save ( )
                    else:
                        context = {
                            "message": messages.warning (request,
                                                         f"Return Object exist for shipment{selected_shipment.code}")
                        }
                else:
                    context = {
                        "message": messages.warning (request,
                                                     f"Return Object exist for shipment{selected_shipment.code}")
                    }

                return redirect ("cancle_sending")

    context = {
        'warehouse': 1,
        "all_shipment": all_shipment,
        "sended": 1

    }

    return render (request, 'manageShipments.html', context)
@login_required (login_url='login')
@can_view_shipment_items
def shipment_items(request, id):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    all_shipment = Shipment.objects.filter (warehouse_id__in=warehouse_list, checked_out_2=False)
    access = AccsessTo.objects.get (user__user=user)

    shipment = Shipment.objects.get (id=id)

    items = OrderItem.objects.filter (order__shipment_id=id)
    blanck_dict = {}

    if shipment.distributeur == user or access.user.all_shipment_view:

        if shipment.warehouse.id in warehouse_list:

            for item in items:

                if item.product.name in blanck_dict:
                    blanck_dict[item.product] += int (item.quantity)
                else:
                    blanck_dict[item.product] = int (item.quantity)
        else:
            raise Http404
    else:
        raise PermissionDenied

    context = {
        "items": shipment.shipment_items,
        "shipment": shipment,
        "kind": "Shipment",
        "access": access,
    }

    return render (request, "shipmentItems.html", context)
@login_required (login_url='login')
@can_view_shipment_items_backed
def print_shipment_items_back(request, id):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    all_shipment = Shipment.objects.filter (warehouse_id__in=warehouse_list, checked_out_2=True)

    shipment = Shipment.objects.get (id=id)

    items = OrderItem.objects.filter (order__shipment_id=id, order__orderkinde_id=6)
    blanck_dict = {}

    if shipment.warehouse.id in warehouse_list:
        if shipment.checked_out_2 == True:

            for item in items:

                if item.product.name in blanck_dict:
                    blanck_dict[item.product] += int (item.quantity)
                else:
                    blanck_dict[item.product] = int (item.quantity)

        else:
            context = {
                "message": messages.info (request,
                                          f"Delivery is not complete,<strong>{shipment.distributeur.first_name}"
                                          f" {shipment.distributeur.last_name}</strong> did not confirm End of"
                                          f"distribution {shipment.code} ")
            }
            # return redirect("shipment_overall")

    else:
        raise Http404

    context = {
        "items": blanck_dict,
        "shipment": shipment,
        "kind": "Return of Shipment"

    }

    return render (request, "shipmentItems.html", context)
@login_required (login_url='login')
@can_confirm_shipment_items_backed
def confirm_shipment_items_back(request, id):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    all_shipment = Shipment.objects.filter (warehouse_id__in=warehouse_list, checked_out_2=True)

    shipment = Shipment.objects.get (id=id)

    items = OrderItem.objects.filter (order__shipment_id=id, order__orderkinde_id=6)

    blanck_dict = {}

    if shipment.checked_out_2 == True and shipment.checked_out_3 == True:

        if shipment.warehouse.id in warehouse_list:

            for item in items:

                if item.product.name in blanck_dict:
                    blanck_dict[item.product]["box"] += int (item.quantity / item.product.box)
                    blanck_dict[item.product]['small'] += int (item.quantity % item.product.box)
                    blanck_dict[item.product]['total'] += int (item.quantity)
                else:
                    blanck_dict[item.product] = {'box': int (item.quantity / item.product.box),
                                                 'small': int (item.quantity % item.product.box),
                                                 'total': int (item.quantity)}

        else:
            raise PermissionDenied

        if request.method == "POST":

            for item in items:
                warehouse = shipment.warehouse
                inventory = Inventory.objects.get (product=item.product, warehouse=warehouse)
                inventory.stock += item.quantity
                inventory.save ( )
                inventory.sell_stock += item.quantity
                inventory.save ( )
            shipment.checked_out_4 = True
            shipment.save ( )
            first_item = items.first ( )
            order = first_item.order
            order.checked_out_2 = True
            order.save ( )
            order.user_craeter = f"{user.username}"
            order.save ( )


    else:
        context = {
            "message": messages.info (request, f"Delivery is not complete,{shipment.distributeur.first_name}"
                                               f"{shipment.distributeur.last_name} did not confirm End of"
                                               f"distributions ")
        }
        raise PermissionDenied
    context = {
        "items": blanck_dict,
        "shipment": shipment,
        "title": f"Confirm Return Products Of Shipment Code {shipment.code}"
    }

    return render (request, "confirmShipmentItemsBack.html", context)
@login_required (login_url='login')
@can_deliver_edit_orders
def deliver_confirm_shipment(request, id):
    user = request.user
    access = AccsessTo.objects.get (user__user=user)
    access_to_user_list = [person for person in access.visitor.all ( )]
    shipment = Shipment.objects.get (id=id)
    order_backed = Order.objects.filter (shipment=shipment, orderkinde=6).first ( )

    if user in access_to_user_list or shipment.distributeur == user:

        orders = Order.objects.filter (shipment=shipment, orderkinde=2)

        sending_message = f"Not settle following orders"
        blank_list = []
        for order in orders:
            if order.settlement.code != 4:
                if float (order.order_finalPrice) - float (order.total_settle) > 0:
                    sending_message.join (f"<p>Oder Number : {order.first_code}</p>")
                    blank_list.append (order.id)
                    print (f'{float (order.order_finalPrice) - float (order.total_settle)} - {order.first_code}')

        if len (blank_list) == 0:

            shipment.checked_out_3 = True
            shipment.save ( )
            if order_backed is not None:
                order_backed.checked_out = True
                order_backed.save ( )
            else:
                shipment.checked_out_4 = True
                shipment.save ( )

            return redirect ("deliver_shipment_view")

        else:
            message = messages.warning (request, sending_message)
            context = {
                "message": message
            }

            return redirect ("deliver_shipment_view")

@login_required (login_url='login')
@can_deliver_confirm_shipment
def deliver_shipment_view(request):
    user = request.user
    user_warehouse_access = Access.objects.filter (user_id=user.id).first ( )
    warehouse_list = [item.id for item in user_warehouse_access.warehouse.all ( )]
    all_shipment = Shipment.objects.filter (warehouse_id__in=warehouse_list, distributeur=user
                                            , checked_out_3=False, checked_out_2=True)
    access = AccsessTo.objects.all ( )
    # if Setting.can_access_all_shipment == True:

    form = Disrobuter
    context = {
        'all_shipment': all_shipment,
        "form": form,


    }

    return render (request, 'deliverConfirmation.html', context)
@login_required (login_url='login')
@can_accounting_shipment
def show_shipments_ready_for_accounting(request):
    shipments = Shipment.objects.filter (checked_out_2=True)
    context = {
        "shipments": shipments
    }
    if request.method == "POST":
        form = dict(request.POST)
        try:
            if form["status"][0] == "1":
                context["onway"] = 1
                context['shipments']=Shipment.objects.filter (checked_out_2=True,checked_out_3=False)
            elif form["status"][0] == "2":
                context["accounting"] = 1
                context['shipments'] = Shipment.objects.filter (checked_out_2=True, checked_out_3=True,checked_out_4=True,checked_out_5=False)
            elif form["status"][0] == "3":
                context["settled"] = 1
                context['shipments'] = Shipment.objects.filter (checked_out_2=True, checked_out_3=True, checked_out_4=True,checked_out_5=True)
            elif  form["status"][0] == "4":
                pass
        except KeyError:
            pass


    return render (request, "showReadyAccountingShipmnets.html", context)



@login_required (login_url='login')
@can_accounting_shipment
def accounting_shipment(request, id):

    form = dict(request.POST)
    user = request.user
    access = Access.objects.get(user = user)
    boxes = access.box.all()
    shipment = Shipment.objects.get (id=id, checked_out_4=True)
    orders = Order.objects.filter (shipment=shipment, orderkinde=2)
    settlment = delivery_settlment.objects.filter (sell_order__shipment=shipment)
    if shipment.checked_out_5 ==True:
        raise PermissionDenied
    if request.method == "POST":


        access_box = access.box.get(id=int(form["Box"][0]))
        box = access_box.accountside

        for order in orders:
            last_order = Order.objects.filter (orderkinde_id=2).order_by ("fianl_code").last ( )
            last_order_code = 1
            if last_order.fianl_code:
                last_order_code += last_order.fianl_code
            if order.order_finalPrice > 0:
                last_cod = 1
                if DocumentNumber.objects.last ( ):
                    code = DocumentNumber.objects.last ( )
                    last_cod += code.code
                warehouse = order.warhouse
                warehouse_account = warehouse.accountside
                journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                relation = OrderJournalRelation.objects.create (order=order, document_number=journal_number)

                off = order.off_price
                vat = order.vat_price

                order_items = OrderItem.objects.filter (order=order)

                ending_inventory = 0
                for item in order_items:
                    inventory = Inventory.objects.get (product=item.product, warehouse=order.warhouse)
                    ending = inventory.average_buy_price * item.quantity
                    ending_inventory += ending

                auto_journal = AutoJoournalFields.objects.get (id=2)

                if order.checked_out == True:
                    order.checked_out_2 = True
                    order.save ( )
                    order.fianl_code = int (last_order_code)
                    order.save ( )

                    debtor1 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code),
                        detailed_account=order.accountside,
                        debtor=order.order_finalPrice,
                        creditor=0,
                        description=f"for finalize sale order number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for selling "
                                    f"to {order.accountside.name}"
                    )

                    creditor1 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code),
                        detailed_account=None,
                        debtor=0,
                        creditor=order.gross_total_price,
                        description=f"for finalize sale order number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for selling "
                                    f"to {order.accountside.name}"
                    )

                    debtor2 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code_2),
                        detailed_account=None,
                        debtor=ending_inventory,
                        creditor=0,
                        description=f"For Sale Number{order.fianl_code}"
                    )
                    creditor2 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code_2),
                        detailed_account=warehouse_account,
                        debtor=0,
                        creditor=ending_inventory,
                        description=f"For Sale Number{order.fianl_code}")

                    debtor3 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code_3),
                        detailed_account=None,
                        debtor=off,
                        creditor=0,
                        description=f"For Sale Number{order.fianl_code}"
                    )

                    creditor3 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code_3),
                        detailed_account=None,
                        debtor=0,
                        creditor=vat,
                        description=f"For Sale Number{order.fianl_code}"
                    )
                    if order.cash:
                        cashs = order.cash
                        for cash in cashs:
                            last_cod = 1
                            if DocumentNumber.objects.last ( ):
                                code = DocumentNumber.objects.last ( )
                                last_cod += code.code

                            cash_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                            box_cach_auto_journal = AutoJoournalFields.objects.get(id=3)

                            debtor1 = Document.objects.create (
                                number=cash_journal_number,
                                difinit_account=DifinitAccounts.objects.get (code=box_cach_auto_journal.debt_code),
                                detailed_account=box,
                                debtor=cash.amount,
                                creditor=0,
                                description=f"Recieved For Invoice {order.fianl_code}"
                            )

                            creditor1 = Document.objects.create (
                                number=cash_journal_number,
                                difinit_account=DifinitAccounts.objects.get (code=box_cach_auto_journal.credit_code),
                                detailed_account=order.accountside,
                                debtor=0,
                                creditor=cash.amount,
                                description=f"Payed For Invoice {order.fianl_code}"
                            )
                            OrderJournalRelation.objects.create(
                                order = order,
                                document_number=cash_journal_number
                            )
                            cash.check_out_1 = True
                            cash.save()
                    if order.pose:
                        poses= order.pose
                        for pose in poses:
                            last_cod = 1
                            if DocumentNumber.objects.last ( ):
                                code = DocumentNumber.objects.last ( )
                                last_cod += code.code

                            pose_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                            box_pose_auto_journal = AutoJoournalFields.objects.get (id=3)

                            debtor1 = Document.objects.create (
                                number= pose_journal_number,
                                difinit_account=DifinitAccounts.objects.get (code=box_pose_auto_journal.debt_code_2),
                                detailed_account=pose.bank_pose.accountside,
                                debtor=pose.amount,
                                creditor=0,
                                description=f"Recieved For Invoice {order.fianl_code}"
                            )

                            creditor1 = Document.objects.create (
                                number= pose_journal_number,
                                difinit_account=DifinitAccounts.objects.get (code=box_pose_auto_journal.credit_code_2),
                                detailed_account=order.accountside,
                                debtor=0,
                                creditor=pose.amount,
                                description=f"Payed For Invoice {order.fianl_code}"
                            )
                            OrderJournalRelation.objects.create (
                                order=order,
                                document_number= pose_journal_number
                            )
                            pose.check_out_1 = True
                            pose.save ( )
                    if order.cheque:
                        cheques= order.cheque
                        for cheque in cheques:
                            last_cod = 1
                            if DocumentNumber.objects.last ( ):
                                code = DocumentNumber.objects.last ( )
                                last_cod += code.code

                            cheque_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                            box_cheque_auto_journal = AutoJoournalFields.objects.get (id=3)

                            debtor1 = Document.objects.create (
                                number= cheque_journal_number,
                                difinit_account=DifinitAccounts.objects.get (code=box_cheque_auto_journal.debt_code_3),
                                detailed_account= box,
                                debtor= cheque.amount,
                                creditor=0,
                                description=f"Recieved For Invoice {order.fianl_code}"
                                            f"Cheque with serial number {cheque.serial_num}"
                                            f"belongs to {cheque.bank.name} Bank"
                            )

                            creditor1 = Document.objects.create (
                                number= cheque_journal_number,
                                difinit_account=DifinitAccounts.objects.get (code= box_cheque_auto_journal.credit_code_3),
                                detailed_account=order.accountside,
                                debtor=0,
                                creditor= cheque.amount,
                                description=f"Payed For Invoice {order.fianl_code}"
                                            f"Cheque with serial number {cheque.serial_num}"
                                            f"belongs to {cheque.bank.name} Bank"
                            )
                            OrderJournalRelation.objects.create (
                                order=order,
                                document_number= cheque_journal_number
                            )
                            cheque.check_out_1 = True
                            cheque.save ( )

                    order.data_convert_invoice = datetime.now()
                    order.save()


        shipment.checked_out_5 = True
        shipment.save ( )

        return redirect ("show_shipments_ready_for_accounting")

    context = {
        "form": form,
        "boxes":boxes,
        "orders": orders,
        "shipment": shipment,
        "settlment": settlment
    }

    return render (request, "accountingShipmnet.html", context)


# ======================REPORTS================================================

@login_required (login_url='login')
@can_sell_sended_order_report
def sell_sended_order_report(request):
    sended_order = OrderItemBackup.objects.all ( )

    context = {
        "orders": sended_order
    }

    return render (request, "sendedOrdersReport.html", context)

@login_required (login_url='login')
@can_invoices_report
def invoices_report(request):

    invoices = Order.objects.filter(fianl_code__isnull=False,orderkinde=2)


    context = {
        "title": "Sold Invoices Report",
        "invoices":invoices
    }

    return render(request,"invoivesReport.html",context)

@login_required (login_url='login')
@can_invoices_report
def invoices_product_report(request):

    items = OrderItem.objects.filter(order__fianl_code__isnull=False,order__orderkinde=2)

    context={
        "items" : items
    }

    return render(request,"products.html",context)

@login_required (login_url='login')
@can_settled_shipment_reports
def settletd_shipment_report(request,id):

    shipment = Shipment.objects.get(id = id)

    orders = Order.objects.filter(shipment=shipment,orderkinde=2)



    context = {
        "shipment":shipment,
        "orders":orders,
    }


    return render(request,"settledShipmentReport.html",context)

@login_required (login_url='login')
@can_invoices_report
def return_report(request):

    back_up = OrderItemBackup.objects.all()
    order_finalize = OrderItem.objects.filter(order__fianl_code__isnull=False)





# =================== CHART ===================================================

import pandas as pd
from datetime import datetime



@login_required (login_url='login')
@can_invoices_report
def chart(request):
    order = Order.objects.filter(orderkinde_id=2).order_by("creation_date").first()
    datelist = pd.date_range (order.creation_date, periods=19).tolist ( )
    items = OrderItem.objects.filter(order__creation_date__range=[min(datelist),max(datelist)],order__orderkinde_id=2)
    date_quantity_dict = {}
    for date in datelist:
        date_quantity_dict[date.date().strftime('%y-%m-%d')] = 0
    quantity = 0
    for item in items:
        quantity+=item.quantity/item.product.box
        date_quantity_dict[item.order.creation_date.date().strftime('%y-%m-%d')]+=item.quantity/item.product.box

    lable = list(date_quantity_dict.keys())
    data=list(date_quantity_dict.values())
    context = {
        "data": data,
        "lable":lable
    }


    return render(request,"chart.html",context)

