from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout
from django.urls import reverse
from .models import TimeSlot, AppUser

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
            return render(request, 'home/public_user.html', context)
        else:
            sample_time = [10,10,5,20,20,35]
            context = {
                'time_slots': sample_time,
            }
            return render(request, 'home/admin_user.html', context)

    def post(self, request):
        pass

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
            'role': app_user[0].role
        }
        return render(request, 'home/get_details.html')
    
    def post(self, request):
        app_user = AppUser.objects.filter(user=request.user)
        if len(app_user)==0:
            app_user = AppUser()
            app_user.email = request.user.email
            app_user.name = request['POST'].name
            app_user.meet_link = request['POST'].meet_link
            app_user.role = 'public'
            app_user.user = request.user
            app_user.save()
        app_user.name = request['POST'].name
        app_user.meet_link = request['POST'].meet_link
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