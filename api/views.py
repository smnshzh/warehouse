from rest_framework import viewsets
from api.serializer import *
from Shop.models import *
from cart.models import *
from accountside.models import *
from SCM.models import * 


class group_serilize_view (viewsets.ModelViewSet):
    queryset = Group.objects.all ( ).order_by ('id')
    serializer_class = GropSerilizer

class user_serilize_view (viewsets.ModelViewSet):
    queryset = User.objects.all ( ).order_by ('id')
    serializer_class = UserSerilizer

class firstcat_serilize_view (viewsets.ModelViewSet):
    queryset = FirstCategory.objects.all ( ).order_by ('id')
    serializer_class = FirstCatSerilizer

class subcat_serilize_view (viewsets.ModelViewSet):
    queryset = SubCategory.objects.all ( ).order_by ('id')
    serializer_class = SubCatSerilizer


class productsalestate_serilize_view (viewsets.ModelViewSet):
    queryset = Product_Sale_State.objects.all ( ).order_by ('id')
    serializer_class = ProductSaleStateSerilizer


class producyoff_serilize_view (viewsets.ModelViewSet):
    queryset = ProductOff.objects.all ( ).order_by ('id')
    serializer_class = ProductOffSerilizer


class product_serilize_view (viewsets.ModelViewSet):
    queryset = Product.objects.all ( ).order_by ('id')
    serializer_class = ProductSerilizer

#-------------------------End of shopApp----------------------


class localid_serilize_view (viewsets.ModelViewSet):
    queryset = local_id_def.objects.all ( ).order_by ('id')
    serializer_class = LocalSerilizer

class kind_serilize_view (viewsets.ModelViewSet):
    queryset = kind.objects.all ( ).order_by ('id')
    serializer_class = KindSerilizer



class accountsid_serilize_view (viewsets.ModelViewSet):
    queryset = accountside.objects.all ( ).order_by ('id')
    serializer_class = AccountsideSerilizer


class difinit_account_serilizer_view(viewsets.ModelViewSet):
    queryset = DifinitAccounts.objects.all ( ).order_by ('id')
    serializer_class = DifinitAccountsSerilizer

#-------------------------End of accountsideApp----------------------

class order_serilizer_view(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerilizer

class shipment_serilizer_view(viewsets.ModelViewSet):
    queryset = Shipment.objects.all ( ).order_by ('id')
    serializer_class = ShipmentSerilizer


#-------------------------End of cartApp----------------------

class order_item_serializer (viewsets.ModelViewSet):
    queryset = OrderItem.objects.all ( ).order_by ('id')
    serializer_class = OrderItemSerilizer

class comefordelivery_serilizer_view(viewsets.ModelViewSet):
    queryset = ComeForDelivery.objects.all().order_by('id')
    serializer_class = ComeForDeliverySerilizer

class buyorder_serilizer_view(viewsets.ModelViewSet):
    queryset = buyOrder.objects.all().order_by('id')
    serializer_class = BuyOrderSerilizer

class buyorderitems_serilizer_view(viewsets.ModelViewSet):
    queryset = buyOrder_items.objects.all().order_by('id')
    serializer_class = BuyOrderItemsSerilizer

class warehouse_difinder_serilizer_view(viewsets.ModelViewSet):
    queryset = WareHouseDefinde.objects.all().order_by('id')
    serializer_class = WareHouseDefindeSerilizer

class inventory_serilizer_view(viewsets.ModelViewSet):
    queryset = Inventory.objects.all().order_by('id')
    serializer_class = InventorySerilizer


class access_serilizer_view(viewsets.ModelViewSet):
    queryset = Access.objects.all().order_by('id')
    serializer_class = AccessSerilizer