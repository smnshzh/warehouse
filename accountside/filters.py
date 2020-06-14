import django_filters
from django import forms
from .models import *
from Shop.models import *


class accountside_filter(django_filters.FilterSet):

    class Meta:
        model=accountside
        fields={
            'name':['icontains'],
            'telephonnumber':['exact'],
            'address':['icontains'],
            'id_code':['exact']
        }
