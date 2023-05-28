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
from datetime import datetime
faker = Faker()
from datetime import *
from . import generate_meeting
import json


## Create your views here.
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/profile")
    if request.method=="POST":
        a=request.POST["email"]
        fm=LoginForm(request,data=request.POST)
        
        if fm.is_valid():
            usernm=fm.cleaned_data["email"]
            paaswrd=fm.cleaned_data["password"]
            user=authenticate(email=usernm,password=paaswrd)
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
        password = request.POST["password"]
        hashed_pwd = make_password(password)
        if user_type=='doctor':
            experience = request.POST["experience"]
            speciality = request.POST["specialization"]
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
        

def get_disease(symptoms_list):
    try:
        disease_list = []
        url = f'https://sandbox-healthservice.priaid.ch/diagnosis?symptoms={symptoms_list}&gender=male&year_of_birth=1982&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFhc3RoYXNpbmdoLnRAZ21haWwuY29tIiwicm9sZSI6IlVzZXIiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiIxMTk1NiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvdmVyc2lvbiI6IjIwMCIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbGltaXQiOiI5OTk5OTk5OTkiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL21lbWJlcnNoaXAiOiJQcmVtaXVtIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAyMy0wMy0xNSIsImlzcyI6Imh0dHBzOi8vc2FuZGJveC1hdXRoc2VydmljZS5wcmlhaWQuY2giLCJhdWQiOiJodHRwczovL2hlYWx0aHNlcnZpY2UucHJpYWlkLmNoIiwiZXhwIjoxNjgyMDAxNTQ5LCJuYmYiOjE2ODE5OTQzNDl9.u-hguRXq-kznVYT_mQt-VUC9uHOzuD4Le3EGxt6vd2k&format=json&language=en-gb'
        email = "aasthasingh.t@gmail.com"
        passwrd = "A@shu6124"
        symptoms_list = json.loads(symptoms_list)
        data = json.loads(requests.get(url,json=symptoms_list,auth=(email,passwrd)).text)
        data_len = min([3,len(data)])
        data = data[:data_len]
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
    is_created = False
    if request.method == 'POST':
        appointment_data = json.loads(request.POST.get('submit_btn'))
        print(f'hey there appointment data is {appointment_data}')
        doctor_mail = appointment_data['doctor_mail']
        patient_mail = appointment_data['patient_mail']
        appointment_data = appointment_data['appointment_time'].split(' ')
        print(f'appointment_date is {appointment_data}')
        appointment_date = appointment_data[0].split('-')
        appointment_start_time = appointment_data[3].split(':')
        start_hour = appointment_start_time[0]
        start_minute = appointment_start_time[1]
        appointment_end_time = appointment_data[4][3:]
        appointment_end_time = appointment_end_time.split(':')
        end_hour = appointment_end_time[0]
        end_minute = appointment_end_time[1]
        appointment_start = datetime(int(appointment_date[0]),int(appointment_date[1]),int(appointment_date[2]),int(start_hour),int(start_minute))
        appointment_end = datetime(int(appointment_date[0]),int(appointment_date[1]),int(appointment_date[2]),int(end_hour),int(end_minute))
        appointment_start_string = appointment_start.isoformat()
        #appointment_start_string = json.dumps(appointment_start_string)
        appointment_end_string = appointment_end.isoformat()
        #appointment_end_string = json.dumps(appointment_end_string)
        print(f'appointment_start is {type(appointment_start_string)}')
        print(f'appointment_end is {appointment_end_string}')
        #----------- sending mail logic ----------
        try:
           # plan = generate_meeting.EventPlanner({"rohitkashyap8925@gmail.com","sangeeta.gupta.dev@gmail.com","pshreyasi325@gmail.com"}, {"start": appointment_start_string,"end": appointment_end_string})                                                        
            plan = generate_meeting.EventPlanner([patient_mail,doctor_mail,"pshreyasi325@gmail.com"], {"start": appointment_start_string,
                                                                          "end": appointment_end_string})
            print(plan.event_states)
        except Exception as e:
            print('error occured : '+str(e))
        #-----------------------------------------
        is_created = True
    doctors = Doctor.objects.all().values()
    for doctor in doctors:
        appointment_data = Appointment.objects.filter(doctor__id=doctor['id'])
        doctor['appointments']=serializers.serialize('json',appointment_data)
    
    return render(request,'doctor.html',{'doctors':doctors,'is_created':is_created})

    
def create_appointments(request):
    s={'is_created':False}
    if request.method=='POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        appointment_data=create_appointment_slots(start_date=start_date,end_date=end_date,start_time=start_time,end_time=end_time,doctor=Doctor.objects.get(pk=request.user.id))
        k=Appointment.objects.bulk_create(appointment_data)
        s={'is_created':True}
    return render(request,'create_appointment.html',context=s)

def split_time(start_time=None, end_time=None, slot_duration=30, curr_date=None,doctor=None):
    

    # convert start and end times to datetime objects
    start_hour = int(start_time[:2])
    start_minute = int(end_time[-2:])
    end_hour = int(end_time[:2])
    end_minute = int(end_time[-2:])
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
        start_time = datetime(2023, 5, 6, start_hour, start_minute, 0)
        slot_start = start_time + timedelta(minutes=i * slot_duration)
        slot_end = slot_start + timedelta(minutes=slot_duration)
        start_time = datetime(2023, 5, 6, end_hour, end_minute, 0)
        # format the start and end times in am-pm format
        slot_start_str = slot_start.time().strftime('%I:%M %p')
        slot_end_str = slot_end.time().strftime('%I:%M %p')
        
        #we are creating Appointment model object to store data using bulk create method
        appointment_data = Appointment(doctor=doctor,appointment_date=curr_date,start_time=slot_start_str,end_time=slot_end_str,is_available=True)
        s.append(appointment_data)
        # add the time slot to the list of slots
        

    return s

def create_appointment_slots(start_date,end_date,start_time,end_time,doctor):
    start_date=datetime(day=int(start_date[-2:]),month=int(start_date[5:7]),year=int(start_date[:4]))
    end_date=datetime(day=int(end_date[-2:]),month=int(end_date[5:7]),year=int(end_date[:4]))
    date_diff=int((end_date-start_date).days)
    k=[]
    for i in range(date_diff+1):
        curr_date = start_date+timedelta(days=i)
        curr_date = curr_date.strftime('%Y-%m-%d : %A')
        k.extend(split_time(start_time=start_time,end_time=end_time,curr_date=curr_date,doctor=doctor))
    return k

def bp(request):
    return render(request,"bp.html")

def sugar(request):
    return render(request,"sugar.html")

def upload(request):
    return render(request,"upload.html")

def upload1(request):
    return render(request,"upload1.html")

def apt_history(request):
    return render(request,"appointment_history.html")

def apt_cancel(request):
    return render(request,"appointment_cancellation.html")

def create_event(request):
    return render(request, 'create_event.html')