from django.urls import path

from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path ('product/<int:id>', views.product_detail, name='productDetail'),
    path ('category/<str:sub>', views.sub_category, name='subcategory'),
    path ('random', views.randomData),
    path ("products", views.product_views, name="product_views"),
    path("autoInventory",views.auto_inventory_maker,name = "auto_inventory_maker"),

]
