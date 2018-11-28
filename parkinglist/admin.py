from django.contrib import admin

# Register your models here.
from .models import Currparkinglot, Client, Parkinglot

admin.site.register(Currparkinglot)
admin.site.register(Client)
admin.site.register(Parkinglot)