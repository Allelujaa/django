# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Client(models.Model):
    carno = models.CharField(db_column='carNo', max_length=10, null=True)  # Field name made lowercase.
    clientno = models.IntegerField(db_column='clientNo', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=10, null=True)

    class Meta:
        managed = False
        db_table = 'client'
    
    def __str__(self):
        return str(self.clientno)


class Currparkinglot(models.Model):
    sectionno = models.CharField(db_column='sectionNo', primary_key=True, max_length=10)  # Field name made lowercase.
    carno = models.CharField(db_column='carNo', max_length=10, null=True)  # Field name made lowercase.
    currexist = models.IntegerField(db_column='currExist', null=True)  # Field name made lowercase.
    avalue = models.IntegerField(db_column='Aval', null=True)
    bvalue = models.IntegerField(db_column='Bval', null=True)
    cvalue = models.IntegerField(db_column='Cval', null=True)
    dvalue = models.IntegerField(db_column='Dval', null=True)
    evalue = models.IntegerField(db_column='Eval', null=True)
    fvalue = models.IntegerField(db_column='Fval', null=True)

    class Meta:
        managed = False
        db_table = 'currParkinglot'
    
    def __str__(self):
        return self.sectionno


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Flight(models.Model):
    flightno = models.CharField(db_column='flightNo', primary_key=True, max_length=10)  # Field name made lowercase.
    gateno = models.CharField(db_column='gateNo', max_length=10, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'flight'

class Parkinglot(models.Model):
    carno = models.CharField(db_column='carNo', max_length=10, primary_key=True)  # Field name made lowercase.
    parkingtime = models.DateTimeField(db_column='parkingTime', blank=True, null=True)  # Field name made lowercase.
    exittime = models.DateTimeField(db_column='exitTime', blank=True, null=True)  # Field name made lowercase.
    cost = models.IntegerField(db_column='cost', blank=True, null=True)
    currexist = models.IntegerField(db_column='currExist', null=True)  # Field name made lowercase.
    sectionno = models.CharField(db_column='sectionNo', max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parkinglot'
    
    def __str__(self):
        return self.carno
