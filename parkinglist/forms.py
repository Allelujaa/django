from django import forms
import datetime

class FlightSearch(forms.Form):
    searched_flight = forms.CharField(label='', max_length=10)

class SearchForm(forms.Form):
    searched_car = forms.CharField(label='', max_length=10)

class AdvSearchForm(forms.Form):
    searched_car = forms.CharField(label='차 번호', max_length=20, required=False)
    in_datetime_start = forms.DateTimeField(label='입장일시(부터)', required=False, input_formats=['%Y-%m-%d %H:%M:%S'], initial='2018-12-31 23:59:59')
    in_datetime_end = forms.DateTimeField(label='입장일시(까지)', required=False, input_formats=['%Y-%m-%d %H:%M:%S'], initial='2018-12-31 23:59:59')
    out_datetime_start = forms.DateTimeField(label='퇴장일시(부터)', required=False, input_formats=['%Y-%m-%d %H:%M:%S'], initial='2018-12-31 23:59:59')
    out_datetime_end = forms.DateTimeField(label='퇴장일시(까지)', required=False, input_formats=['%Y-%m-%d %H:%M:%S'], initial='2018-12-31 23:59:59')
    cost_min = forms.IntegerField(label='요금(부터)', required=False)
    cost_max = forms.IntegerField(label='요금(까지)', required=False)
    sectionno = forms.CharField(label='주차자리', max_length=10, required=False)
    exists = forms.ChoiceField(label='현재유무', required=False, widget=forms.Select(), choices=(
        (None, '선택안함'),
        (1, '있음'),
        (0, '없음')
    ))

class StatsForm(forms.Form):
    type_stats = forms.ChoiceField(label='통계유형', required=True, widget=forms.Select(), choices=(
        ('1', '매출'),
        ('2', '차량'),
        ('3', '구역'),
        ('4', '고객')
    ))
    datetime_start = forms.DateTimeField(label='기간(부터)', required=False, input_formats=['%Y-%m-%d %H:%M:%S'], initial='2018-12-31 23:59:59')
    datetime_end = forms.DateTimeField(label='기간(까지)', required=False, input_formats=['%Y-%m-%d %H:%M:%S'], initial='2018-12-31 23:59:59')