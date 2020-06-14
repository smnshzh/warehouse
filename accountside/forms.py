from django import forms
from .models import *
from cart.models import Order



class accountside_form (forms.ModelForm):
    class Meta:
        model = accountside
        fields = '__all__'

    def clean(self, *args, **kwargs):
        return super (accountside_form, self).clean (*args, **kwargs)


class BoxForm (forms.Form):
    CHOICES = [(item.id, item.name) for item in accountside.objects.filter (kind__id=5)]

    Box = forms.TypedChoiceField (choices=CHOICES)

