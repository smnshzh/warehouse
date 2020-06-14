from django.urls import path
from . import views

urlpatterns=[

    path('login',views.logIn,name='login'),
    path('signup',views.register,name='signup'),
    path('logout',views.out,name='logout'),

    ]