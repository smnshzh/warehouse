from django import forms
from .models import *
from Shop.models import *


PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,999)]
CUSTOMER_LIST=[(i.id,i.name) for i in accountside.objects.all()]
PRODUCT_LIST=  [(i.id,i.name) for i in Product.objects.all()]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,widget=forms.TextInput(attrs={'class': 'quantity-input'}),label='',
                                      required=False)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)



class OrderAddProductFrom(forms.ModelForm):
    class Meta:
        model=OrderItem
        fields='__all__'


class SendToWarehouseForm (forms.Form):

     select_for_scm=forms.BooleanField(label='', required=False,widget=forms.CheckboxInput)



class customer(forms.Form):
    custumer = forms.TypedChoiceField (choices=CUSTOMER_LIST)



class new_order(forms.Form):


    product=forms.TypedChoiceField(choices=PRODUCT_LIST)
    quantity = forms.TypedChoiceField (choices=PRODUCT_QUANTITY_CHOICES,
                                       coerce=int, widget=forms.TextInput (attrs={'class': 'quantity-input'}),
                                       required=True)
from django import forms
from .models import *
from Shop.models import *


PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,999)]
CUSTOMER_LIST=[(i.id,i.name) for i in accountside.objects.all()]
PRODUCT_LIST=  [(i.id,i.name) for i in Product.objects.all()]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,widget=forms.TextInput(attrs={'class': 'quantity-input'}),label='',
                                      required=False)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)



class OrderAddProductFrom(forms.ModelForm):
    class Meta:
        model=OrderItem
        fields='__all__'


class SendToWarehouseForm (forms.Form):

     select_for_scm=forms.BooleanField(label='', required=False,widget=forms.CheckboxInput)



class customer(forms.Form):
    custumer = forms.TypedChoiceField (choices=CUSTOMER_LIST)



class new_order(forms.Form):


    product=forms.TypedChoiceField(choices=PRODUCT_LIST)
    quantity = forms.TypedChoiceField (choices=PRODUCT_QUANTITY_CHOICES,
                                       coerce=int, widget=forms.TextInput (attrs={'class': 'quantity-input'}),
                                       required=True)
