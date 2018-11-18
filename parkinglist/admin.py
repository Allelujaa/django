from django.contrib import admin

# Register your models here.
from .models import Currparkinglot, Client, Flight, Parkinglot

admin.site.register(Currparkinglot)
admin.site.register(Client)
admin.site.register(Flight)
admin.site.register(Parkinglot)