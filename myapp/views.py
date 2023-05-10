from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import authenticate,login as lk,logout as lo
from django.contrib import messages
from .forms import LoginForm
from django.core import serializers
from .models import *
import requests
from django.contrib.auth.hashers import make_password, check_password
import json
from faker import Faker
import random
faker = Faker()
from datetime import *
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
    return render(request,"login.html",{"form":fm})

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
        hashed_pwd = make_password(password)
        if user_type=='doctor':
            experience = request.POST["experience"]
            speciality = request.POST["specialization"]
            print(fname,lname,email,phone,speciality,experience,gender)
            Doctor.objects.create(first_name=fname,last_name=lname,phone_number=phone,gender=gender,email=email,user_type=user_type,password=hashed_pwd,experience=experience,speciality=speciality)
        else:
            s=User.objects.create_user(first_name=fname,last_name=lname,phone_number=phone,gender=gender,email=email,user_type=user_type,password=password)
        return HttpResponseRedirect("/")
    else:
        return render(request,"register.html")
    return render(request,'theatre.html')


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
    return render(request,'temp.html')

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
    if request.method == 'POST':
        appointment_id = None
        user_id = None
    doctors = Doctor.objects.filter(pk=3).values()
    for doctor in doctors:
        appointment_data = Appointment.objects.filter(doctor__id=3)
        doctor['appointments']=serializers.serialize('json',appointment_data)
    print('-------------------')
    print(doctors)
    print('--------------------')

    return render(request,'doctor.html',{'doctors':doctors})

def generate_appointments(start_date=None,appointment_days=None,start_time=None,end_time=None):
    s=datetime.now().date()
    start_time=timedelta(hours=9,minutes=0)
    end_time=timedelta(hours=12,minutes=0)
    duration = 30
    print(start_time)
    print(int((end_time-start_time).total_seconds()//60))
    next_date=s+timedelta(days=1)
    print(next_date)
    print('--------------------------')
    count=1
    for i in range(duration,int((end_time-start_time).total_seconds()//60)+duration,duration):
        print(f'slot {count} : {start_time} - {start_time+timedelta(minutes=duration)}')
        count+=1
        start_time+=timedelta(minutes=duration)
    print('----------------------------')
    

def create_appointments(request):
    s={'is_created':False}
    if request.method=='POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        print('logged in user id is ',request.user.id)
        print('logged in doctor obj is ',Doctor.objects.filter(pk=request.user.id).values())
        appointment_data=create_appointment_slots(start_date=start_date,end_date=end_date,start_time=start_time,end_time=end_time,doctor=Doctor.objects.get(pk=request.user.id))
        print(appointment_data)
        k=Appointment.objects.bulk_create(appointment_data)
        print(f'mst bhai record create ho gya , data dekho toh {k}')
        s={'is_created':True}
    return render(request,'create_appointment.html',context=s)

def split_time(start_time=None, end_time=None, slot_duration=30, curr_date=None,doctor=None):
    

    # convert start and end times to datetime objects
    start_time = timedelta(hours=int(start_time[:2]),minutes=int(end_time[-2:]))
    end_time = timedelta(hours=int(end_time[:2]),minutes=int(end_time[-2:]))

    # calculate the total number of minutes between start and end time
    total_minutes = int((end_time - start_time).total_seconds() / 60)

    # calculate the number of slots
    num_slots = int(total_minutes / slot_duration)
    
    # initialize the list of time slots

    s=[]
    # iterate through the slots and calculate the start and end time of each slot
    for i in range(num_slots):
        start_time = datetime(2023, 5, 6, 9, 0, 0)
        slot_start = start_time + timedelta(minutes=i * slot_duration)
        slot_end = slot_start + timedelta(minutes=slot_duration)
        start_time = datetime(2023, 5, 6, 0, 0, 0)
        # format the start and end times in am-pm format
        slot_start_str = slot_start.time().strftime('%I:%M %p')
        slot_end_str = slot_end.time().strftime('%I:%M %p')
        # appointment_dict = {}
        # appointment_dict['doctor']=doctor
        # appointment_dict['appointment_date']=curr_date
        # appointment_dict['start_time']=slot_start_str
        # appointment_dict['end_time']=slot_end_str
        # appointment_dict['is_available']=True
        #we are creating Appointment model object to store data using bulk create method
        appointment_data = Appointment(doctor=doctor,appointment_date=curr_date,start_time=slot_start_str,end_time=slot_end_str,is_available=True)
        s.append(appointment_data)
        # add the time slot to the list of slots
        

    return s

def create_appointment_slots(start_date,end_date,start_time,end_time,doctor):
    start_date=datetime(day=int(start_date[-2:]),month=int(start_date[5:7]),year=int(start_date[:4]))
    print(start_date.strftime('%Y-%m-%d : %A'))
    end_date=datetime(day=int(end_date[-2:]),month=int(end_date[5:7]),year=int(end_date[:4]))
    date_diff=int((end_date-start_date).days)
    k=[]
    for i in range(date_diff+1):
        curr_date = start_date+timedelta(days=i)
        curr_date = curr_date.strftime('%Y-%m-%d : %A')
        k.extend(split_time(start_time=start_time,end_time=end_time,curr_date=curr_date,doctor=doctor))
    return k