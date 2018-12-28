import pymysql
import datetime
from dateutil.relativedelta import *
import requests
from bs4 import BeautifulSoup
from django.db.models import Q
import os

html = requests.get(
    'https://www.airport.co.kr/gimpo/extra/liveSchedule/liveScheduleList/layOut.do?langType=1&inoutType=OUT&cid=2015102611043202364&menuId=8').text
soup = BeautifulSoup(html, 'html.parser')

# 이 프로그램이 메인일 경우 프로그램 시작시 DB에 connect를 합니다.
# 웹에서 import할 경우, 각 클래스 인스턴스 생성 시점에 connect를 합니다.
if __name__ == '__main__':
    # app engine에서 작동할 경우, unix socket으로 db에 연결합니다
    # db에 대한 정보는 app.yaml의 환경변수에서 볼 수 있습니다.
    if os.environ.get('CHECK_INSTANCE'):
        db_user = os.environ.get('CLOUD_SQL_USERNAME')
        db_password = os.environ.get('CLOUD_SQL_PASSWORD')
        db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
        db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
    # 일반 기기에서 작동할 경우, tcp socket으로 db에 연결합니다.
    else:
        conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
    cursor = conn.cursor()

class car():
    def __init__(self,car_no,server):
        self.car_no = car_no
        self.server = server
        self.flight_no = None
        self.check_inf = None
        self.user = False
        self.sectionNo = None

        # app engine에서 작동할 경우, unix socket으로 db에 연결합니다
        # db에 대한 정보는 app.yaml의 환경변수에서 볼 수 있습니다.
        if os.environ.get('CHECK_INSTANCE'):
            db_user = os.environ.get('CLOUD_SQL_USERNAME')
            db_password = os.environ.get('CLOUD_SQL_PASSWORD')
            db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
            db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            self.conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
        # 일반 기기에서 작동할 경우, tcp socket으로 db에 연결합니다.
        else:
            self.conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
        self.cursor = self.conn.cursor()

    def car_in(self):
        sql = "SELECT count(*) FROM currParkinglot WHERE carNo = '%s'" % self.car_no
        self.cursor.execute(sql)
        if (self.cursor.fetchone()[0] > 0):
            print("이미 주차된 차량입니다.\n")
            return 0

        sql = "SELECT count(*) FROM currParkinglot WHERE currExist = 0"
        self.cursor.execute(sql)
        if (self.cursor.fetchone()[0] <= 0):
            print("만차입니다.\n")
            return 0

        self.check_inf = 'N'
        self.user = False

        # 회원일 경우
        sql = "SELECT count(*) FROM client WHERE carNo = '%s'" % self.car_no  # 회원 DB에 해당 차량 번호가 있는지 확인
        self.cursor.execute(sql)
        if (self.cursor.fetchone()[0] > 0):
            self.user = True
            self.check_inf = 'Y'
            print("회원입니다.")

        # 비회원이 올바른 정보 입력 시까지 루프
        while (self.check_inf != 'Y'):
            self.flight_no = input("비행편 입력 : ")
            self.check_inf = input("차량번호 : %s , 비행편 : %s 가 맞으십니까?(Y/N) : " % (self.car_no, self.flight_no))
        if self.user == False:
            print("추천 자리 :", self.server.Induce(self.flight_no))

        self.server.barr_on()
        # self.parking()

    def parking(self):
        while True:
            self.sectionNo = input("(주차자리인식) ")
            sql = "SELECT count(*) FROM currParkinglot WHERE sectionNo='%s' and currExist = 0 and Aval = 6" % self.sectionNo
            self.cursor.execute(sql)
            if (self.cursor.fetchone()[0] <= 0):
                print("이미 주차된 자리이거나 유효하지 않은 자리입니다.")
                continue
            else:
                break

        print(self.sectionNo, "주차완료.")

        sql = "SELECT count(*) FROM currParkinglot WHERE carNo = '%s'" % self.car_no  # 이미 주차된 차량이 자리를 옮기는 경우
        self.cursor.execute(sql)
        if (self.cursor.fetchone()[0] > 0):
            sql = "UPDATE currParkinglot SET currExist = 0, carNo = null WHERE carNo = '%s'" % self.car_no
            self.cursor.execute(sql)
            self.conn.commit()

            sql = "UPDATE currParkinglot SET carNo = '%s', currExist = 1 WHERE sectionNo = '%s'" % (
            self.car_no, self.sectionNo)
            self.cursor.execute(sql)
            self.conn.commit()

            sql = "UPDATE parkinglot SET sectionNo = '%s' WHERE carNo = '%s' and currExist = 1" % (
            self.sectionNo, self.car_no)
            self.cursor.execute(sql)
            self.conn.commit()

        else:
            sql = """INSERT INTO
                            parkinglot(carNo, sectionNo, parkingTime, currExist)
                            VALUES(%s,%s, %s, %s)"""
            self.cursor.execute(sql, (self.car_no, self.sectionNo, datetime.datetime.now(), 1))
            self.conn.commit()

            sql = """
                    UPDATE currParkinglot
                    SET carNo = %s, currExist = %s
                    WHERE sectionNo = %s
                    """
            self.cursor.execute(sql, (self.car_no, 1, self.sectionNo))
            self.conn.commit()

    # 차량 퇴장 함수 // sectionNo 정해지면 sql 문 수정
    def car_out(self):
        sql = "SELECT count(*) FROM currParkinglot WHERE carNo = '%s'" % self.car_no
        cursor.execute(sql)
        if (cursor.fetchone()[0] <= 0):
            print("주차 기록이 없는 차량입니다.")

        sql = "SELECT count(*) FROM client WHERE carNo = '%s'" % self.car_no  # 회원 DB에 해당 차량 번호가 있는지 확인, 회원이면 요금 부과되지 않음
        cursor.execute(sql)
        if (cursor.fetchone()[0] > 0):
            print("회원입니다.")                     

        else:
            self.server.calculate(self.car_no)
            sql = """
                            UPDATE currParkinglot
                            SET carNo = %s, currExist = %s
                            WHERE carNo = %s
                            """
            cursor.execute(sql, (None, 0, self.car_no))
            conn.commit()

            sql = """update parkinglot
                             set currExist = %s
                             WHERE carNo = %s and currExist = 1"""
            cursor.execute(sql, (0, self.car_no))
            conn.commit()

        self.server.barr_off()


class parkingsystem():
    if __name__ != '__main__':
        def __init__(self):
            # app engine에서 작동할 경우, unix socket으로 db에 연결합니다
            # db에 대한 정보는 app.yaml의 환경변수에서 볼 수 있습니다.
            if os.environ.get('CHECK_INSTANCE'):
                db_user = os.environ.get('CLOUD_SQL_USERNAME')
                db_password = os.environ.get('CLOUD_SQL_PASSWORD')
                db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
                db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
                unix_socket = '/cloudsql/{}'.format(db_connection_name)
                self.conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
            # 일반 기기에서 작동할 경우, tcp socket으로 db에 연결합니다.
            else:
                self.conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
            self.cursor = self.conn.cursor()

    def CarEnterHandler(self):
        while True:
            print("차량번호 인식")
            client = car(input(),self)  # 차량번호 입력
            client.car_in()
            del client

    def CarExitHandler(self):
        while True:
            print('차량번호 인식')
            client = car(input(),self)
            client.car_out()
            del client

    def barr_on(self):
        # 차단봉 개방
        print("차단봉이 개방되었습니다.\n")

    def barr_off(self):
        print("차단봉이 해제되었습니다.\n")

        # 입장 시간 구하는 함수
    def get_enter_time(self,car_no):
        sql = "select parkingTime from parkinglot where carNo = '%s' and currExist = 1" %car_no
        self.cursor.execute(sql)
        time = self.cursor.fetchone()[0]   #위 select 결과 하나의 튜플만 나오는것이 정상
        return time

    def calculate(self,car_no,command='exit'):
        cost_day = 24000
        cost_hour = 4000
        cost_min = 500
        flag = False
        time_now = datetime.datetime.now()
        parkingTime = str(time_now - self.get_enter_time(car_no))
        print(parkingTime)
        
        if 'day' in parkingTime:
            parkingTime = parkingTime.replace("days", "").replace("day", "").replace(',', ":")
            print(parkingTime)
        else:
            parkingTime = parkingTime.replace(',', '')
            flag = True
        parkingTime = parkingTime.split(":")
        if flag:
            parkingTime.insert(0, '0')
        print(parkingTime)
        cost = str((int(parkingTime[0]) * cost_day) + (int(parkingTime[1]) * cost_hour) + (
                int(parkingTime[2]) // 10 * cost_min))

        if parkingTime[0] == '0' and parkingTime[1] == '0' and int(parkingTime[2]) < 15:
            print('15분 미만 주차로 요금이 부과되지 않습니다.')
            cost = "0"
        elif (int(cost) >= 300000):
            cost = "300000"

        print("사용 요금 : " + cost)

        sql = "UPDATE parkinglot SET cost= %s WHERE carNo = %s"
        self.cursor.execute(sql, (int(cost), car_no))
        self.conn.commit()
        # admin.get_search() 또는 admin.adv_search에서 calculate()를 호출시, command를 'search'로 전달하여 exitTime 업데이트를 하지 않습니다.
        if command == 'search':
            pass
        # car.car_out()에서 호출할 경우, command는 기본값인 'exit'을 가지고, exitTime을 업데이트합니다.
        else:
            sql = "UPDATE parkinglot SET exitTime = %s, currExist = 0 WHERE carNo = %s"   #계산할 때의 현재시간으로 퇴장시간 저장(예외케이스 고려)
            self.cursor.execute(sql, (time_now, car_no))
            self.conn.commit()

    def Get_Gate_no(self,flight_no):
        Counter = 0
        Gate_no = -1

        for tag in soup.select('#customer_container > div.table-responsive.mt30 > table > tbody > tr > td'):
            if tag.text == flight_no:
                Gate_no += (Counter + 7)

            elif Counter == Gate_no:
                return tag.text
            Counter += 1

    def Induce(self, flightNo):
        gate = self.Get_Gate_no(flightNo)
        print('게이트:',gate)
        if (gate == None) or (gate == ''):
            print("a")
            sql = "SELECT sectionNo FROM currParkinglot WHERE currExist = 0 order by rand()"
            self.cursor.execute(sql)
            return (self.cursor.fetchone()[0])
        else:
            gate = int(gate)

            if gate <= 4:
                val = "Aval"
            elif gate <= 11:
                val = "Bval"
            elif gate <= 17:
                val = "Cval"
            elif gate <= 34:
                val = "Dval"
            elif gate <= 37:
                val = 'Eval'
            else:
                val = 'Fval'

            Counter = 6
            while Counter >= 1:
                sql = "SELECT sectionNo FROM currParkinglot WHERE %s = %s and currExist = 0" % (val, Counter)
                if self.cursor.execute(sql):
                    return (self.cursor.fetchone()[0])
                else:
                    Counter -= 1

class admin():
    if __name__ != '__main__':
        def __init__(self):
            # app engine에서 작동할 경우, unix socket으로 db에 연결합니다
            # db에 대한 정보는 app.yaml의 환경변수에서 볼 수 있습니다.
            if os.environ.get('CHECK_INSTANCE'):
                db_user = os.environ.get('CLOUD_SQL_USERNAME')
                db_password = os.environ.get('CLOUD_SQL_PASSWORD')
                db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
                db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
                unix_socket = '/cloudsql/{}'.format(db_connection_name)
                self.conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
            # 일반 기기에서 작동할 경우, tcp socket으로 db에 연결합니다.
            else:
                self.conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
            self.cursor = self.conn.cursor()
        
    # check_overTime()은 parkinglot에서 현재 주차된 차 중 1년이 지난 차를 tuple 형태로 반환합니다.
    def check_overTime(self):
        year_before = datetime.datetime.now() - relativedelta(years=1)
        print(year_before)

        sql = "SELECT carNo from parkinglot where currExist = 1 and parkingTime<=%s"
        self.cursor.execute(sql, year_before)
        data = self.cursor.fetchall()
        print(data)
        return data
    
    # delete_overTime()은 check_overTime()에서 확인된 차량들을 
    #   1. currParkinglot에서 제거하고,
    #   2. parkinglot에서 currExist를 0으로 바꿉니다.
    #   3. 퇴장시간은 현재시간(관리자가 '현황에서 삭제' 버튼을 누른 시간)으로 기록합니다.
    def delete_overTime(self):
        try:
            count = 0
            for idx in self.check_overTime():
                sql = "UPDATE currParkinglot set currExist = %s, carNo = %s where carNo = %s"
                sql2 = "UPDATE parkinglot set currExist = %s, exitTime = %s where carNo = %s"
                self.cursor.execute(sql, (0, None, idx[0]))
                count = self.cursor.execute(sql2, (0, datetime.datetime.now(), idx[0]))
            self.conn.commit()
            return count
        except self.check_overTime() == None:
            return 0
        

    # visualize()는 현재 주차장을 표시한 2d 배열을 반환합니다.
    # 배열은 3(구역)x10(행)x10(열) 이고, 데이터는 'num', 'exist'으로 구성된 dictionary입니다.
    def visualize(self):
        sql = 'SELECT sectionNo, carNo, currExist FROM currParkinglot'
        self.cursor.execute(sql)
        currentlot = self.cursor.fetchall()
        # for spot in currentlot
        # spot[0] --> sectionNo
        # spot[1] --> carNo
        # spot[2] --> currExist
        
        # car2darray[3][10][10]
        car2darray = [[[{'num': '', 'exist': ''} for i in range(10)] for j in range(10)] for k in range(3)]

        for spot in currentlot:
            # sectionNos that start with A, C, E take the first half of the area
            # sectionNos that start with B, D, F take the other half
            if spot[0][0] in 'ACE': #A10
                x = int(spot[0][2])
                y = int(spot[0][1]) - 1
            elif spot[0][0] in 'BDF':
                x = int(spot[0][2])
                y = int(spot[0][1]) + 4
                
            # sectionNos that start with A, B --> car2darray[0]
            # sectionNos that start with C, D --> car2darray[1]
            # sectionNos that start with E, F --> car2darray[2]
            if spot[0][0] in 'AB':
                car2darray[0][x][y] = {'num': spot[0], 'exist': spot[2]}
            elif spot[0][0] in 'CD':
                car2darray[1][x][y] = {'num': spot[0], 'exist': spot[2]}
            elif spot[0][0] in 'EF':
                car2darray[2][x][y] = {'num': spot[0], 'exist': spot[2]}
        
        return car2darray

    # carcount(area)는 현재 주차장 area에 있는 차량의 개수를 반환합니다.
    # area = 1 -> A, B
    # area = 2 -> C, D
    # area = 3 -> E, F
    def carcount(self, area):
        if area == 1:
            val = ['A%%', 'B%%']
        elif area == 2:
            val = ['C%%', 'D%%']
        elif area == 3:
            val = ['E%%', 'F%%']
        else:
            return False
        sql = 'SELECT * FROM currParkinglot WHERE currExist = ''1'' AND sectionNo LIKE %s'
        
        count = self.cursor.execute(sql, val[0])
        count += self.cursor.execute(sql, val[1])
        
        return count

    # show_records(start, until)는 parkinglot에서 start번부터 until번 row를 tuple 형태로 반환합니다.
    def show_records(self, start, until):
        sql = "SELECT * from parkinglot limit %s, %s"
        self.cursor.execute(sql, (start, until))
        
        return self.cursor.fetchall()

    # count_records()는 parkinglot의 row 개수를 반환합니다.
    def count_records(self):
        sql = 'SELECT * FROM parkinglot'
        count = self.cursor.execute(sql)
        
        return count

    # advanced_search()는 특수검색을 위한 q object를 반환합니다.
    def advanced_search(
        self,
        cardata='',
        in_datetime_start=None,
        in_datetime_end=None,
        out_datetime_start=None,
        out_datetime_end=None,
        cost_min=None,
        cost_max=None,
        sectionno='',
        exists=''
        ):
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
            else: q &= Q(cost__gte=cost_min) #cost_min있음
        elif cost_max != None:  q &= Q(cost__lte=cost_max) #cost_max 있음

        if sectionno != '':  #주차 구역 조건 있을 때
            q &= Q(sectionno=sectionno)

        if exists != '':   #현재 유무 조건 있을 때
            q &= Q(currexist=int(exists))
        
        return q

    #매출: 총액, 평균 리턴
    def sale_stats(self,datetime_start,datetime_end):  
        if datetime_start=='':
            if datetime_end=='':  #시작, 끝 모두 없음
                sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE exitTime IS NOT NULL"
            else:    #끝 있음
                sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE exitTime<='%s'"%datetime_end
        else: #시작 있음
            if datetime_end=='':
                sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE exitTime>='%s'"%datetime_start
            else:    #시작, 끝 둘다 있음
                sql = "SELECT sum(cost), avg(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s')"%(datetime_start, datetime_end)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        
        return data

    #차량 통계: 차량별 주차장 이용횟수, 총금액, 평균 금액
    def car_stats(self,datetime_start,datetime_end):
        if datetime_start=='':
            if datetime_end=='':  #시작, 끝 모두 없음
                sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE exitTime IS NOT NULL GROUP BY carNo"
            else:    #끝 있음
                sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE exitTime<='%s' GROUP BY carNo"%datetime_end
        else:   #시작 있음
            if datetime_end=='':
                sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE exitTime>='%s' GROUP BY carNo"%datetime_start
            else:    #시작, 끝 둘다 있음
                sql = "SELECT carNo,count(*),sum(cost),avg(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s') GROUP BY carNo"%(datetime_start, datetime_end)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        
        return data

    #구역 통계: 구역별 총 차량 수, 총 금액 리턴
    def section_stats(self,datetime_start,datetime_end):  
        section_list = ['A%','B%','C%','D%','E%','F%']
        data_list = []  #A,B,C,D,E,F 각 구역별 주차했던 총 차량 수, 총 금액 저장 Ex.[23,450000,42,430000,...] 2개씩 해당 구역의 총차량수와 총금액
        if datetime_start=='':
            if datetime_end=='':  #시작, 끝 모두 없음
                for section in section_list:
                    sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE exitTime IS NOT NULL and sectionNo LIKE '%s'"%section
                    self.cursor.execute(sql)
                    for row in self.cursor:
                        data_list.append(row[0]), data_list.append(row[1])
            else:    #끝 있음
                for section in section_list:
                    sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE exitTime<='%s' and sectionNo LIKE '%s'"%(datetime_end,section)
                    self.cursor.execute(sql)
                    for row in self.cursor:
                        data_list.append(row[0]), data_list.append(row[1])  
        else:
            if datetime_end=='':  #시작 있음
                for section in section_list:
                    sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE exitTime>='%s' and sectionNo LIKE '%s'"%(datetime_start,section)
                    self.cursor.execute(sql)
                    for row in self.cursor:
                        data_list.append(row[0]), data_list.append(row[1])
            else:    #시작, 끝 둘다 있음
                for section in section_list:
                    sql = "SELECT count(*),sum(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s') and sectionNo LIKE '%s'"%(datetime_start, datetime_end, section)
                    self.cursor.execute(sql)
                    for row in self.cursor:
                        data_list.append(row[0]), data_list.append(row[1])
        
        return data_list

        
    #사용자 통계: 총 고객수, 총 금액, 총 일반 고객수, 일반 고객수의 총 금액, 총 회원 고객수, 총 회원 고객수의 총 금액 리턴   
    def user_stats(self,datetime_start,datetime_end):     
        if datetime_start=='':
            if datetime_end=='':  #시작, 끝 모두 없음
                sql =  """SELECT count(*), sum(cost) FROM parkinglot WHERE exitTime IS NOT NULL
                union all
                SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and exitTime IS NOT NULL
                union all
                SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and exitTime IS NOT NULL"""
            else:  # 끝 있음
                sql = """SELECT count(*), sum(cost) FROM parkinglot WHERE exitTime<='%s'
                union all
                SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and exitTime<='%s'
                union all
                SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and exitTime<='%s'"""%(datetime_end, datetime_end, datetime_end)
        else:  # 시작 있음
            if datetime_end=='':
                sql =  """SELECT count(*), sum(cost) FROM parkinglot WHERE exitTime>='%s'
                union all
                SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and exitTime>='%s'
                union all
                SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and exitTime>='%s'"""%(datetime_start, datetime_start, datetime_start)
            else:  # 시작, 끝 둘다 있음
                sql = """SELECT count(*), sum(cost) FROM parkinglot WHERE (exitTime BETWEEN '%s' AND '%s')
                union all
                SELECT count(*), sum(cost) FROM parkinglot WHERE carNo not in (SELECT distinct carNo FROM client) and (exitTime BETWEEN '%s' AND '%s')
                union all
                SELECT count(*), sum(cost) FROM parkinglot p, client c WHERE p.carNo = c.carNo and (exitTime BETWEEN '%s' AND '%s')"""%(datetime_start, datetime_end, datetime_start, datetime_end, datetime_start, datetime_end)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        
        return data


# system = parkingsystem()
# # system.CarExitHandler()
# system.CarEnterHandler()
