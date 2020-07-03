from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from UserControl.decorators import *
from .forms import *


@login_required (login_url='login')
@can_make_new_account
def new_account(request, id=None):
    form = accountside_form (request.POST or None)
    accounts = accountside.objects.all ( )
    title = "New Account"
    if id != None:
        account = accounts.get (id=id)
        form = accountside_form (instance=account)
        title = "Edit Account"
    if request.method == "POST" and id:
        account = accounts.get (id=id)
        form = accountside_form (request.POST, instance=account)
        form.save ( )
    if request.method == "POST" and id == None:

        if form.is_valid ( ):
            form.save ( )

    context = {
        "title": title,
        'form': form,
        "accounts": accounts,
        "id": id

    }
    return render (request, 'accounting.html', context)


@login_required (login_url='login')
@can_show_accountside
def accountside_show(request):
    accountsides = accountside.objects.all ( )

    context = {
        "accountsides": accountsides
    }

    return render (request, 'accounsidsedetail.html', context)



from cart.models import *


def random_maker(request):
    documents = DocumentNumber.objects.all ( )
    for doc in documents:
        if OrderJournalRelation.objects.filter (document_number=doc).first ( ):

            pass
        else:
            print (doc.code)

    return redirect ("new_account")

@login_required (login_url='login')
@can_making_journal
def making_journal(request):
    form = request.POST
    if request.method == "POST":
        print (form)

    context = {
        "title": "Making Journal"
    }

    return render (request, 'journaling.html', context)

@login_required (login_url='login')
@can_auto_journal
def making_all_journal(request):
    title = " Auto Journal"
    account = 1
    user = request.user
    orders = Order.objects.filter (orderkinde_id__in=[1, 3, 4])

    if request.method == "POST":
        form = dict (request.POST)

        form.pop ("csrfmiddlewaretoken")
        for key in form.keys ( ):

            last_cod = DocumentNumber.objects.last ( )
            journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod.code) + 1)
            order = Order.objects.get (id=key)
            if order.checked_out_2:
                raise PermissionDenied
            OrderJournalRelation.objects.create (order=order, document_number=journal_number,)
            if order.orderkinde.id == 1:
                buy_auto_journal_data = AutoJoournalFields.objects.get (name="Buy")
                definit_account_credit = DifinitAccounts.objects.get (code=buy_auto_journal_data.credit_code)
                definit_account_debt = DifinitAccounts.objects.get (code=buy_auto_journal_data.debt_code)

                last_order = Order.objects.filter (orderkinde_id=1).order_by ("fianl_code").last ( )
                last_order_code = 1
                if last_order.fianl_code:
                    last_order_code += last_order.fianl_code

                order.fianl_code = last_order_code
                order.save ( )
                warehouse = order.warhouse.accountside
                if order.checked_out == True:
                    order.checked_out_2 = True
                    order.save ( )
                    order.fianl_code = int (last_order_code)
                    order.save ( )
                    debtor = Document.objects.create (
                        number=journal_number,
                        difinit_account=definit_account_debt,
                        detailed_account=warehouse,
                        debtor=order.order_finalPrice,
                        creditor=0,
                        description=f"for finalize buy order number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for buying "
                                    f"from {order.accountside.name}"
                    )

                    creditor = Document.objects.create (
                        number=journal_number,
                        difinit_account=definit_account_credit,
                        detailed_account=order.accountside,
                        debtor=0,
                        creditor=order.order_finalPrice,
                        description=f"for finalize buy order number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for buying "
                                    f"from {order.accountside.name}"
                    )

            if order.orderkinde.id == 3:
                buy_auto_journal_data = AutoJoournalFields.objects.get (name="Buy")
                definit_account_credit = DifinitAccounts.objects.get (code=buy_auto_journal_data.credit_code)
                definit_account_debt = DifinitAccounts.objects.get (code=buy_auto_journal_data.debt_code)

                last_buy_back = Order.objects.filter (orderkinde_id=3).last ( )
                last_buy_back_code = 1
                if last_buy_back.fianl_code:
                    last_buy_back_code += last_buy_back.fianl_code

                order.fianl_code = last_buy_back_code

                warehouse = order.warhouse.accountside
                if order.checked_out == True:
                    debtor = Document.objects.create (
                        number=journal_number,
                        difinit_account=definit_account_debt,
                        detailed_account=warehouse,
                        debtor=0,
                        creditor=order.order_finalPrice,
                        description=f"for finalize buy back number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for return product "
                                    f"to {order.accountside.name}"
                    )

                    creditor = Document.objects.create (
                        number=journal_number,
                        difinit_account=definit_account_credit,
                        detailed_account=order.accountside,
                        debtor=order.order_finalPrice,
                        creditor=0,
                        description=f"for finalize buy back number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for return product "
                                    f"to {order.accountside.name}"
                    )
                    order.checked_out_2 = True
                    order.save ( )
                    order.fianl_code = int (last_buy_back_code)
                    order.save ( )

            if order.orderkinde.id == 4:
                sell_back_auto_journal_data = AutoJoournalFields.objects.get (id=4)
                definit_account_credit = DifinitAccounts.objects.get (
                    code=sell_back_auto_journal_data.credit_code)
                definit_account_debt = DifinitAccounts.objects.get (
                    code=sell_back_auto_journal_data.debt_code)
                off = order.off_price
                vat = order.vat_price
                last_sell_back = Order.objects.filter (orderkinde_id=4).last ( )
                last_sell_back_code = 1
                if last_sell_back.fianl_code:
                    last_sell_back_code += last_sell_back.fianl_code

                order.fianl_code = last_sell_back_code

                order_items = OrderItem.objects.filter (order=order)

                ending_inventory = 0
                for item in order_items:
                    inventory = Inventory.objects.get (product=item.product, warehouse=order.warhouse)
                    ending = inventory.average_buy_price * item.quantity
                    ending_inventory += ending

                warehouse = accountside.objects.get (name=order.warhouse.name)
                if order.checked_out == True and order.checked_out_2 == False:
                    debtor = Document.objects.create (
                        number=journal_number,
                        difinit_account=definit_account_debt,
                        detailed_account=None,
                        debtor=order.order_finalPrice,
                        creditor=0,
                        description=f"for finalize sell back number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for return product "
                                    f"to {order.accountside.name}"
                    )
                    if vat > 0:
                        debtor2 = Document.objects.create (
                            number=journal_number,
                            difinit_account=DifinitAccounts.objects.get (
                                code=sell_back_auto_journal_data.debt_code_2),
                            detailed_account=None,
                            debtor=vat,
                            creditor=0,
                            description=f"for finalize sell back number {order.first_code} "
                                        f"and convert to invoice number {order.fianl_code} for return product "
                                        f"to {order.accountside.name}"
                        )
                    creditor = Document.objects.create (
                        number=journal_number,
                        difinit_account=definit_account_credit,
                        detailed_account=order.accountside,
                        debtor=0,
                        creditor=order.gross_total_price,
                        description=f"for finalize sell back number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for return product "
                                    f"to {order.accountside.name}"
                    )
                    debtor3 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (
                            code=sell_back_auto_journal_data.debt_code_3),
                        detailed_account=warehouse,
                        debtor=ending_inventory,
                        creditor=0,
                        description=f"for finalize sell back number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for return product "
                                    f"to {order.accountside.name}"
                    )

                    creditor3 = Document.objects.create (
                        number=journal_number,
                        difinit_account=DifinitAccounts.objects.get (
                            code=sell_back_auto_journal_data.credit_code_3),
                        detailed_account=None,
                        debtor=0,
                        creditor=ending_inventory,
                        description=f"for finalize sell back number {order.first_code} "
                                    f"and convert to invoice number {order.fianl_code} for return product "
                                    f"to {order.accountside.name}"
                    )

                    order.checked_out_2 = True
                    order.save ( )
                    order.fianl_code = int (last_sell_back_code)
                    order.save ( )


        return redirect ('auto_journal')

    context = {
        "title": "Auto Journal",
        "orders": orders,
        "account": account,
        "title": title
    }

    return render (request, "buyorder.html", context)

@login_required (login_url='login')
@can_show_journals
def show_journals(request):
    journals = Document.objects.all ( )
    sum_debt = sum ([journal.debtor for journal in journals])
    sum_credit = sum ([journal.creditor for journal in journals])
    totals = TotalAccounts.objects.all ( ).order_by ("name")
    selected = 0
    if request.method == "POST":
        form = dict (request.POST)
        selected = int (form["total"][0])
        if selected != 0:
            total = totals.get (id=selected)
            journals = journals.filter (difinit_account__total_account=total)

    context = {
        "title": "Journals Report",
        'journals': journals,
        'sum_debt': sum_debt,
        'sum_credit': sum_credit,
        'selected': selected,
        "totals": totals
    }

    return render (request, 'journals.html', context)

@login_required (login_url='login')
@can_defind_banck_pose
def define_bank_pose(request):
    banks = BankPose.objects.all ( )
    regions = local_id_def.objects.all()

    if request.method == "POST":
        form = dict (request.POST)
        form.pop ("csrfmiddlewaretoken")
        account = accountside.objects.create (
            id_code=int (form["code"][0]),
            name=f"{form['name'][0]} bank {form['branch'][0]}",
            region=local_id_def.objects.get(id = int(form["region"][0])),
            telephonnumber=form["tel"][0]

        )
        account.kind.add (4)
        BankPose.objects.create (
            code=int (form["code"][0]),
            slug=form["name"][0],
            name=form["name"][0],
            branch=form["branch"][0],
            accountside=account

        )

    context = {
        "banks": banks,
        "regions":regions,
    }

    return render (request, "defindeBanckPose.html", context)

@login_required (login_url='login')
@can_settle_invoice
def settle_invoice(request):
    invoices = Order.objects.filter (fianl_code__isnull=False, orderkinde_id__in=[1, 2])

    if request.method == "POST":
        form = dict (request.POST)

        try:
            if form["type"]:
                if len (form["type"]) > 0:
                    invoices = Order.objects.filter (fianl_code__isnull=False, orderkinde_id__in=form["type"])
        except KeyError:
            pass

    context = {
        "settle": 1,
        "invoices": invoices
    }

    return render (request, 'invoivesReport.html', context)


from UserControl.models import Access

@login_required (login_url='login')
@can_confirm_settlment
def confirm_settelmenet(request):
    user = request.user
    settelments = delivery_settlment.objects.filter (sell_order__orderkinde_id=2,sell_order__isnull=False, user=user, check_out_1=False)
    access = Access.objects.get (user=user)
    access_box = access.box.all ( )
    if request.method == "POST":

        form = dict (request.POST)
        box_id = form["Box"][0]
        box = Safe_Box.objects.filter (id=box_id).first ( )
        if box in access_box:
            box_account = box.accountside
            auto_journal = AutoJoournalFields.objects.get (id=3)

            if "cash" in form.keys ( ):
                for cash in form["cash"]:
                    last_cod = 1
                    if DocumentNumber.objects.last ( ):
                        code = DocumentNumber.objects.last ( )
                        last_cod += code.code
                    settle = delivery_settlment.objects.get (id=cash)
                    order = settle.sell_order
                    if settle.check_out_1 == False and order.orderkinde.id == 2:

                        cash_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                        debtor1 = Document.objects.create (
                            number=cash_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code),
                            detailed_account=box_account,
                            debtor=settle.amount,
                            creditor=0,
                            description=f"Recieved For Invoice {order.fianl_code}"
                        )

                        creditor1 = Document.objects.create (
                            number=cash_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code),
                            detailed_account=order.accountside,
                            debtor=0,
                            creditor=settle.amount,
                            description=f"Payed For Invoice {order.fianl_code}"
                        )
                        OrderJournalRelation.objects.create (
                            order=order,
                            document_number=cash_journal_number,
                            descripion=f"For settele invoice {order.fianl_code}"
                        )
                        settle.check_out_1 = True
                        settle.save ( )

                    else:
                        context = {
                            "message": messages.warning (request,
                                                         "<h5 style='color:red'>this settlement confirmed BEFORE</h5>")
                        }
            if "cheque" in form.keys ( ):
                for cheque in form["cheque"]:
                    settle = delivery_settlment.objects.get (id=cheque)
                    order = settle.sell_order
                    if settle.check_out_1 == False and order.orderkinde.id == 2:
                        last_cod = 1
                        if DocumentNumber.objects.last ( ):
                            code = DocumentNumber.objects.last ( )
                            last_cod += code.code
                        order = settle.sell_order
                        cheque_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                        debtor1 = Document.objects.create (
                            number=cheque_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code_3),
                            detailed_account=box_account,
                            debtor=settle.amount,
                            creditor=0,
                            description=f"Recieved For Invoice {order.fianl_code}"
                                        f"Cheque with serial number {settle.serial_num}"
                                        f"belongs to {settle.bank.name} Bank"
                        )

                        creditor1 = Document.objects.create (
                            number=cheque_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code_3),
                            detailed_account=order.accountside,
                            debtor=0,
                            creditor=settle.amount,
                            description=f"Payed For Invoice {order.fianl_code}"
                                        f"Cheque with serial number {settle.serial_num}"
                                        f"belongs to {settle.bank.name} Bank"
                        )
                        OrderJournalRelation.objects.create (
                            order=order,
                            document_number=cheque_journal_number,
                            descripion=f"For settele invoice {order.fianl_code}"
                        )
                        settle.check_out_1 = True
                        settle.save ( )

            if "pose" in form.keys ( ):
                for pose in form["pose"]:
                    settle = delivery_settlment.objects.get (id=pose)
                    order = settle.sell_order
                    if settle.check_out_1 == False and order.orderkinde.id == 2:
                        last_cod = 1
                        if DocumentNumber.objects.last ( ):
                            code = DocumentNumber.objects.last ( )
                            last_cod += code.code
                        order = settle.sell_order
                        pose_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                        debtor1 = Document.objects.create (
                            number=pose_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code_2),
                            detailed_account=settle.bank_pose.accountside,
                            debtor=settle.amount,
                            creditor=0,
                            description=f"Recieved For Invoice {order.fianl_code}"
                        )

                        creditor1 = Document.objects.create (
                            number=pose_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code_2),
                            detailed_account=order.accountside,
                            debtor=0,
                            creditor=settle.amount,
                            description=f"Payed For Invoice {order.fianl_code}"
                        )
                        OrderJournalRelation.objects.create (
                            order=order,
                            document_number=pose_journal_number,
                            descripion=f"For settele invoice {order.fianl_code}"
                        )
                        settle.check_out_1 = True
                        settle.save ( )

        else:
            context = {
                "message": messages.warning (request, f"You Do Not Access To {box.name}")
            }

    context = {
        "cashs": settelments.filter (settel_kinde__code=1),
        "poses": settelments.filter (settel_kinde__code=2),
        "cheques": settelments.filter (settel_kinde__code=3),
        "access_box": access_box,
    }

    return render (request, "confirmSettelmets.html", context)
@login_required (login_url='login')
@can_confirm_pay_order
def confirm_pay_order(request):
    user = request.user
    settelments = delivery_settlment.objects.filter (sell_order__orderkinde_id=1,sell_order__isnull=False, user=user, check_out_1=False)
    access = Access.objects.get (user=user)
    access_box = access.box.all ( )
    if request.method == "POST" and access.confirm_pay_order:

        form = dict (request.POST)
        box_id = form["Box"][0]
        box = Safe_Box.objects.filter (id=box_id).first ( )
        if box in access_box:
            box_account = box.accountside
            auto_journal = AutoJoournalFields.objects.get (id=5)

            if "cash" in form.keys ( ):
                for cash in form["cash"]:
                    last_cod = 1
                    if DocumentNumber.objects.last ( ):
                        code = DocumentNumber.objects.last ( )
                        last_cod += code.code
                    settle = delivery_settlment.objects.get (id=cash)
                    order = settle.sell_order
                    if settle.check_out_1 == False and order.orderkinde.id == 1:
                        order = settle.sell_order
                        cash_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                        debtor1 = Document.objects.create (
                            number=cash_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code),
                            detailed_account=order.accountside,
                            debtor=settle.amount,
                            creditor=0,
                            description=f"Payed For Buy Invoice {order.fianl_code}"
                        )

                        creditor1 = Document.objects.create (
                            number=cash_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code),
                            detailed_account= box_account,
                            debtor=0,
                            creditor=settle.amount,
                            description=f"Received For Buy Invoice {order.fianl_code}"
                        )
                        OrderJournalRelation.objects.create (
                            order=order,
                            document_number=cash_journal_number,
                            descripion=f"For settele invoice {order.fianl_code}"
                        )
                        settle.check_out_1 = True
                        settle.save ( )

                    else:
                        context = {
                            "message": messages.warning (request,
                                                         "<h5 style='color:red'>this settlement confirmed BEFORE</h5>")
                        }
            if "cheque" in form.keys ( ):
                for cheque in form["cheque"]:
                    settle = delivery_settlment.objects.get (id=cheque)
                    order = settle.sell_order
                    if settle.check_out_1 == False and order.orderkinde.id == 1:
                        last_cod = 1
                        if DocumentNumber.objects.last ( ):
                            code = DocumentNumber.objects.last ( )
                            last_cod += code.code
                        order = settle.sell_order
                        cheque_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                        debtor1 = Document.objects.create (
                            number=cheque_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code_3),
                            detailed_account=order.accountside,
                            debtor=settle.amount,
                            creditor=0,
                            description=f"Payed For Invoice {order.fianl_code}"
                                        f"Cheque with serial number {settle.serial_num}"
                                        f"belongs to {settle.bank_pose.name} Bank"
                        )

                        creditor1 = Document.objects.create (
                            number=cheque_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code_3),
                            detailed_account=settle.bank_pose.accountside,
                            debtor=0,
                            creditor=settle.amount,
                            description=f"Payed For Buy Invoice {order.fianl_code}"
                                        f"Cheque with serial number {settle.serial_num}"
                                        f"belongs to {settle.bank_pose.name} Bank"
                        )
                        OrderJournalRelation.objects.create (
                            order=order,
                            document_number=cheque_journal_number,
                            descripion=f"For settele Buy invoice {order.fianl_code}"
                        )
                        settle.check_out_1 = True
                        settle.save ( )

            if "pose" in form.keys ( ):
                for pose in form["pose"]:
                    settle = delivery_settlment.objects.get (id=pose)
                    order = settle.sell_order
                    if settle.check_out_1 == False and order.orderkinde.id == 1:
                        last_cod = 1
                        if DocumentNumber.objects.last ( ):
                            code = DocumentNumber.objects.last ( )
                            last_cod += code.code
                        order = settle.sell_order
                        pose_journal_number = DocumentNumber.objects.create (createur=user, code=int (last_cod))
                        debtor1 = Document.objects.create (
                            number=pose_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.debt_code_2),
                            detailed_account= order.accountside,
                            debtor=settle.amount,
                            creditor=0,
                            description=f"Recieved For Buy Invoice {order.fianl_code}"
                        )

                        creditor1 = Document.objects.create (
                            number=pose_journal_number,
                            difinit_account=DifinitAccounts.objects.get (code=auto_journal.credit_code_2),
                            detailed_account=settle.bank_pose.accountside,
                            debtor=0,
                            creditor=settle.amount,
                            description=f"Payed For Invoice {order.fianl_code}"
                        )
                        OrderJournalRelation.objects.create (
                            order=order,
                            document_number=pose_journal_number,
                            descripion=f"For settele Buy invoice {order.fianl_code}"
                        )
                        settle.check_out_1 = True
                        settle.save ( )

        else:
            context = {
                "message": messages.warning (request, f"You Do Not Access To {box.name}")
            }

    context = {
        "cashs": settelments.filter (settel_kinde__code=1),
        "poses": settelments.filter (settel_kinde__code=2),
        "cheques": settelments.filter (settel_kinde__code=3),
        "access_box": access_box,
    }

    return render (request, "confirmSettelmets.html", context)
@login_required (login_url='login')
@can_show_accountside
def my_map(request):
    geos = GeoAccount.objects.all ( )

    if request.method == "POST":
        form = request.POST

    context = {
        "geos": geos
    }

    return render (request, "map.html", context)


# ================= Reports ===========================================

@login_required (login_url='login')
@can_show_journals
def detailed_account_report(request, id):
    detailed_account = accountside.objects.get (id=id)
    difinit_accounts = DifinitAccounts.objects.all ( ).order_by ("name")
    journals = Document.objects.filter (detailed_account=detailed_account)
    selected = 0
    if request.method == "POST":
        form = dict (request.POST)
        selected = int (form["difinit"][0])
        if selected != 0:
            difinit_account = difinit_accounts.get (id=selected)
            journals = journals.filter (difinit_account=difinit_account)

    context = {
        "journals": journals,
        "difinits": difinit_accounts,
        "selected": selected
    }

    return render (request, "journalsReports.html", context)
