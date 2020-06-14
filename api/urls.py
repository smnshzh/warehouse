from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'group',views.group_serilize_view)
router.register(r'users',views.user_serilize_view)
router.register(r'firstcat', views.firstcat_serilize_view)
router.register(r'subcat', views.subcat_serilize_view)
router.register(r'state', views.productsalestate_serilize_view)
router.register(r'productoff', views.producyoff_serilize_view)
router.register(r'product', views.product_serilize_view)
router.register(r'localid',views.localid_serilize_view)
router.register(r'kind',views.kind_serilize_view)
router.register(r'accountside', views.accountsid_serilize_view)
router.register(r'definitAccount', views.difinit_account_serilizer_view)
router.register(r'orderitems' ,views.order_item_serializer)
router.register(r'order',views.order_serilizer_view)
router.register(r'shipment',views.shipment_serilizer_view)
router.register(r'buyOrder',views.buyorder_serilizer_view)
router.register(r'buyOrderItems',views.buyorderitems_serilizer_view)
router.register(r'warehouse',views.warehouse_difinder_serilizer_view)
router.register(r'inventory',views.inventory_serilizer_view)
router.register(r'access',views.access_serilizer_view)




urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]

