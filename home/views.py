from sqlite3 import Time
from time import time
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout
from django.urls import reverse
from .models import TimeSlot, AppUser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import datetime

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
# TOKEN = str({"web":{"client_id":"948911588932-bgrvnm8bo86uthtuglr4r4v0e1h1jgvt.apps.googleusercontent.com","project_id":"bughunters-362806","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://127.0.0.1:8000/accounts/google/login/callback/"],"javascript_origins":["https://127.0.0.1:8000"]}})

# Create your views here.
class Home(View):
    def get(self, request):
        if request.user.is_authenticated is False:
            return render(request, 'index.html')
        app_user = AppUser.objects.filter(user=request.user)
        if app_user[0].role=='public':
            sample_time = [10,25,30,35]
            context = {
                'time_slots': sample_time,
            }
            # return render(request, 'home/public_user.html', context)
            admin = AppUser.objects.filter(role='admin')
            if len(admin)==0:
                return render(request, 'home/public_user.html')
            time_slots = admin[0].admin_slots.all()
            context = {
                'time_slots': time_slots
            }
            return render(request, 'home/public_user.html', context)
        else:
            sample_time = [10,10,5,20,20,35]
            context = {
                'time_slots': sample_time,
            }
            # return render(request, 'home/admin_user.html', context)
            return render(request, 'home/admin_user.html')

    def post(self, request):
        app_user = AppUser.objects.get(user=request.user)
        if app_user.role=='public':
            admin = AppUser.objects.get(role='admin')
            time_slots = admin.admin_slots.all()
            start_datetime = datetime.datetime.strptime(request.POST['start_time'],"%H:%M")
            end_datetime = datetime.datetime.strptime(request.POST['end_time'],"%H:%M")
            start_time = start_datetime.time()
            end_time = end_datetime.time()
            print(start_time, end_time)
            for time_slot in time_slots:
                print(time_slot.start_time, time_slot.end_time)
                if time_slot.start_time<=start_time and time_slot.end_time>=end_time:
                    time_slot_to_add = TimeSlot()
                    time_slot_to_add.start_time = time_slot.start_time
                    time_slot_to_add.end_time = start_time
                    time_slot_to_add.date = datetime.date.today()
                    time_slot_to_add.admin_user=admin
                    time_slot_to_add.save()
                    time_slot_to_add = TimeSlot()
                    time_slot_to_add.start_time = end_time
                    time_slot_to_add.end_time = time_slot.end_time
                    time_slot_to_add.date = datetime.date.today()
                    time_slot_to_add.admin_user=admin
                    time_slot_to_add.save()
                    time_slot.delete()
                    creds = Credentials.from_authorized_user_file("/Users/mananjain/Desktop/virtualEnv/techathon/techathon/token.json", SCOPES)
                    service = build('calendar', 'v3', credentials=creds)
                    event = {
                        'summary': app_user.name,
                        'description': request.POST['notes'],
                        'start': {
                            'dateTime': start_datetime,
                            'timeZone': 'India/Delhi',
                        },
                        'end': {
                            'dateTime': end_datetime,
                            'timeZone': 'India/Delhi',
                        },
                        "conferenceSolution": {
                            "key": {
                                "type": "hangoutsMeet"
                            },
                        },
                        "conferenceId": "trh-nymg-mzw",
                        'attendees': [
                            {'email': app_user.email},
                            {'email': admin.email},
                        ],
                        'reminders': {
                            'useDefault': False,
                            'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                            ],
                        },
                    }
                    event = service.events().insert(calendarId='primary', body=event).execute()
                    print("event set on calendar")
                    return HttpResponseRedirect(reverse('home'))
            print("nothing done!!")
        else:
            admin = AppUser.objects.get(role='admin')
            time_slots = TimeSlot()
            time_slots.date = datetime.date.today()
            time_slots.start_time = request.POST['start_time']
            time_slots.end_time = request.POST['end_time']
            time_slots.admin_user = admin
            time_slots.save()
            return HttpResponseRedirect(reverse('home'))

class UserDetails(View):
    def get(self, request):
        app_user = AppUser.objects.filter(user=request.user)
        if len(app_user)==0:
            context = {
                'role': 'public'
            }
            return render(request, 'home/get_details.html')
        context = {
            'name': app_user[0].name,
            'role': app_user[0].role,
            'meet_link': app_user[0].meet_link
        }
        print(context['role'])
        return render(request, 'home/get_details.html', context)
    
    def post(self, request):
        app_user = AppUser.objects.filter(user=request.user)
        if len(app_user)==0:
            app_user = AppUser()
            app_user.email = request.user.email
            app_user.name = request.POST['name']
            app_user.meet_link = "Not set"
            app_user.role = 'public'
            app_user.user = request.user
            app_user.save()
            print("len of users is 0")
            return HttpResponseRedirect(reverse('home'))
        app_user[0].name = request.POST['name']
        app_user[0].meet_link = request.POST['meet_link']
        app_user[0].save()
        return HttpResponseRedirect(reverse('home'))
        

class SetUserPublic(View):
    def post(self, request):
        app_user = AppUser.objects.get(user=request.user)
        app_user.role = "public"
        app_user.save()
        return HttpResponseRedirect(reverse('home'))


class SetUserAdmin(View):
    def post(self, request):
        app_user = AppUser.objects.get(user=request.user)
        app_user.role = "admin"
        app_user.save()
        return HttpResponseRedirect(reverse('home'))


def LogOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))