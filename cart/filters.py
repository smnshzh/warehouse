import django_filters
from django import forms
from .models import *
from Shop.models import *


class order_filter (django_filters.FilterSet):
    CHOISE_PRODUCT = [item.name for item in Product.objects.all ( )]

    start_date = django_filters.DateFilter (field_name='order__creation_date', lookup_expr='gte',
                                            widget=forms.TextInput (attrs={
                                                'placeholder': 'Start Date', 'class': 'input-group-text',
                                                'type': 'date'}),
                                            label='')
    end_date = django_filters.DateFilter (field_name='order__creation_date', lookup_expr='lte',
                                          widget=forms.TextInput (attrs={
                                              'placeholder': 'End Date', 'class': 'input-group-text', 'type': 'date'}),
                                          label='')
    user = django_filters.CharFilter (field_name='user', lookup_expr='icontains', widget=forms.TextInput (attrs={
        'class': 'input-group-text', 'placeholder': 'Seller'}),
                                      label='')

    class Meta:
        model = OrderItem
        fields = []
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateField,
                }
            }}


class product_filter (django_filters.FilterSet):
    name = django_filters.CharFilter (field_name='name', lookup_expr='icontains', widget=forms.TextInput (attrs={
        'placeholder': 'Product Name', 'class': 'input-group-text', 'type': 'Text'}), label='')
    category = django_filters.ChoiceFilter (field_name='category',
                                            choices=[(i.id, i.name) for i in SubCategory.objects.all ( )],
                                            )


class Meta:
    model = Product
    fields = []
    filter_overrides = {
        models.ImageField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_expr': 'icontains',
            }}}
