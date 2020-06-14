from django.db import models
from Shop.models import *
from django.contrib.auth.models import User
from accountside.models import *
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal as D

class settlement(models.Model):

    code = models.IntegerField()
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name



class Shipment (models.Model):
    code= models.PositiveIntegerField()
    creation_date = models.DateTimeField (verbose_name=_ ('creation date'))
    checked_out = models.BooleanField (default=False, verbose_name=_ ('recieved'))
    checked_out_2 = models.BooleanField (default=False, verbose_name=_ ('send'))
    checked_out_3 = models.BooleanField (default=False, verbose_name=_ ('disributer confirm'))
    checked_out_4 = models.BooleanField (default=False, verbose_name=_ ('warehouse confirm'))
    checked_out_5 = models.BooleanField (default=False, verbose_name=_ ('accounting'))
    user_craeter = models.CharField (max_length=12)
    distributeur = models.ForeignKey (User, on_delete=models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey(WareHouseDefinde,on_delete=models.CASCADE)
    description = models.TextField (blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.id}'

    def shipment_totalPrice(self):
        select_order = Order.objects.filter (shipment_id=self.id,orderkinde=2)

        total_sum =sum([item.order_finalPrice for item in select_order])

        return   D(total_sum).quantize(D('0.01'))


    total_price = property (shipment_totalPrice)

    def total_box(self):
        order_items = OrderItem.objects.filter( order__shipment_id = self.id)

        items = [item.quantity / item.product.box for item in order_items]
        return sum (items)

    def shipment_items(self):
        items = OrderItem.objects.filter(order__shipment_id = self.id)
        blank_list = {}
        for item in items:
            if item.product in blank_list.keys():
                blank_list[item.product] += int(item.quantity)
            else:
                blank_list[item.product] = int(item.quantity)

        return blank_list

    shipment_items = property(shipment_items)

    def total_box_back(self):
        order_items = OrderItem.objects.filter( order__shipment_id = self.id,order__orderkinde_code = 6)

        items = [item.quantity / item.product.box for item in order_items]
        return sum (items)


    def total_settle(self):
        select_order = Order.objects.filter (shipment_id=self.id, orderkinde=2)


        total_sum = sum ([item.total_settle_for_shipment for item in select_order])

        return D (total_sum).quantize (D ('0.01'))

    total_settle= property(total_settle)


    def cash_total_settle(self):
        select_order = Order.objects.filter (shipment_id=self.id, orderkinde=2)


        total_sum = sum ([item.total_settle_cash_befor_final for item in select_order])

        return D (total_sum).quantize (D ('0.01'))

    cash_total_settle= property(cash_total_settle)


    def pose_total_settle(self):
        select_order = Order.objects.filter (shipment_id=self.id, orderkinde=2)


        total_sum = sum ([item.total_settle_pose_befor_final for item in select_order])

        return D (total_sum).quantize (D ('0.01'))

    pose_total_settle= property(pose_total_settle)


    def cheque_total_settle(self):
        select_order = Order.objects.filter (shipment_id=self.id, orderkinde=2)


        total_sum = sum ([item.total_settle_cheque_befor_final for item in select_order])

        return D (total_sum).quantize (D ('0.01'))

    cheque_total_settle= property(cheque_total_settle)

    def total_remain(self):
        total_remain = float(self.total_price) - float(self.total_settle)

        return total_remain

    total_remain = property(total_remain)


    def shipment_return(self):

        order = Order.objects.filter(shipment=self,orderkinde=6)

        return order

class shipmentBack(models.Model):
    shipment = models.ForeignKey(Shipment,null=True,blank=True,on_delete=models.CASCADE)
    code = models.PositiveIntegerField ( )
    creation_date = models.DateTimeField (verbose_name=_ ('creation date'))
    checked_out = models.BooleanField (default=False, verbose_name=_ ('recieved'))
    checked_out_2 = models.BooleanField (default=False, verbose_name=_ ('send'))
    checked_out_3 = models.BooleanField (default=False, verbose_name=_ ('accounting'))
    user_craeter = models.CharField (max_length=12)
    distributeur = models.ForeignKey (User, on_delete=models.DO_NOTHING, blank=True, null=True)
    warehouse = models.ForeignKey (WareHouseDefinde, on_delete=models.CASCADE)
    description = models.TextField (blank=True, null=True)


class OrderKinde(models.Model):

    code = models.PositiveIntegerField()
    name = models.CharField(max_length=10)

class Order (models.Model):

    first_code = models.PositiveIntegerField()
    fianl_code = models.PositiveIntegerField(blank=True,null=True)
    creation_date = models.DateTimeField (auto_now_add=True,verbose_name=_ ('creation date'))
    checked_out = models.BooleanField (default=False, verbose_name=_ ('checked out'))
    checked_out_2 = models.BooleanField (default=False, verbose_name=_ ('checked out'))
    checked_out_3 = models.BooleanField (default=False, verbose_name=_ ('checked out'))
    checked_out_4 = models.BooleanField (default=False, verbose_name=_ ('checked out'))
    user_craeter = models.CharField (max_length=45)
    accountside = models.ForeignKey (accountside, on_delete=models.CASCADE)
    shipment = models.ForeignKey (Shipment, on_delete=models.SET_NULL, blank=True, null=True)
    shipment_back = models.ForeignKey (shipmentBack, on_delete=models.SET_NULL, blank=True, null=True)
    warhouse = models.ForeignKey(WareHouseDefinde,on_delete = models.DO_NOTHING)
    orderkinde = models.ForeignKey(OrderKinde,on_delete= models.DO_NOTHING,blank=True,null=True)
    visitor = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    settlement = models.ForeignKey(settlement,on_delete=models.SET_DEFAULT,default=1)
    row = models.PositiveIntegerField(default=0)
    orderid = models.PositiveIntegerField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    data_convert_invoice = models.DateTimeField(null=True,blank=True)



    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.id}'

    def order_totalPrice (self):
        select = OrderItem.objects.filter(order_id = self.id)

        return sum([item.total_price for item in select])

    order_finalPrice = property(order_totalPrice)


    def gros_total_price(self):
        select = OrderItem.objects.filter (order_id=self.id)

        return float(sum ([item.gross_total_price for item in select]))

    gross_total_price = property(gros_total_price)


    def total_box (self):
        order_items = OrderItem.objects.filter( order_id = self.id)
        items = [item.quantity/item.product.box for item in order_items]
        return sum(items)

    def total_settle_cash(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order,settel_kinde=1)
        items = [0]
        if settle:
            items = [item.amount for item in settle]


        return sum(items)




    def total_settle_pose(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order,settel_kinde=2)
        items = [0]
        if settle:
            items = [item.amount for item in settle]


        return sum(items)



    def total_settle_cheque(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order,settel_kinde=3)
        items = [0]
        if settle:
            items = [item.amount for item in settle]


        return sum(items)


    def total_settle_cash_befor_final(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order,settel_kinde=1)
        if order.fianl_code:
            settle = delivery_settlment.objects.filter(sell_order=order,
                                                       settel_kinde=1,
                                                       now_date__lte=order.data_convert_invoice )
        items = [0]
        if settle:
            items = [item.amount for item in settle]


        return sum(items)

    total_settle_cash_befor_final=property(total_settle_cash_befor_final)


    def total_settle_pose_befor_final(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order,settel_kinde=2)
        if order.fianl_code:
            settle = delivery_settlment.objects.filter(sell_order=order,
                                                       settel_kinde=2,
                                                       now_date__lte=order.data_convert_invoice )
        items = [0]
        if settle:
            items = [item.amount for item in settle]


        return sum(items)

    total_settle_pose_befor_final=property(total_settle_pose_befor_final)

    def total_settle_cheque_befor_final(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order,settel_kinde=3)
        if order.fianl_code:
            settle = delivery_settlment.objects.filter(sell_order=order,
                                                       settel_kinde=3,
                                                       now_date__lte=order.data_convert_invoice )
        items = [0]
        if settle:
            items = [item.amount for item in settle]


        return sum(items)

    total_settle_cheque_befor_final = property(total_settle_cheque_befor_final)








    def cash(self):
        order = Order.objects.get (id=self.id)
        settle = delivery_settlment.objects.filter (sell_order=order, settel_kinde=1)

        return settle
    cash = property(cash)


    def pose(self):
        order = Order.objects.get (id=self.id)
        settle = delivery_settlment.objects.filter (sell_order=order, settel_kinde=2)

        return settle

    pose = property(pose)

    def cheque(self):
        order = Order.objects.get (id=self.id)
        settle = delivery_settlment.objects.filter (sell_order=order, settel_kinde=3)

        return settle

    cheque=property(cheque)

    def total_settle(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order)
        items = [0]
        if settle:
            items = [item.amount for item in settle]


        return sum(items)

    total_settle = property(total_settle)

    def total_settle_for_shipment(self):
        order = Order.objects.get(id = self.id)
        settle = delivery_settlment.objects.filter(sell_order=order)
        items = [0]
        if settle:
            if order.data_convert_invoice:
                items = [item.amount for item in settle if item.now_date < order.data_convert_invoice]
            else:
                items = [item.amount for item in settle]


        return sum(items)

    total_settle_for_shipment = property(total_settle_for_shipment)

    def off_price(self):
        select = OrderItem.objects.filter (order_id=self.id)

        return sum ([item.off_price for item in select])

    off_price = property(off_price)


    def vat_price(self):

        select = OrderItem.objects.filter (order_id=self.id)

        return sum ([item.vat_price for item in select])

    vat_price = property(vat_price)

    def non_settelde_befor_final(self):


        mines =  float(self.order_finalPrice) - float(self.total_settle_for_shipment)
        return mines

    non_settelde_befor_final = property(non_settelde_befor_final)

    def non_settelde(self):


        mines =  float(self.order_finalPrice) - float(self.total_settle)
        return mines

    non_settelde= property(non_settelde)





class OrderItem (models.Model):


    order = models.ForeignKey (Order, on_delete=models.CASCADE, blank=True,null=True)
    vat = models.DecimalField(max_digits=18, decimal_places=2)
    off = models.DecimalField(max_digits=18, decimal_places=2)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True,null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(verbose_name='sell price',max_digits=18, decimal_places=2)

    def total_price(self):
         totalite = self.quantity*((100- self.off)/100)*((100 + self.vat)/100) * self.unit_price
         return  D(totalite).quantize(D('0.01'))

    total_price = property (total_price)

    def gros_total_price(self):
        totalite = self.quantity  * self.unit_price
        return D (totalite).quantize (D ('0.01'))

    gross_total_price = property (gros_total_price)


    def off_price (self):

        off= self.unit_price*self.off/100*self.quantity
        return off

    off_price = property(off_price)

    def vat_price(self):

        vat_price = self.quantity*((100- self.off)/100)*self.unit_price*self.vat/100

        return vat_price

    vat_price = property(vat_price)





    class Meta:
        ordering = ('id',)
        # unique_together=('order','object_id')


class OrderItemBackup (models.Model):


    order = models.ForeignKey (Order, on_delete=models.CASCADE, blank=True,null=True)
    vat = models.DecimalField(max_digits=18, decimal_places=2)
    off = models.DecimalField(max_digits=18, decimal_places=2)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True,null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(verbose_name='sell price',max_digits=18, decimal_places=2)

    def total_price(self):
         totalite = self.quantity*((100- self.off)/100)*((100 + self.vat)/100) * self.unit_price
         return  D(totalite).quantize(D('0.01'))

    total_price = property (total_price)



    class Meta:
        ordering = ('id',)
        # unique_together=('order','object_id')






class delivery_settlment(models.Model):


    sell_order = models.ForeignKey(Order,on_delete=models.CASCADE)
    settel_kinde = models.ForeignKey(settlement,on_delete=models.SET_NULL,null=True)
    bank = models.ForeignKey(BankCheck,on_delete=models.SET_NULL,null=True,blank=True)
    bank_pose = models.ForeignKey(BankPose,on_delete=models.CASCADE,blank=True,null=True)
    now_date = models.DateTimeField(auto_now_add=True)
    usance_date = models.DateTimeField(blank=True,null=True)
    serial_num = models.CharField(max_length=40,blank=True,null=True)
    name = models.CharField(max_length=40,blank=True,null=True)
    amount = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    check_out_1 = models.BooleanField(default=False)
    check_out_2 = models.BooleanField (default=False)
    check_out_3 = models.BooleanField (default=False)

class OrderJournalRelation(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    document_number = models.ForeignKey(DocumentNumber,on_delete=models.CASCADE)
    descripion=models.TextField(null=True,blank=True)
