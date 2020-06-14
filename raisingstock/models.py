from django.db import models
from accountside.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from Shop.models import *



class buyOrder(models.Model):
    code = models.PositiveIntegerField(blank=True,null=True)
    creation_date = models.DateTimeField (verbose_name=_('creation date'))
    checked_out = models.BooleanField (default=False, verbose_name=_('checked out'))
    checked_out_2 = models.BooleanField (default=False, verbose_name=_('checked out'))
    warehouse = models.ForeignKey (WareHouseDefinde, on_delete=models.CASCADE)
    path = models.ImageField(blank=True,null=True)

    user_craeter = models.CharField (max_length=45)
    accountside = models.ForeignKey (accountside, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.id}'

    def final_price(self):
        selected_items = buyOrder_items.objects.filter(buyorder_id = self.id)
        sumTotalPrice = sum([item.total_price for item in selected_items])
        return sumTotalPrice
    total_price = property(final_price)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).filter(*args, **kwargs)


class buyOrder_items(models.Model):
    buyorder = models.ForeignKey (buyOrder, verbose_name=_ ('buyorder'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField (verbose_name=_ ('quantity'))
    unit_price = models.DecimalField (max_digits=18, decimal_places=2, verbose_name=_ ('unit price'))

    # product as generic relation
    content_type = models.ForeignKey (ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField ( )
    warehouse = models.ForeignKey(WareHouseDefinde,on_delete = models.DO_NOTHING,null = True,blank = True)


    objects = ItemManager ( )

    class Meta:
        verbose_name = _ ('item')
        verbose_name_plural = _ ('items')
        ordering = ('buyorder',)

    def total_price(self):
        return self.quantity * self.unit_price

    total_price = property (total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type (pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model (type (product))
        self.object_id = product.pk

    product = property (get_product, set_product)


class buyBack (models.Model):
    creation_date = models.DateTimeField (verbose_name=_ ('creation date'))
    checked_out = models.BooleanField (default=False, verbose_name=_ ('checked out'))
    checked_out_2 = models.BooleanField (default=False, verbose_name=_ ('checked out'))

    user_craeter = models.CharField (max_length=45)
    accountside = models.ForeignKey (accountside, on_delete=models.CASCADE)


    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.id}'

    # def order_totalPrice (self):
    #     select = OrderItem.objects.filter(order_id = self.id)
    #
    #     return sum([item.total_price for item in select])
    #
    # order_finalPrice = property(order_totalPrice)


from decimal import Decimal as D
class buyBackItem (models.Model):
    order = models.ForeignKey (buyBack, on_delete=models.CASCADE, blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True,null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)

    def total_price(self):
         totalite = self.quantity*self.unit_price
         return  D(totalite).quantize(D('0.01'))

    total_price = property (total_price)



    class Meta:
        ordering = ('id',)
        # unique_together=('order','object_id')


class wareHouseInvoice(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)
    creeateur = models.ForeignKey(User,on_delete=models.DO_NOTHING)

class invoiceItem(models.Model):

    invoice = models.ForeignKey(wareHouseInvoice,on_delete=models.CASCADE)



