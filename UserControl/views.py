from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, get_user_model, login, logout
 
# Create your views here.
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


def register(request):
    # print(request.user.is_authenticated())
    form = UserRegisterForm (request.POST or None)
    if request.method == 'POST':

        if form.is_valid ( ):
            user = form.save (commit=False)
            password = form.cleaned_data.get ('password')
            user.set_password (password)
            user.save ( )
            new_user = authenticate (username=user.username, password=password)
            login (request, new_user)
            return redirect ("index")

    context = {
        'form': form,

    }
    return render (request, 'signup.html', context)


def out(request):
    logout (request)
    return redirect ('login')

