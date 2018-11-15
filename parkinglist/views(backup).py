from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Car
from .forms import SearchForm

def index(request):
    existing_cars = Car.objects.filter(current_exist=True)
    car2darray = [[False for i in range(10)] for j in range(10)]
    for car in existing_cars:
        if car.location == '':
            continue
        #row number is 10, gets idx[2]
        if len(car.location) == 3:
            x = 9
        else:
            x = int(car.location[1]) - 1
        y = ord(car.location[0]) - 65
        car2darray[x][y] = True
    context = {
        'title': '주차장 현황',
        'car2darray': car2darray
    }
    return render(request, 'parkinglist/index.html', context)

def detail(request, car_no):
    try:
        car = Car.objects.filter(car_no=car_no)
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, 'parkinglist/detail.html', {'car' : car})

def get_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('searched_car')
            car = Car.objects.filter(car_no=data)
            return render(request, 'parkinglist/detail.html', {'car' : car})
    else:
        form = SearchForm()
        return render(request, 'parkinglist/search.html', {'form' : form})