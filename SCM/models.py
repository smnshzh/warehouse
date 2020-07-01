from django.contrib.auth.models import User

from Shop.models import WareHouseDefinde
from cart.models import *


class ComeForDelivery (models.Model):
    coming_date = models.DateTimeField (auto_now_add=True)
    order_number = models.ForeignKey (Order, on_delete=models.DO_NOTHING, blank=True, null=True)
    user_modifier = models.CharField (max_length=35)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Delivery Management'


class WarehouseInvoiceNumber (models.Model):
    shipment = models.ForeignKey (Shipment, null=True, blank=True, on_delete=models.CASCADE, unique=True)
    order = models.ForeignKey (Order, null=True, blank=True, on_delete=models.CASCADE, unique=True)
    code = models.PositiveIntegerField ( )
    warehouse = models.ForeignKey (WareHouseDefinde, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField (null=True, blank=True)


class WarehouseInvoiceItems (models.Model):
    invoice_number = models.ForeignKey (WarehouseInvoiceNumber, on_delete=models.CASCADE)
    product = models.ForeignKey (Product, on_delete=models.CASCADE)
    input_quantity = models.PositiveIntegerField (default=0)
    output_quantity = models.PositiveIntegerField (default=0)
