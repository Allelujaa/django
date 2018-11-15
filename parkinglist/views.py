from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Currparkinglot, Parkinglot
from .forms import SearchForm, AdvSearchForm
from django.views.generic.edit import CreateView

def index(request):
    existing_cars = Currparkinglot.objects.all()
    car2darray = [[False for i in range(10)] for j in range(10)]
    for car in existing_cars:
        if car.sectionno == '':
            continue
        else:
            # y = alphabet                  - A
            # x = number following alphabet - 10
            y = ord(car.sectionno[0]) - 65
            x = int((car.sectionno).replace(car.sectionno[0], '')) - 1
            car2darray[x][y] = True
    context = {
        'title': '주차장 현황',
        'car2darray': car2darray
    }
    return render(request, 'parkinglist/index.html', context)

def detail(request, carno):
    try:
        car = Parkinglot.objects.filter(carno=carno)
    except Parkinglot.objects.filter(carno=carno).DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, 'parkinglist/detail.html', {'car' : car})

def get_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('searched_car')
            car = Parkinglot.objects.filter(carno=data)
            return render(request, 'parkinglist/detail.html', {'car' : car})
    else:
        form = SearchForm()
        return render(request, 'parkinglist/search.html', {'form' : form})

def adv_search(request):
    if request.method == 'POST':
        form = AdvSearchForm(request.POST)
        if form.is_valid():
            cardata = form.cleaned_data.get('searched_car')
            in_datetime_start = form.cleaned_data.get('in_datetime_start')
            in_datetime_end = form.cleaned_data.get('in_datetime_end')
            out_datetime_start = form.cleaned_data.get('out_datetime_start')
            out_datetime_end = form.cleaned_data.get('out_datetime_end')
            cost_min = form.cleaned_data.get('cost_min')
            cost_max = form.cleaned_data.get('cost_max')
            location = form.cleaned_data.get('location')
            exists = form.cleaned_data.get('exists')
            
            # context = {
            #     'car' : cardata,
            #     'in_datetime_start' : in_datetime_start,
            #     'in_datetime_end' : in_datetime_end,
            #     'out_datetime_start' : out_datetime_start,
            #     'out_datetime_end' : out_datetime_end,
            #     'cost_min' : cost_min,
            #     'cost_max' : cost_max,
            #     'location' : location,
            #     'exists' : exists,
            # }
            return render(request, 'parkinglist/test.html', context)
    else:
        form = AdvSearchForm()
        return render(request, 'parkinglist/adv_search.html', {'form' : form})