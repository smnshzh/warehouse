from django.urls import path
from . import views

urlpatterns = [


    path('shipments-overall',views.shipment_overall, name = 'shipment_overall'),
    path("R&S-shipments",views.recieve_and_send_shipments,name = "recieve_and_send_shipments"),
    path('shipment-items<int:id>',views.shipment_items,name = "shipment_items"),
    path('shipment-items-back<int:id>',views.print_shipment_items_back,name = "print_shipment_items-back"),
    path('confirm-shipment-items-back<int:id>',views.confirm_shipment_items_back,name = "confirm_shipment_items-back"),
    path('shipment-view',views.deliver_shipment_view,name = "deliver_shipment_view"),
    path('sended-shipment',views.cancle_sending,name = "cancle_sending"),
    path('deliver-confirm-shipment-<int:id>',views.deliver_confirm_shipment,name = "deliver_confirm_shipment"),

    path('report/sended-orders-report',views.sell_sended_order_report,name = "sell_sended_order_report"),
    path('ready-acoounting-shipments',views.show_shipments_ready_for_accounting,name = "show_shipments_ready_for_accounting"),
    path('accounting-shipment-<int:id>',views.accounting_shipment,name = "accounting_shipment"),
    path('invoices-report',views.invoices_report,name = 'invoices_report'),
    path('sold-product-report',views.invoices_product_report,name = "invoices_product_report"),
    path('shipment-settle-report-<int:id>',views.settletd_shipment_report,name = "settletd_shipment_report"),
    path('chart',views.chart,name="chart")
]
