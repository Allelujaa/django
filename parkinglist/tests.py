from django.test import TestCase
from django.db.models import Q
import datetime
import unittest
from parkfunctions import admin
from unittest.mock import MagicMock
import pymysql

admin = admin()
admin.delete_overTime_mock = MagicMock(return_value=None)

conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
cursor = conn.cursor()

class AdminTest(unittest.TestCase):
    
    # 테스트하는 유닛마다 parkinglist에 4줄의 데이터를 추가합니다.
    # 삭제는 추가한 데이터의 차량번호와 일치하는 데이터를 삭제하기 때문에, 테스트용 데이터는 기존에 있는 차량번호와 겹치지 않도록 해야합니다.
    def setUp(self):
        sqladd = """INSERT INTO parkinglot(carNo, sectionNo, parkingTime, exitTime, cost, currExist) VALUES(%s,%s,%s,%s,%s,%s)"""

        cursor.execute(sqladd, ("test1", "A10", datetime.datetime(2016, 1, 1, 0, 0), None, 300000, 1))
        cursor.execute(sqladd, ("test2", "B10", datetime.datetime(2016, 1, 1, 0, 0), None, 300000, 1))
        cursor.execute(sqladd, ("test1", "A10", datetime.datetime(2013, 1, 1, 0, 0), datetime.datetime(2013, 1, 2, 0, 0), 10000, 0))
        cursor.execute(sqladd, ("test2", "B10", datetime.datetime(2013, 1, 1, 0, 0), datetime.datetime(2013, 1, 2, 0, 0), 10000, 0))
        conn.commit()
        print('setUp running')

    def test_check_overtime(self):
        result = admin.check_overTime()
        check = (('test1',), ('test2',))
        self.assertEqual(result, check)
    
    def test_delete_overtime(self):
        result = admin.delete_overTime()
        self.assertEqual(result, 2)
    
    def test_visualize(self):
        result = admin.visualize()
        self.assertIsNotNone(result)
    
    # currParkinglot을 참조하기 때문에 반드시 테스트 전에 테이블 확인
    def test_carcount(self):
        result = admin.carcount(1)
        check = 1
        self.assertEqual(result, check)
    
    def test_show_records(self):
        result = admin.show_records(0, 10)
        check = (
            ('test1', datetime.datetime(2016, 1, 1, 0, 0), None, 300000, 1, 'A10'),
            ('test2', datetime.datetime(2016, 1, 1, 0, 0), None, 300000, 1, 'B10'),
            ('test1', datetime.datetime(2013, 1, 1, 0, 0), datetime.datetime(2013, 1, 2, 0, 0), 10000, 0, 'A10'),
            ('test2', datetime.datetime(2013, 1, 1, 0, 0), datetime.datetime(2013, 1, 2, 0, 0), 10000, 0, 'B10'),
            )
        self.assertEqual(result, check)

    def test_count_records(self):
        result = admin.count_records()
        check = 4
        self.assertEqual(result, check)

    def test_advanced_search(self):
        result = admin.advanced_search(
            cardata='test1',
            in_datetime_start=datetime.datetime(2010, 1, 1, 0, 0),
            in_datetime_end=datetime.datetime(2018, 12, 31, 0, 0),
            out_datetime_start=datetime.datetime(2010, 1, 1, 0, 0),
            out_datetime_end=datetime.datetime(2018, 12, 31, 0, 0),
            cost_min=0,
            cost_max=300000,
            sectionno='A10',
            exists='0'
        ).children
        check = [
            ('carno', 'test1'),
            ('parkingtime__range', (datetime.datetime(2010, 1, 1, 0, 0), datetime.datetime(2018, 12, 31, 0, 0))),
            ('exittime__range', (datetime.datetime(2010, 1, 1, 0, 0), datetime.datetime(2018, 12, 31, 0, 0))),
            ('cost__range', (0, 300000)),
            ('sectionno', 'A10'),
            ('currexist', 0)
        ]
        self.assertEqual(result, check)

    # 유닛 테스트가 끝날때마다 새로 추가했던 데이터를 삭제합니다.
    def tearDown(self):
        sqldelete = """DELETE FROM parkinglot WHERE carNo = %s"""
        cursor.execute(sqldelete, 'test1')
        cursor.execute(sqldelete, 'test2')
        conn.commit()
        print('tearDown running')

if __name__ == '__main__':
    unittest.main()