from django.shortcuts import render
from .models import *


def accsees_for_all (request):
    return {"all_access": AccsessTo.objects.all()}