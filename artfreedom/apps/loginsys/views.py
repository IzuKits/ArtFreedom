from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages

import re
from main.models import User_data

#from django.core.context_processors import csrf


def registration(request):
    template = "main/register.html"
    if request.POST:
        print(request.POST['login'])
        form = UserRegistrationForm(request.POST)
        if form.is_valid() :
            print("form is valid")
            user = User(username=form.cleaned_data['login'])
            user.set_password(form.cleaned_data['password2'])
            user.save()
            userdata = User_data(user=user, contacts=form.cleaned_data['contact'])
            userdata.save()

        else:
            messages.error(request, "Ошибка регистрации. Проверьте введенные дынные")
            HttpResponseRedirect("/registration/", status=422)
        
        messages.add_message(request, messages.SUCCESS, 'Регистрация прошла успешно')
        return HttpResponseRedirect("/login/", )
    else:
        form = UserRegistrationForm()
        return render(request, "loginsys/register.html", {'form': form})



def login(request):
    args = {}
    #args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/profile/")
        else:
            args['login_error'] = "Неверный логин или пароль"
            return render(request, 'loginsys/login.html', args)
    else:
        return render(request, "loginsys/login.html", args)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

class UserRegistrationForm(forms.Form):
    login = forms.CharField(label="Логин", max_length=50)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    contact = forms.CharField(label='Контакты', max_length=200)

    def clean_password2(self):
        print("clean_password2")
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не одинаковые')
        return cd['password2']
    
    def clean_login(self):
        print("clean_login")

        s = self.cleaned_data['login']
        a = re.match("^[\da-zA-Z0-9]+$", s)
        if a:
            return s
        else:
            raise forms.ValidationError('Лишние знаки')



    def is_digit_and_lowercase_only(s): 
        return re.match("^[\da-zA-Z0-9]+$", s)

