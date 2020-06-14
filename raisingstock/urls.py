from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework import routers


urlpatterns = [
    path('Confirm-Buy-Order-By-Warhouse',views.warehouse_confirm_buy_order,name = 'warehouse_confirm_buy_order'),
    path('Confirm-Buy-Order-By-Warhouse/<int:id>',views.warehouse_confirm_buy_order,name = 'warehouse_confirm_buy_order_by_id'),
    path("warehouse-confirm-buy-back",views.warehouse_confirm_buy_back,name ="warehouse_confirm_buy_back" ),
    path('deleteBuyOrder',views.delete_buy_order, name = "delete_buy_order"),
    path("buy-invoice",views.show_confirmed_buy,name ="show_confirmed_buy" ),
    path("deconfirm-buy-order/<int:id>",views.deconfirm_buy_order,name = "deconfirm"),
    path("warehouse-deconfirm-buy-back/<int:id>",views.deconfirm_buy_back,name = "deconfirm_buy_back"),
]