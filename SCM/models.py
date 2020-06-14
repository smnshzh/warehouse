
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from cart.models import *


class ComeForDelivery(models.Model):

    coming_date= models.DateTimeField (auto_now_add=True)
    order_number= models.ForeignKey(Order,on_delete=models.DO_NOTHING , blank=True,null=True)
    user_modifier=models.CharField(max_length=35)
    class Meta:
        ordering = ('id',)
        verbose_name = 'Delivery Management'



