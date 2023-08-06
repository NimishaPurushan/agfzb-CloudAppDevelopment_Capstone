from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import DealerReview, CarModel
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_login.html', context)
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:login')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        try:
            User.objects.get(username)
            print("user already exits")
            context['message'] = "User already exists."
            return redirect('djangoapp:login')
        except:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect('djangoapp:index')

            
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/9103f29e-2898-4270-84f4-08bd82ed47c0/dealership_package/get-dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {}
        # Concat all dealer's short name
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)
    
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/9103f29e-2898-4270-84f4-08bd82ed47c0/dealership_package/get-review.json"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url,dealerId=dealer_id)
        context = {}
        context["reviews"] = reviews
        dealer_url = "https://us-east.functions.appdomain.cloud/api/v1/web/9103f29e-2898-4270-84f4-08bd82ed47c0/dealership_package/get-dealerships"
        dealer = get_dealer_from_cf_by_id(dealer_url, dealer_id)
        print(dealer)
        context["dealer"] = dealer.full_name
        return render(request, 'djangoapp/dealer_details.html', context)
    
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/9103f29e-2898-4270-84f4-08bd82ed47c0/dealership_package/get-dealerships"
        dealer = get_dealer_from_cf_by_id(url, dealer_id)
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"] = cars
        context["dealer"] = dealer
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST": 
        url="https://us-east.functions.appdomain.cloud/api/v1/web/9103f29e-2898-4270-84f4-08bd82ed47c0/dealership_package/post-review"
    
        if 'purchasecheck' in request.POST:
            was_purchased = True
        else:
            was_purchased = False
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        print(request.POST)
        for car in cars:
            print(car.model_id)
            if car.model_id == int(request.POST['car']):
                review_car = car  
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.POST['name']
        review["dealership"] = dealer_id
        review["review"] = request.POST['content']
        review["purchase"] = was_purchased
        review["purchase_date"] = request.POST['purchasedate']
        review["car_make"] = review_car.make.name
        review["car_model"] = review_car.name
        review["car_year"] = review_car.year.strftime("%Y")
        json_payload = {}
        json_payload["review"] = review
        response = post_request(url, json_payload)
        print(response)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    
