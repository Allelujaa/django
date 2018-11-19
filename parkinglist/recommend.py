import requests
from bs4 import BeautifulSoup
import pymysql

html = requests.get('https://www.airport.co.kr/gimpo/extra/liveSchedule/liveScheduleList/layOut.do?langType=1&inoutType=OUT&cid=2015102611043202364&menuId=8').text
soup = BeautifulSoup(html, 'html.parser')
conn = pymysql.connect(host = 'localhost',port = 3306,user = 'root',passwd = '2018',db = 'project7')
curs = conn.cursor()

def Get_Gate_no(flight_no):
    Counter = 0
    Gate_no = -1

    for tag in soup.select('#customer_container > div.table-responsive.mt30 > table > tbody > tr > td'):
        if tag.text == flight_no:
            Gate_no +=(Counter+7)

        elif Counter==Gate_no:
            return tag.text
        Counter+=1

def Induce(flightNo):
    gate = Get_Gate_no(flightNo)
    print(gate)
    if gate == None:
        sql = "SELECT sectionNo FROM currParkinglot WHERE currExist = 0"
        curs.execute(sql)
        return curs.fetchone()[0]

    else:
        gate = int(gate)

        if gate<=4:
            val = "Aval"
        elif gate<=11:
            val = "Bval"
        elif gate<=17:
            val = "Cval"
        elif gate<=34:
            val = "Dval"
        elif gate <=37:
            val = 'Eval'
        else:
            val = 'Fval'

        Counter = 6
        while Counter>=1:
            sql = "SELECT sectionNo FROM currParkinglot WHERE %s = %s and currExist = 0"%(val,Counter)
            if curs.execute(sql):
                return(curs.fetchone()[0])
            else:
                Counter -= 1
