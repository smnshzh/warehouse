from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


def accsees_for_all (request):
    user = request.user
    if user.is_authenticated:
        return {"all_access": Access.objects.get(user=user) }
    else:
        return {"all_access": Access.objects.get (user=1)}
