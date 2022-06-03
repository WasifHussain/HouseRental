import re
from django.shortcuts import render,redirect
import imp,math
import pandas as pd
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import House,Review
from .forms import HouseForm,UploadForm,ReviewForm

from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, "index.html")

def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/index')

    return render(request, 'signup.html', {'form': form})

def signin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password'])
            login(request, user)
            return redirect('/houses/page/1')

    return render(request, 'signin.html', {'form': form})
def signout(request):
    logout(request)
    return redirect('/index')

def post_house(request):
    form = HouseForm()
    if request.method == "POST":
        house_form = HouseForm(request.POST, request.FILES)

        if house_form.is_valid():
            house_form.save()
            return redirect('/houses/page/1')
    return render(request, 'post_house.html',{'form':form})

def get_houses(request, page_number):
    page_size = 12

    if page_number < 1:
        page_number = 1

    house_count =  House.objects.count()

    last_page = math.ceil(house_count/page_size)

    pagination = {
        'previous_page': page_number - 1,
        'current_page': page_number,  
        'next_page': page_number + 1,
        'last_page': last_page
    }
    houses = House.objects.all()[(page_number-1)
                                 * page_size:page_number*page_size]
    return render(request,'houses.html',{'houses':houses, 'pagination': pagination})

def add_to_favorite(request, id):
    house = House.objects.get(id=id)
    house.favorite.add(request.user)

    return redirect('/house/{0}'.format(id))

def remove_from_favorites(request, id):
    house = House.objects.get(id=id)
    house.favorite.remove(request.user)

    return redirect('/house/{0}'.format(id))

def get_user_favorites(request):
    houses = request.user.favorite.all()
    return render(request, 'user_favorite.html', {'houses': houses})


def  get_house_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/signin')
    try:
        review_form = ReviewForm()
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.house_id = id
                review.user_id = request.user.id
                review.save()

        house = House.objects.get(id=id)
        reviews = Review.objects.filter(house=house).order_by('-created_at')[0:4]
        context = {
                'is_favorite': False
        }

        if house.favorite.filter(pk=request.user.pk).exists():
            context['is_favorite'] = True
        return render(request,"house.html",{'house':house,'context':context,'reviews':reviews,'review_form':review_form})
    except House.DoesNotExist:
        return render(request,'404.html')

def upload_dataset(request):
    file_form = UploadForm()
    error_messages = {}

    if request.method == "POST":
        file_form = UploadForm(request.POST, request.FILES)
        try:
            if file_form.is_valid():
                dataset = pd.read_csv(request.FILES['file'])
                new_houses_list = []
                with transaction.atomic():
                    for index, row in dataset.iterrows():
                        house = House(
                            houseName=row['houseName'],
                            ownerName=row['ownerName'],
                            address=row['address'],
                            city=row['city'],
                            rent=row['rent'],
                            description=row['description'],
                            allowed=row['allowed'],
                            roomType=row['roomType'],
                            phone=row['phone'],
                            building_img=row['building_img'],
                            bedroom_img=row['bedroom_img'],
                            kitchen_img=row['kitchen_img'],
                            bathroom_img=row['bathroom_img'],
                        )

                        new_houses_list.append(house)

                House.objects.bulk_create(new_houses_list)
                return redirect('houses/page/{0}'.format(id))
        except Exception as e:
            error_messages['error'] = e

    return render(request, 'upload_dataset.html', {'form': file_form, 'error_messages': error_messages})


