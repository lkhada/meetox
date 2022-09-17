from django.contrib import admin
from .models import AppUser, TimeSlot
# Register your models here.

admin.site.register(AppUser)
admin.site.register(TimeSlot)
