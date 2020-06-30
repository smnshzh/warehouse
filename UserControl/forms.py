from django import forms
from django.contrib.auth import (authenticate
, get_user_model)

from .models import *

User = get_user_model ( )


class UserLoginForms (forms.Form):
    username = forms.CharField (max_length=255, widget=forms.TextInput (attrs={'class': 'form-control'}))
    password = forms.CharField (max_length=255, widget=forms.PasswordInput (attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get ('username')
        password = self.cleaned_data.get ('password')
        if username and password:
            user = authenticate (username=username, password=password)
            if not user:
                raise forms.ValidationError ("Username or Password Not Valid")
            if not user.check_password (password):
                raise forms.ValidationError ("password is not correct")
            if not user.is_active:
                raise forms.ValidationError ("This user does not exist")
        return super (UserLoginForms, self).clean (*args, **kwargs)


class UserRegisterForm (forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'groups',
            'password',

        ]

    first_name = forms.CharField (max_length=25, label='First Name')
    last_name = forms.CharField (max_length=25, label='Last Name')
    username = forms.CharField (max_length=10, label='User Name')
    email = forms.CharField (max_length=25, label='E-Mail')
    password = forms.CharField (widget=forms.PasswordInput)
    ConfirmPassword = forms.CharField (widget=forms.PasswordInput, label='Confirm Password')

    def clean(self, *args, **kwargs):

        email = self.cleaned_data.get ('email')
        pass1 = self.cleaned_data.get ('password')
        pass2 = self.cleaned_data.get ('ConfirmPassword')

        email_qs = User.objects.filter (email=email)
        if email_qs:
            raise forms.ValidationError ("This E-Mail has been registered before")
        if pass1 != pass2:
            raise forms.ValidationError ("Passwords are not Identical")

        return super (UserRegisterForm, self).clean (*args, **kwargs)



class Disrobuter(forms.Form):
    CHOICES = [(item.id , f"{item.first_name} {item.last_name}")for item in User.objects.filter(groups = 2) ]

    Distrobuter = forms.TypedChoiceField(choices= CHOICES)


class AccessForm (forms.ModelForm):
    class Meta:
        model = Access
        fields = "__all__"
        exclude = ["user", ]
