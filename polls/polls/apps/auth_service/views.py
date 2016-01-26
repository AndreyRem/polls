from django.shortcuts import render, redirect
from django.contrib import auth
from polls.apps.auth_service.forms import LoginForm, UserCreationForm


def login(request):
    args = dict()
    args['form'] = LoginForm()

    if request.POST:
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(email=user_form.cleaned_data['email'],
                                     password=user_form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                args['login_error'] = 'User is not found'
                return render(request, 'login.html', args)
        else:
            args['login_error'] = 'User is not found'
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    args = dict()
    args['form'] = UserCreationForm()
    if request.POST:
        new_user_form = UserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            new_user_form = auth.authenticate(email=new_user_form.cleaned_data['email'], password=new_user_form.cleaned_data['password2'])
            auth.login(request, new_user_form)
            return redirect('/')
        else:
            args['form'] = new_user_form
    return render(request, 'registration.html', args)