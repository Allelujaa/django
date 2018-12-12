import datetime
import unittest
from parkfunctions import admin, car, parkingsystem
import pymysql
import random

admin = admin()
parkingsystem = parkingsystem()

conn = pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')
cursor = conn.cursor()

class ExitTest(unittest.TestCase):
    def test_exit(self):
        timelist = list()
        totaltime = 0
        for i in range(0, 10):
            carno = 'newtest1'
            #insert
            sql = """INSERT INTO
                            parkinglot(carNo, sectionNo, parkingTime, currExist)
                            VALUES(%s, %s, %s, %s)"""
            cursor.execute(sql, (carno, "A10", datetime.datetime(2018, 12, 10), 1))
            sql2 = """
                    UPDATE currParkinglot
                    SET carNo = %s, currExist = %s
                    WHERE sectionNo = %s
                    """
            cursor.execute(sql2, (carno, 1, "A10"))
            conn.commit()


            
            client = car(carno, parkingsystem)

            start = datetime.datetime.now()
            result = client.car_out()
            end = datetime.datetime.now()
            exectime = (end - start).total_seconds()
            timelist.append(exectime)

            self.assertEqual(result, None)
            
            totaltime += exectime
            del client

            sql = """
                DELETE FROM parkinglot WHERE carNo = %s
                """
            cursor.execute(sql, carno)
            conn.commit()
        
        for i in range(0, 10):
            print("EXIT TIME ", i, ": ", timelist[i], " seconds")
        print("AVERAGE TIME: ", totaltime/10, "seconds")

if __name__ == '__main__':
    unittest.main()