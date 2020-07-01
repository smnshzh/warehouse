from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from .decorators import *
from .forms import *


def logIn(request):
    next = request.GET.get ('next')
    form = UserLoginForms (request.POST or None)
    if form.is_valid ( ):
        username = form.cleaned_data.get ('username')
        password = form.cleaned_data.get ('password')
        user = authenticate (username=username, password=password)

        login (request, user)
        if next:
            return redirect (next)
        return redirect ('index')
    context = {
        'form': form,
        'button': "LOG IN",
        'action': 'login'
    }
    return render (request, 'login.html', context)


@can_register
def register(request, id=None):
    # print(request.user.is_authenticated())
    form = UserRegisterForm (request.POST or None)
    all_access = Access.objects.all ( )
    username = None
    if id != None:
        username = User.objects.get (id=id)
        form = UserEditForm (instance=username)
    if request.method == 'POST' and username:
        form = UserEditForm (request.POST, instance=username)
        form.save ( )

    if request.method == 'POST' and id == None:
        if form.is_valid ( ):
            user = form.save (commit=False)
            password = form.cleaned_data.get ('password')
            positions = form.cleaned_data.get ('groups')
            user.set_password (password)
            user.save ( )
            for position in positions:
                user.groups.add (position)
            Access.objects.create (user=user)
            message = messages.success (request, f"{user.username} was made successfully")
            return redirect ("signup")
        else:
            message = messages.warning (request, "form is not valid")

    context = {
        'form': form,
        "accesses": all_access,
        "username": username,

    }
    return render (request, 'signup.html', context)


def out(request):
    logout (request)
    return redirect ('login')


def access_definer(request, id=None):
    form = AccessForm (request.POST or None)
    all_access = Access.objects.all ( )
    username = None
    if id != None:
        get_user_access = Access.objects.get (id=id)
        form = AccessForm (instance=get_user_access)
        username = get_user_access.user.username
    if request.POST and id != None:
        get_user_access = Access.objects.get (id=id)
        form = AccessForm (request.POST, instance=get_user_access)
        form.save ( )
    context = {
        "accesses": all_access,
        "form": form,
        "username": username

    }
    return render (request, 'form.html', context)
