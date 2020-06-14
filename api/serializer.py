from rest_framework import serializers
from cart.models import *
from Shop.models import *
from SCM.models import *
from raisingstock.models import *
from django.contrib.auth.models import User,Group
from UserControl.models import *


class GropSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["name",]


class UserSerilizer(serializers.HyperlinkedModelSerializer):
    groups = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'username','first_name','last_name','groups']


class FirstCatSerilizer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FirstCategory
        fields =['id','name','slug','url',]
class SubCatSerilizer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductSaleStateSerilizer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product_Sale_State
        fields = '__all__'


class ProductOffSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductOff
        fields = '__all__'

class ProductSerilizer(serializers.HyperlinkedModelSerializer):

    off = serializers.CharField()

    class Meta:
        model = Product
        fields = ['id','name','price','stock','sell_stock','box','vat','off']



#+================== End Of ShopApp =============================
class LocalSerilizer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = local_id_def
        fields = '__all__'

class KindSerilizer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = kind
        fields = ["id","type_code","type_name"]


class AccountsideSerilizer(serializers.HyperlinkedModelSerializer):
    region_city = serializers.CharField(source='region.city')
    region_local_name = serializers.CharField(source='region.local_name')
    kind = KindSerilizer(read_only=True, many=True)

    class Meta:
        model = accountside
        fields = ['id','name','id_code','telephonnumber','region_city','region_local_name','address','credit','kind']

class DifinitAccountsSerilizer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = DifinitAccounts
        fields = ['name','code',]

#======================End of Accountside App=====================

class OrderSerilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

class ShipmentSerilizer(serializers.HyperlinkedModelSerializer):



    class Meta:
        model=Shipment
        fields='__all__'

class OrderItemSerilizer(serializers.HyperlinkedModelSerializer):
    order_id = serializers.CharField(source='order.id')
    shipment_id = serializers.CharField (source='order.shipment')


    class Meta:
        model=OrderItem
        fields=['id','order_id','shipment_id','total_price']



#======================End of cart App=====================

class ComeForDeliverySerilizer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=ComeForDelivery
        fields='__all__'


class BuyOrderSerilizer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model= buyOrder
        fields='__all__'

class BuyOrderItemsSerilizer(serializers.HyperlinkedModelSerializer):

    buyorder_creation_date = serializers.DateTimeField(source='buyorder.creation_date')

    class Meta:
        model=buyOrder_items
        fields = ['id','buyorder','buyorder_creation_date','object_id','quantity','unit_price','total_price']

class WareHouseDefindeSerilizer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = WareHouseDefinde
        fields = ['id','name','code']


class InventorySerilizer (serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Inventory
        fields = "__all__"


#====================== End Of Raising Stock App ==============================


class AccessSerilizer (serializers.HyperlinkedModelSerializer):

    user_username = serializers.CharField(source='user.username')
    warehouse = serializers.StringRelatedField(many=True)

    class Meta:
        model = Access
        fields = ['user_username','warehouse']