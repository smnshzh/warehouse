from django.urls import path

from . import views

urlpatterns = [

    path ('login', views.logIn, name='login'),
    path ('signup', views.register, name='signup'),
    path ('edit-user-<int:id>', views.register, name="edit_user"),
    path ('logout', views.out, name='logout'),
    path ('access-definer', views.access_definer, name="access_definer"),
    path ('edit-access-<int:id>', views.access_definer, name="edit_access")

]
