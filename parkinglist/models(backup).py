from django.db import models

class Car(models.Model):
    car_no = models.CharField('Car Number', max_length=10)
    location = models.CharField(max_length=10, blank=True)
    parking_time = models.DateTimeField('time in')
    exit_time = models.DateTimeField('time out', blank=True, null=True)
    cost = models.IntegerField(default=0, blank=True)
    current_exist = models.BooleanField('In lot', default=0)
    def __str__(self):
        return self.car_no

class Client(models.Model):
    client_no = models.CharField(max_length=10)
    car_no = models.CharField(max_length=10)
    def __str__(self):
        return self.client_no

class Weighted_value(models.Model):
    section_no = models.CharField(max_length=10)
    A_val = models.IntegerField
    B_val = models.IntegerField
    C_val = models.IntegerField