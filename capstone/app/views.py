"""
Definition of views.
"""

from datetime import datetime
from urllib.error import HTTPError
from django.shortcuts import render, redirect
from .forms import NewUserForm, YelpForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .API.YelpAPI.yelp import yelp_main, query_api
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'app/index.html')

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Application description page.',
            'year':datetime.now().year,
        }
    )

def foodie(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/foodie.html',
        {
            'title':'Foodie Page',
            'year':datetime.now().year,
        }
    )

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'app/login.html', {})

@csrf_exempt
def yelping(request):
    if request.method == "POST":
        form = YelpForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False)
            term = request.POST['term']
            location = request.POST['location']
            form.save()
            print("yelping", term, location)
            yelp_main(request, term, location)
            messages.success(request, "Search successful." )
            return render(request, 'app/yelp.html', {'form' : form})
        else:
            form = YelpForm()
        messages.error(request, "Unsuccessful Search. Invalid information.")
        form = YelpForm()
        
    assert isinstance(request, HttpRequest)
    return render(request, 'app/yelp.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("app:login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="app/registration.html", context={"register_form":form})