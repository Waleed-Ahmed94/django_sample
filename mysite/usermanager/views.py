# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import PollUser
# Create your views here.

def home(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'usermanager/home.html', {'username': username})
    else:
        return render(request, 'usermanager/home.html')

def login_page(request):
    return render(request, 'usermanager/login.html')

def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            User = PollUser.objects.get(username=username)
        except (KeyError, PollUser.DoesNotExist):
            return render(request, 'usermanager/login.html', {'errormessage': 'User Does not exist'})
        else:
            if User.password != password:
                return render(request, 'usermanager/login.html', {'errormessage': 'username and password do not match'})
            else:
                request.session['username'] = User.username
                request.session['userid'] = User.id
                return HttpResponseRedirect(reverse('usermanager:home'))
    else:
        return render(request, 'usermanager/home.html')




def signup(request):
    return render(request, 'usermanager/signup.html')

def create_user(request):
    if request.method == "POST":
        username = request.POST['username']
        user = PollUser.objects.filter(username=username)
        if user:
            return render(request, 'usermanager/signup.html', {'errormessage' : "username already exists"})

        elif request.POST['password'] != request.POST['confirm-password']:
            return render(request, 'usermanager/signup.html', {'errormessage': "password does not match"})

        else:
            User = PollUser()
            User.username = request.POST['username']
            User.password = request.POST['password']
            User.save()
            return HttpResponseRedirect(reverse('usermanager:login_page'))

    else:
        return render(request, 'usermanager/home.html')

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'usermanager/home.html')
