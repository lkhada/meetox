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
        app_user = AppUser.objects.get(user=request.user)
        if app_user.role=='public':
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

class MakeUser(View):
    def get(self, request):
        app_user = AppUser()
        app_user.email = request.user.email
        app_user.role = "public"
        app_user.user = request.user
        app_user.save()
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