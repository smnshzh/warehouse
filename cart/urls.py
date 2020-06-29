from django.urls import path,include
from . import views
from rest_framework import routers



urlpatterns = [
    path('sell',views.sell,name='sell'),
    path('sellview',views.modify_sell_view,name='modify_sell_view'),
    path('order/<int:id>',views.show_order_items,name='show_order_items'),
    # start sell back fumctions =============End of sell fumctions
    path('new-sell-back-order',views.new_sell_back_order,name = 'new_sell_back_order'),
    path("show-sell-back-orders",views.show_sell_back_orders,name = "show_sell_back_orders"),

    # start buy fumctions =============End of sell back fumctions
    path('new-buy-Order',views.new_buy_order,name='new_buy_order'),
    path("show-buy-orders",views.show_buy_orders,name = "show_buy_orders"),
    path("show-Buy-Order-items/<int:id>",views.show_buy_order_items,name = "show_buy_order_items"),
    # start buy-back fumctions =============End of Buy functions
    path("new-buy-back",views.buy_back,name = "buy_back"),
    path("show-buy-back-orders",views.show_buy_back,name ="show_buy_back" ),
    path('order/delete/<int:order_id>',views.remove_order,name='remove_order'),
    path('send-for-supply-chain-managment/<int:order_id>',views.send_for_scm,name='send_for_scm'),
    #========= Start Shipment Functions ===================================
    path('make-shipment',views.make_shipment, name = 'make_shipment'),
    path('shipment-orders/<int:id>',views.show_shipment_orders,name='show_shipment_orders'),
    path('edit-shipment-<int:id>',views.edit_shipment,name = "edit_shipment"),
    path('delivery-edit-<int:id>',views.delivery_function_on_order_items,name = "delivery_function_on_order_items"),
    path('static-sell-view-<int:id>',views.static_sell_veiw,name = "static_sell_veiw"),
    #===============start settlment =============================
    path('order-settlment-<int:id>',views.settle_order,name = "settle_order"),
    path('date',views.date_to,name = "date_to")

         ]