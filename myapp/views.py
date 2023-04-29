from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import authenticate,login as lk,logout as lo
from django.contrib import messages
from .forms import LoginForm
from .models import *
import requests
import json
from faker import Faker
import random
faker = Faker()
## Create your views here.
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/profile")
    if request.method=="POST":
        a=request.POST["email"]
        print("a is ",a)
        fm=LoginForm(request,data=request.POST)
        
        if fm.is_valid():
            usernm=fm.cleaned_data["email"]
            paaswrd=fm.cleaned_data["password"]
            print("username is ",usernm)
            print("passwrd is ",paaswrd)
            user=authenticate(email=usernm,password=paaswrd)
            print("user is ",user)
            if user is not None:
                lk(request,user)
                messages.set_level(request,5)
                messages.info(request,"welcome to profile page")
                return HttpResponseRedirect("/profile/")
    else:
        fm=LoginForm()
    return render(request,"temp.html",{"form":fm})

def profile(request):
    return render(request,"profile.html")

def movie(request):
    if request.method=="POST":
        moviename=request.POST.get("moviename",None)
        category=request.POST.get("category")
        language=request.POST.get("language",None)
        description=request.POST.get("description",None)
        release_date=request.POST.get("release_date")
        user=request.POST.get("user")
        print(moviename,category,language,description,release_date,user)
        #s=ReportForm(location1=loc1,location2=loc2,description=description,date=date,time=time,severity=serverity,cause=cause,actions=action,type_env=type_env,type_inju=type_inju,type_property=type_property,type_vehicle=type_vehicle,submitted="f",reported_by_id=request.user)
        #s.save()
        print("saved")
    return render(request,"movie.html")

def logout(request):
    lo(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.method=="POST":
        fname=request.POST["fname"]
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        user_type = request.POST['user_type']
        print(gender,user_type)
        password = request.POST["password"]
        password1 = request.POST["password1"]
        s=User.objects.create_user(first_name=fname,last_name=lname,phone_number=phone,gender=gender,email=email,user_type=user_type,password=password)
        return HttpResponseRedirect("/")
    else:
        return render(request,"register.html")
    return render(request,'theatre.html')

def hall(request):
    return render(request,'hall.html')

def slots(request):
    return render(request,'slots.html')

def dashboard(request):
    disease_list=[]
    if request.method=="POST":
        symptoms = request.POST['frm_btn']
        print("bhai symptoms ka list dekhna toh ",symptoms,type(symptoms))
        disease_list=get_disease(symptoms)
    symptoms = Symptom.objects.all()
    return render(request,'dashboard.html',{'symptoms':symptoms,'disease_list':disease_list})

def get_all_symptoms():
    url = "https://healthservice.priaid.ch/symptoms?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFhc3RoYXNpbmdoLnRAZ21haWwuY29tIiwicm9sZSI6IlVzZXIiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiI5MzIxIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMTA5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6IjEwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IkJhc2ljIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAyMy0wMy0xNSIsImlzcyI6Imh0dHBzOi8vYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTY3OTI1MjQ1MywibmJmIjoxNjc5MjQ1MjUzfQ.Nmk3V8JT4jJ_ADEP2CTp0XuvK-jcpM8dYIo6hllB8YU&format=json&language=en-gb"
    email = "aasthasingh.t@gmail.com"
    passwrd = "A@shu6124"
    data = json.loads(requests.get(url,auth=(email,passwrd)).text)
    for i in range(50):
        Symptom.objects.create(id=data[i]["ID"],name=data[i]["Name"])
        print(i,"done")
    print(len(data))

def get_disease(symptoms_list):
    try:
        disease_list = []
        url = f'https://sandbox-healthservice.priaid.ch/diagnosis?symptoms={symptoms_list}&gender=male&year_of_birth=1982&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFhc3RoYXNpbmdoLnRAZ21haWwuY29tIiwicm9sZSI6IlVzZXIiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiIxMTk1NiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvdmVyc2lvbiI6IjIwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbGltaXQiOiI5OTk5OTk5OTkiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL21lbWJlcnNoaXAiOiJQcmVtaXVtIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAyMy0wMy0xNSIsImlzcyI6Imh0dHBzOi8vc2FuZGJveC1hdXRoc2VydmljZS5wcmlhaWQuY2giLCJhdWQiOiJodHRwczovL2hlYWx0aHNlcnZpY2UucHJpYWlkLmNoIiwiZXhwIjoxNjgyMDAxNTQ5LCJuYmYiOjE2ODE5OTQzNDl9.u-hguRXq-kznVYT_mQt-VUC9uHOzuD4Le3EGxt6vd2k&format=json&language=en-gb'
        email = "aasthasingh.t@gmail.com"
        passwrd = "A@shu6124"
        symptoms_list = json.loads(symptoms_list)
        data = json.loads(requests.get(url,json=symptoms_list,auth=(email,passwrd)).text)
        print("data is ",data)
        data_len = min([3,len(data)])
        data = data[:data_len]
        print(data)
        for diesease in data:
            disease_list.append({'name':diesease["Issue"]["Name"],'accuracy':round(diesease["Issue"]["Accuracy"],2),'prof_name':diesease["Issue"]["ProfName"],'ranking':diesease["Issue"]["Ranking"]})
        return disease_list
    except:
        return 
    

def bc(request):
    return render(request,'s.html')

def create_doctors(count):
    for i in range(count):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        gender = random.choice(['Male','Female'])
        user_type = 'Doctor'
        phone_number = '9754603986'
        experience = random.randint(1,15)
        password = '12345678'
        specialties = ['Cardiologist', 'Dermatologist', 'Endocrinologist', 'Gastroenterologist', 'Neurologist', 'Oncologist', 'Pediatrician', 'Psychiatrist', 'Radiologist', 'Surgeon']
        random_specialty = random.choice(specialties)
        address = faker.city()
        Doctor.objects.create(first_name=first_name,last_name=last_name,phone_number=phone_number,email=email,gender=gender,user_type=user_type,address=address,experience=experience,speciality=random_specialty)
    
def doctor(request):
    doctors = Doctor.objects.all()
    return render(request,'doctor.html',{'doctors':doctors})


