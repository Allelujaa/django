import os
import pymysql

def con():
    if os.environ.get('CHECK_INSTANCE'):
        db_user = os.environ.get('CLOUD_SQL_USERNAME')
        db_password = os.environ.get('CLOUD_SQL_PASSWORD')
        db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
        db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        return pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
    
    else:
        return pymysql.connect(host='localhost', port=3306, user = 'root', password='2018', database = 'project7')