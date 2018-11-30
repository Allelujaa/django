from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Currparkinglot, Parkinglot
from .forms import FlightSearch, SearchForm, AdvSearchForm, StatsForm
from django.views.generic.edit import CreateView
from .parkfunctions import admin, parkingsystem
from django.contrib.auth.decorators import login_required

admin = admin()
parkingsystem = parkingsystem()

def index(request, show='default'):
    car2darray = admin.visualize()

    # line is used to mark cols and rows that need spaces in html output
    line = ['A20', 'A40', 'B10', 'B30', 'C20', 'C40', 'D10', 'D30', 'E20', 'E40', 'F10', 'F30']

    # carcount[0] --> A,B 차 개수
    # carcount[1] --> C,D 차 개수
    # carcount[2] --> E,F 차 개수
    carcount = [admin.carcount(x) for x in range(1, 4)]

    context = {
        'title': '주차장 현황',
        'car2darray': car2darray,
        'line': line,
        'form': FlightSearch(),
        'carcount': carcount,
        'show': show    # 사용자 검색에서 주차된 차량의 자리 링크를 선택하면 자리(str)가 show로 전달된다.
    }

    if request.method == 'POST':
        form = FlightSearch(request.POST)
        if form.is_valid():
            flightNo = form.cleaned_data.get('searched_flight')
            context['recommend'] = parkingsystem.Induce(flightNo)
            context['flight'] = flightNo
            context['gate'] = parkingsystem.Get_Gate_no(flightNo)

    return render(request, 'parkinglist/index.html', context)

def get_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('searched_car')
            car = Parkinglot.objects.filter(carno=data)
            for x in car:
                if x.currexist == 1:
                    parkingsystem.calculate(x.carno, command='search')
            return render(request, 'parkinglist/detail.html', {'car': car})
    else:
        form = SearchForm()
        return render(request, 'parkinglist/search.html', {'form' : form})

@login_required(login_url='/admin/login')
def adv_search(request):
    if request.method == 'POST':
        form = AdvSearchForm(request.POST)
        if form.is_valid():
            
            q = admin.advanced_search(
                cardata = form.cleaned_data.get('searched_car'),
                in_datetime_start = form.cleaned_data.get('in_datetime_start'),
                in_datetime_end = form.cleaned_data.get('in_datetime_end'),
                out_datetime_start = form.cleaned_data.get('out_datetime_start'),
                out_datetime_end = form.cleaned_data.get('out_datetime_end'),
                cost_min = form.cleaned_data.get('cost_min'),
                cost_max = form.cleaned_data.get('cost_max'),
                sectionno = form.cleaned_data.get('sectionno'),
                exists = form.cleaned_data.get('exists')
            )
            
            car = Parkinglot.objects.filter(q)
                # 추후에 primary key인 자동생성 id column이 필요
                # 지금은 model.Parkinglot.carNo로 조회하기때문에 중복차량은 안나올수도 있음

            for x in car:
                if x.currexist == 1:
                    parkingsystem.calculate(x.carno)

            context = {
                'car': car
            }
            return render(request, 'parkinglist/detail.html', context)
            
    else:
        form = AdvSearchForm()
        return render(request, 'parkinglist/adv_search.html', {'form' : form})

@login_required(login_url='/admin/login')
def check_car(request):
    if request.method == 'POST':
        admin.delete_overTime()
    context = {
        'car': admin.check_overTime()
    }
    return render(request, 'parkinglist/check.html', context)

@login_required(login_url='/admin/login')
def get_records(request, page):
    start = (page - 1) // 10 * 10 + 1
    end = start + 10
    totalpagecount = admin.count_records() // 10 + 1
    display = [i for i in range(start, end)]
    context = {
        'car': admin.show_records((page - 1) * 10, page * 10 - 1),
        'display': display,
        'totalpagecount': totalpagecount
    }
    return render(request, 'parkinglist/records.html', context)

@login_required(login_url='/admin/login')
def statistics(request):
    if request.method == 'POST':
        form = StatsForm(request.POST)
        if form.is_valid():
            type_stats = form.cleaned_data.get('type_stats')
            datetime_start = form.cleaned_data.get('datetime_start')
            datetime_end = form.cleaned_data.get('datetime_end')
            if datetime_start == None:
                datetime_start = ''
            if datetime_end == None:
                datetime_end = ''

            if type_stats == '1':
                context = {
                    'title': '매출 통계',
                    'tabletitle': ['총액', '평균 금액'],
                    'data': admin.sale_stats(datetime_start,datetime_end)
                    }
            elif type_stats == '2':
                context = {
                    'title': '차량 통계',
                    'tabletitle': ['차량 번호', '주차장 이용 횟수', '총액', '평균 금액'],
                    'data': admin.car_stats(datetime_start,datetime_end)
                    }
            elif type_stats == '3':
                data = admin.section_stats(datetime_start,datetime_end)
                # list의 None을 0으로 변환
                data = [0 if x == None else x for x in data]
                # list에서 3개씩 골라 tuple로 묶은 후, tuple의 list로 변환
                # [('A', 10, 20000), ('B', 5, 1000), ...]
                data = [(chr((i // 2) + 65), data[i], data[i + 1]) for i in range(0, 10, 2)]
                
                context = {
                    'title': '구역 통계',
                    'tabletitle': ['구역', '총 이용 차량 수', '총액'],
                    'data': data
                    }
            elif type_stats == '4':
                context = {
                    'title': '고객 통계',
                    'tabletitle': ['총 고객 수', '총액', '총 일반 고객 수', '일반 고객 총 요금', '총 회원 고객 수', '회원 고객 총 요금'],
                    'data': admin.user_stats(datetime_start,datetime_end)
                    }
            else:
                return False
            return render(request, 'parkinglist/stats_display.html', context)
    else:
        form = StatsForm()
        return render(request, 'parkinglist/stats.html', {'form' : form})

def enter(request):
    if request.method == 'POST':
        form = EnterForm(request.POST)
        if form.is_valid():
            carno = form.cleaned_data.get('carno')
            if form.cleaned_data.get('inout') == 0: #입장
                parkingsystem.CarEnterHandler(carno=carno)
                
            
            return render(request, 'parkinglist/detail.html', {'car': car})
    else:
        form = SearchForm()
        return render(request, 'parkinglist/search.html', {'form' : form})