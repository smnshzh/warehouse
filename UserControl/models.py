from django.contrib.auth.models import User

from cart.models import OrderKinde
from raisingstock.models import *


class Access(models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE, unique=True)
    warehouse = models.ManyToManyField (WareHouseDefinde, blank=True)
    orderkind = models.ManyToManyField (OrderKinde, blank=True)
    bank_pose = models.ManyToManyField (BankPose, blank=True)
    box = models.ManyToManyField (Safe_Box, blank=True)
    # buy access
    make_buy_order = models.BooleanField (default=False)
    show_buy_orders = models.BooleanField (default=False)
    edit_buy_oder = models.BooleanField (default=False)
    show_confirmed_buy = models.BooleanField (default=False)
    see_confirmed_buy = models.BooleanField (default=False)
    # buy access relavent to wareehouse
    confirm_buy_order = models.BooleanField (default=False)
    deconfirm_buy_order = models.BooleanField (default=False)
    delete_buy_order = models.BooleanField (default=False)
    # buy back access
    make_buy_back = models.BooleanField (default=False)
    show_buy_back = models.BooleanField (default=False)
    # buy back access relevant to Warehouse
    warhouse_confirm_buy_back = models.BooleanField (default=False)
    deconfirm_buy_back = models.BooleanField (default=False)
    # sell access
    make_sell_order = models.BooleanField (default=False)
    edit_sell_oder = models.BooleanField (default=False)
    confirm_sell_order = models.BooleanField (default=False)
    remove_sell_order = models.BooleanField (default=False)
    send_for_SCM = models.BooleanField (default=False)
    # shipment access
    make_shipment = models.BooleanField (default=False)
    edit_shipment = models.BooleanField (default=False)
    show_shipment_orders = models.BooleanField (default=False)
    view_shipment_items = models.BooleanField (default=False)
    confirm_shipment = models.BooleanField (default=False)
    all_shipment_view = models.BooleanField (default=False)
    view_shipment_items_backed = models.BooleanField (default=False)
    confirm_shipment_items_backed = models.BooleanField (default=False)
    # shipment access relevant to warehouse
    recieve_shipments = models.BooleanField (default=False)
    send_shipments = models.BooleanField (default=False)
    cancle_sending = models.BooleanField (default=False)
    # deliver access
    deliver_confirm_shipment = models.BooleanField (default=False)
    deliver_edit_orders = models.BooleanField (default=False)
    settel_order = models.BooleanField (default=False)
    # sell back access
    make_sell_back = models.BooleanField (default=False)
    show_sell_back_orders = models.BooleanField (default=False)
    confirm_sell_back = models.BooleanField (default=False)
    # accountside access
    make_new_account = models.BooleanField (default=False)
    show_accountside = models.BooleanField (default=False)
    register = models.BooleanField (default=False)
    defind_banck_pose = models.BooleanField (default=False)
    # accounting access
    show_shipments_ready_for_accounting = models.BooleanField (default=False)
    see_shipment_ready_for_accounting = models.BooleanField (default=False)
    accounting_shipment = models.BooleanField (default=False)
    accounting_after_return = models.BooleanField (default=False)
    settle_invoice = models.BooleanField (default=False)
    confirm_settlment = models.BooleanField (default=False)
    make_pay_order = models.BooleanField (default=False)
    confirm_pay_order = models.BooleanField (default=False)
    # journaling access
    making_journal = models.BooleanField (default=False)
    show_journals = models.BooleanField (default=False)
    auto_journal = models.BooleanField (default=False)
    # products access
    product_views = models.BooleanField (default=False)
    products_detail = models.BooleanField (default=False)
    auto_inventory_maker = models.BooleanField (default=False)
    # reports Access
    sell_sended_order_report = models.BooleanField (default=False)
    invoices_report = models.BooleanField (default=False)
    settled_shipment_reports = models.BooleanField (default=False)

    def __str__(self):
        return self.user.username


class AccsessTo(models.Model):
    user = models.OneToOneField(Access,on_delete=models.CASCADE,unique=True)
    visitor = models.ManyToManyField(User)


