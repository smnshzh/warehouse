from django.db import models
from django.contrib.auth.models import User
from raisingstock.models import *
from cart.models import OrderKinde


class Access(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    warehouse = models.ManyToManyField(WareHouseDefinde)
    orderkind = models.ManyToManyField(OrderKinde)
    bank_pose = models.ManyToManyField(BankPose)
    box = models.ManyToManyField(Safe_Box)



    make_buy_order = models.BooleanField(default=False)
    edit_buy_oder = models.BooleanField(default=False)
    confirm_buy_order = models.BooleanField(default=False)

    make_sell_order = models.BooleanField(default=False)
    edit_sell_oder = models.BooleanField (default=False)
    confirm_sell_order = models.BooleanField (default=False)

    make_shipment = models.BooleanField(default=False)
    edit_shipment = models.BooleanField(default=False)
    confirm_shipment = models.BooleanField(default=False)

    all_shipment_view = models.BooleanField(default=False)
    accounting_after_return = models.BooleanField(default=False)

    confirm_pay_order = models.BooleanField(default=False)
    make_pay_order = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


class AccsessTo(models.Model):
    user = models.OneToOneField(Access,on_delete=models.CASCADE,unique=True)
    visitor = models.ManyToManyField(User)


