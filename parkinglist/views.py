from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Currparkinglot, Parkinglot
from .forms import FlightSearch, SearchForm, AdvSearchForm, StatsForm
from django.views.generic.edit import CreateView
from django.db.models import Q
import datetime
from . import calculate, recommend, visual, stats
from django.contrib.auth.decorators import login_required

def index(request, show='default'):
    car2darray = visual.visualize()

    # line is used to mark cols and rows that need spaces in html output
    line = ['A20', 'A40', 'B10', 'B30', 'C20', 'C40', 'D10', 'D30', 'E20', 'E40', 'F10', 'F30']

    # carcount[0] --> A,B 차 개수
    # carcount[1] --> C,D 차 개수
    # carcount[2] --> E,F 차 개수
    carcount = [visual.carcount(x) for x in range(1, 4)]

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
            data = form.cleaned_data.get('searched_flight')
            context['recommend'] = recommend.Induce(data)
            context['flight'] = data
            context['gate'] = recommend.Get_Gate_no(data)

    return render(request, 'parkinglist/index.html', context)

def get_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('searched_car')
            car = Parkinglot.objects.filter(carno=data)
            # update cost if car exists
            # 추후 통합시 반드시 수정할것***
            for x in car:
                if x.currexist == 1:
                    x.cost = calculate.calculate(x.parkingtime)
                    x.save()
            return render(request, 'parkinglist/detail.html', {'car' : car})
    else:
        form = SearchForm()
        return render(request, 'parkinglist/search.html', {'form' : form})

@login_required(login_url='/admin/login')
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
            
            car = Parkinglot.objects.filter(q)
                # 추후에 primary key인 자동생성 id column이 필요
                # 지금은 model.Parkinglot.carNo로 조회하기때문에 중복차량은 안나올수도 있음
            # if car.exists() == False:
            #     raise Http404('No records available')

            for x in car:
                if x.currexist == 1:
                    x.cost = calculate.calculate(x.parkingtime)
                    x.save()

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
        visual.delete_overTime()
    context = {
        'car': visual.check_overTime()
    }
    return render(request, 'parkinglist/check.html', context)

@login_required(login_url='/admin/login')
def get_records(request, page):
    start = (page - 1) // 10 * 10 + 1
    end = start + 10
    totalpagecount = visual.count_records() // 10 + 1
    display = [i for i in range(start, end)]
    context = {
        'car': visual.show_records((page - 1) * 10, page * 10 - 1),
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
                    'data': stats.sale_stats(datetime_start,datetime_end)
                    }
            elif type_stats == '2':
                context = {
                    'title': '차량 통계',
                    'tabletitle': ['차량 번호', '주차장 이용 횟수', '총액', '평균 금액'],
                    'data': stats.car_stats(datetime_start,datetime_end)
                    }
            elif type_stats == '3':
                data = stats.section_stats(datetime_start,datetime_end)
                # list의 None을 0으로 변환
                data = [0 if x == None else x for x in data]
                # list에서 3개씩 골라 tuple로 묶은 후, tuple의 list로 변환
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
                    'data': stats.user_stats(datetime_start,datetime_end)
                    }
            else:
                return False
            if not context: context = '조건에 일치하는 통계 자료가 없습니다.'  #자료가 없다.
            return render(request, 'parkinglist/stats_display.html', context)
    else:
        form = StatsForm()
        return render(request, 'parkinglist/stats.html', {'form' : form})
