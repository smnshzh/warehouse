from django.urls import path, include
from . import views

urlpatterns = [
    path ('new-account', views.new_account, name='new_account'),
    path ("accountsides-show", views.accountside_show, name='accountside_show'),
    path ('random', views.random_maker),
    path ('auto-Journal', views.making_all_journal, name="auto_journal"),
    path ('show-Journal', views.show_journals, name="show_journals"),
    path ('making-Journal', views.making_journal, name="making_journal"),
    path('bank-pose',views.define_bank_pose,name = "define_bank_pose"),
    path('settle-invoice',views.settle_invoice,name = "settle_invoice" ),
    path('confirm-settel',views.confirm_settelmenet,name ="confirm_settelmenet" ),
    path("map",views.my_map,name ='map')
]
