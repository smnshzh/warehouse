from django.core.exceptions import PermissionDenied

from .models import *


def can_register(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.register:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_product_view(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.product_views:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_products_detail(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.products_detail:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_auto_inventory_maker(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.auto_inventory_maker:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap



def can_make_buy_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.make_buy_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_show_buy_orders(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_buy_orders:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_show_confirmed_buy(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_confirmed_buy:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_edit_buy_oder(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.edit_buy_oder:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_confirm_buy_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.confirm_buy_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_delete_buy_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.delete_buy_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_see_confirmed_buy(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.see_confirmed_buy:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_deconfirm_buy_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.deconfirm_buy_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_make_buy_back(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.deconfirm_buy_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap
def can_show_buy_back(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_buy_back:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_warhouse_confirm_buy_back(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.deconfirm_buy_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_deconfirm_buy_back(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.deconfirm_buy_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_make_sell_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.make_sell_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_confirm_sell_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.confirm_sell_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_edit_sell_oder(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.edit_sell_oder:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap
def can_remove_sell_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.edit_sell_oder:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap
def can_send_for_SCM(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.send_for_SCM:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_settel_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.settel_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_make_sell_back(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.make_sell_back:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_show_sell_back_orders(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_sell_back_orders:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_confirm_sell_back(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.confirm_sell_back:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap



def can_make_shipment(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.make_shipment:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_show_shipment_orders(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_shipment_orders:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_edit_shipment(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.edit_shipment:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_confirm_shipment(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.confirm_shipment:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_recieve_and_send_shipments(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.recieve_shipments:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_cancle_sending(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.cancle_sending:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_all_shipment_view(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.cancle_sending:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_view_shipment_items(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.view_shipment_items:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_view_shipment_items_backed(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.view_shipment_items_backed:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_confirm_shipment_items_backed(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.confirm_shipment_items_backed:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_deliver_confirm_shipment(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.deliver_confirm_shipment:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap
def can_deliver_edit_orders(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.deliver_edit_orders:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_accounting_after_return(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.accounting_after_return:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_see_shipment_ready_for_accounting(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.see_shipment_ready_for_accounting:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_accounting_shipment(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.accounting_shipment:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def accesse_to_sell(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)
        orderkind_list = [item.name for item in access.orderkind.all ( )]
        if "sell" in orderkind_list and access.make_sell_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def can_sell_sended_order_report(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.sell_sended_order_report:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap
def can_invoices_report(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.sell_sended_order_report:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_settled_shipment_reports(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.sell_sended_order_report:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_make_new_account(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.make_new_account:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_show_accountside(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_accountside:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_making_journal(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_accountside:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_show_journals(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.show_journals:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_auto_journal(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.auto_journal:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_defind_banck_pose(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.defind_banck_pose:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_settle_invoice(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.settle_invoice:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_confirm_settlment(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.confirm_settlment:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_confirm_pay_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.confirm_pay_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_make_pay_order(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.make_pay_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

def can_show_shipments_ready_for_accounting(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        access = Access.objects.get (user=user)

        if access.make_pay_order:
            return function (request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap

