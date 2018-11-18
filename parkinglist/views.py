from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Currparkinglot, Parkinglot
from .forms import SearchForm, AdvSearchForm
from django.views.generic.edit import CreateView
from django.db.models import Q
import datetime

def color(x):
    if x == 0:
        return 'green'
    else:
        return 'red'

def index(request):
    currentlot = Currparkinglot.objects.all().order_by('sectionno')
    # car2darray[3][10][10]
    car2darray = [[[{'num': '', 'exist': ''} for i in range(10)] for j in range(10)] for k in range(3)]

    for spot in currentlot:
        # spotnames that start with A, C, E take the first half of the area
        # spotnames that start with B, D, F take the other half
        if spot.sectionno[0] in 'ACE':
            x = int(spot.sectionno[2])
            y = int(spot.sectionno[1]) - 1
        elif spot.sectionno[0] in 'BDF':
            x = int(spot.sectionno[2])
            y = int(spot.sectionno[1]) + 4
        # spotnames that start with A, B --> car2darray[0]
        # spotnames that start with C, D --> car2darray[1]
        # spotnames that start with E, F --> car2darray[2]
        if spot.sectionno[0] in 'AB':
            car2darray[0][x][y] = {'num': spot.sectionno, 'exist': color(spot.currexist)}
        elif spot.sectionno[0] in 'CD':
            car2darray[1][x][y] = {'num': spot.sectionno, 'exist': color(spot.currexist)}
        elif spot.sectionno[0] in 'EF':
            car2darray[2][x][y] = {'num': spot.sectionno, 'exist': color(spot.currexist)}

    # line is used to add cols and rows in html output
    line = ['A20', 'A40', 'B10', 'B30', 'C20', 'C40', 'D10', 'D30', 'E20', 'E40', 'F10', 'F30']

    context = {
        'title': '주차장 현황',
        'car2darray': car2darray,
        'line': line
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
            sectionno = form.cleaned_data.get('sectionno')
            exists = form.cleaned_data.get('exists')

            q = Q()
            if cardata != '': #차량번호 조건 있을 때
                q &= Q(carno=cardata)

            if in_datetime_start != None:
                if in_datetime_end != None:  #시작과 끝 범위 모두 있음
                    q &= Q(parkingtime__range=(in_datetime_start, in_datetime_end))
                else: q &= Q(parkingtime__gte=in_datetime_start) #시작만 있음
            elif in_datetime_end != None: q &= Q(parkingtime__lte=in_datetime_end) #끝만 있음

            if out_datetime_start != None:
                if out_datetime_end != None: #시작과 끝 범위 모두 있음
                    q &= Q(exittime__range=(out_datetime_start, out_datetime_end))
                else: q &= Q(exittime__gte=out_datetime_start)#시작만 있음
            elif out_datetime_end != None: q &= Q(exittime__lte=out_datetime_end)#끝만 있음

            if cost_min != None:
                if cost_max != None:
                    q &= Q(cost__range=(cost_min, cost_max))  #cost_min과 cost_max 모두 있음
                else: q &= Q(cost__gte=min_cost) #cost_min있음
            elif cost_max != None:  q &= Q(cost__lte=max_cost) #cost_max 있음

            if sectionno != '':  #주차 구역 조건 있을 때
                q &= Q(sectionno=sectionno)

            if exists != '':   #현재 유무 조건 있을 때
                q &= Q(currexist=int(exists))

            context = {
                'car': Parkinglot.objects.filter(q)   #필터링
            }
            return render(request, 'parkinglist/detail.html', context)
        
    else:
        form = AdvSearchForm()
        return render(request, 'parkinglist/adv_search.html', {'form' : form})
