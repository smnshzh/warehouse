from django.db import models


class FirstCategory (models.Model):
    name = models.CharField (max_length=10, db_index=True)
    slug = models.SlugField (max_length=10, db_index=True, unique=True)

    class Meta:
        ordering = (['name'])
        verbose_name = 'Main Category'
        verbose_name_plural = 'Main Categories'

    def __str__(self):
        return self.name


class SubCategory (models.Model):
    mainCategory = models.ForeignKey (FirstCategory, on_delete=models.DO_NOTHING)
    name = models.CharField (max_length=10, db_index=True)
    slug = models.SlugField (max_length=10, db_index=True, unique=True)

    class Meta:
        ordering = (['name'])
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name


class Product_Sale_State (models.Model):
    state = models.CharField (max_length=5)
    slug = models.CharField (unique=True, max_length=5, default='')

    def __str__(self):
        return self.state


class ProductOff (models.Model):
    name = models.CharField (max_length=10)
    steps = models.PositiveIntegerField (null=True)
    minQ_1 = models.PositiveIntegerField (null=True)
    maxQ_1 = models.PositiveIntegerField (null=True)
    off_persentage_1 = models.PositiveIntegerField (null=True)
    minQ_2 = models.PositiveIntegerField (null=True)
    maxQ_2 = models.PositiveIntegerField (null=True)
    off_persentage_2 = models.PositiveIntegerField (null=True)
    minQ_3 = models.PositiveIntegerField (null=True)
    maxQ_3 = models.PositiveIntegerField (null=True)
    off_persentage_3 = models.PositiveIntegerField (null=True)
    minQ_4 = models.PositiveIntegerField (null=True)
    maxQ_4 = models.PositiveIntegerField (null=True)
    off_persentage_4 = models.PositiveIntegerField (null=True)

    def __str__(self):
        return self.name


class ProductEchantion (models.Model):
    name = models.CharField (max_length=10)
    quantity = models.PositiveIntegerField ( )
    ech_quantity = models.PositiveIntegerField ( )

    def __str__(self):
        return self.name


class Product (models.Model):
    category = models.ForeignKey (SubCategory, on_delete=models.DO_NOTHING, related_name='Products')
    name = models.CharField (max_length=10, db_index=True)
    slug = models.SlugField (max_length=10, db_index=True, unique=True)
    image = models.ImageField (blank=True, error_messages={TypeError: "image did not saved"})
    description = models.TextField (blank=True, null=True)
    price = models.DecimalField (max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField (db_index=True)
    available = models.BooleanField (default=True)
    created = models.DateTimeField (auto_now_add=True)
    updated = models.DateTimeField (auto_now=True)
    salestate = models.ForeignKey (Product_Sale_State, on_delete=models.DO_NOTHING, null=True, blank=True, max_length=5)
    sell_stock = models.PositiveIntegerField (db_index=True)
    vat = models.PositiveIntegerField (default=0)
    off = models.ForeignKey (ProductOff, on_delete=models.DO_NOTHING, null=True, blank=True)
    box = models.PositiveIntegerField (default=1)
    echantion = models.ForeignKey (ProductEchantion, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        ordering = (['price'])
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class them (models.Model):
    image = models.ImageField (blank=True, error_messages={TypeError: "image did not saved"})
    title = models.CharField (blank=True, null=True, max_length=10)
    description = models.TextField (blank=True, null=True)

    def __str__(self):
        return self.title

from accountside.models import accountside
class WareHouseDefinde (models.Model):
    code = models.PositiveIntegerField (unique=True)
    name = models.CharField (max_length=30)
    accountside = models.ForeignKey(accountside,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


from cart.models import OrderItem,OrderItemBackup
from decimal import Decimal as D


class Inventory (models.Model):
    product = models.ForeignKey (Product, on_delete=models.DO_NOTHING)
    warehouse = models.ForeignKey (WareHouseDefinde, on_delete=models.CASCADE)
    sell_stock = models.PositiveIntegerField ( )
    stock = models.PositiveIntegerField ( )
    unique_together = ['product', 'warehouse']

    def average_buy_price(self):
        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=1,
                                          order__warhouse=self.warehouse,
                                          order__checked_out=True)
        items_back = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=3,
                                          order__warhouse=self.warehouse,
                                          order__checked_out=True)

        multiple_quantity_price = 0
        quantity = 0
        for item in items:
            multiple_quantity_price += float(item.total_price)
            quantity += float(item.quantity)

        multiple_quantity_price_back = 0
        quantity_back = 0
        for item in items_back:
            multiple_quantity_price_back += float(item.total_price)
            quantity_back += float(item.quantity)

        if len (items) != 0 or len(items_back) != 0 :
            return (multiple_quantity_price - multiple_quantity_price_back) / (quantity - quantity_back)
        else:
            return 0



    average_buy_price = property (average_buy_price)

    def buy_quantity(self):
        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=1,
                                          order__warhouse=self.warehouse,
                                          order__checked_out=True)

        quantity = 0
        for item in items:
            quantity += item.quantity

        return quantity

    buy_quantity= property(buy_quantity)

    def sell_order_quantity(self):

        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=2,
                                          order__warhouse=self.warehouse,
                                          order__checked_out_2=False,
                                          )

        quantity = 0
        for item in items:
            if item.order.shipment:
                if  item.order.shipment.checked_out_2 == False:
                    quantity += item.quantity
            else:
                quantity += item.quantity
        return quantity

    sell_order_quantity=property(sell_order_quantity)

    def finalize_sell_quantity(self):
        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=2,
                                          order__warhouse=self.warehouse,
                                          order__checked_out_2=True
                                          )
        quantity = 0
        for item in items:
            quantity += item.quantity

        return quantity

    finalize_sell_quantity=property(finalize_sell_quantity)

    def sell_back_quantity(self):
        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=4,
                                          order__warhouse=self.warehouse,
                                          order__checked_out=True
                                          )
        quantity = 0
        for item in items:
            quantity += item.quantity

        return quantity

    sell_back_quantity=property(sell_back_quantity)

    def buy_back_quantity(self):

        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=3,
                                          order__warhouse=self.warehouse,
                                          order__checked_out=True
                                          )
        quantity = 0
        for item in items:
            quantity += item.quantity

        return quantity
    buy_back_quantity=property(buy_back_quantity)
    def product_cartex(self):
        items = OrderItem.objects.filter (
            product=self.product,
            order__warhouse=self.warehouse,
            order__checked_out=True,
            order__checked_out_2=True,
        ).order_by ("order__creation_date")

        return items

    def sended(self):
        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=2,
                                          order__checked_out=True,
                                          order__checked_out_2=False,
                                          order__warhouse=self.warehouse,
                                          order__shipment__checked_out=True,
                                          order__shipment__checked_out_2=True,
                                          order__shipment__checked_out_5=False,
                                          )

        quantity = 0
        for item in items:
            quantity += item.quantity

        return quantity
    sended= property(sended)

    def order_back_quantity(self):
        items = OrderItem.objects.filter (product=self.product,
                                          order__orderkinde_id=6,
                                          order__warhouse=self.warehouse,
                                          )
        quantity = 0
        for item in items:
            quantity += item.quantity

        return quantity

    order_back_quantity=property(order_back_quantity)


    def test_stock(self):

        stock = self.buy_quantity+self.sell_back_quantity-self.finalize_sell_quantity-self.buy_back_quantity-self.sended
        return stock

    test_stock= property(test_stock)

    def exit_quantity(self):

        items = OrderItemBackup.objects.filter(product=self.product,order__warhouse=self.warehouse)

        quantity = 0
        for item in items:
            quantity += item.quantity
        return quantity

    exit_quantity = property(exit_quantity)

    def returned(self):

        quantity = self.exit_quantity-self.sended-self.finalize_sell_quantity

        return quantity

    returned = property(returned)











def __str__(self):
    return f'{self.product} in {self.warehouse}'
