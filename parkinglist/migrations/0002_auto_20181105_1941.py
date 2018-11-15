# Generated by Django 2.1.3 on 2018-11-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_no', models.CharField(max_length=50)),
                ('car_no', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Parkinglot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_no', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=10)),
                ('parking_time', models.DateTimeField(verbose_name='time in')),
                ('exit_time', models.DateTimeField(verbose_name='time out')),
                ('cost', models.IntegerField(default=0)),
                ('current_exist', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Weighted_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_no', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='member',
            name='car',
        ),
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]