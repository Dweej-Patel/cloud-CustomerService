import pymysql
import os

pw = os.environ['dbuser']
host = os.environ['dbhost']

c_info = {
    "host": host,
    "port": 3306,
    "user": "admin",
    "password": pw,
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}

conn = pymysql.connect(**c_info)
cur = conn.cursor()


def getDbConnection(sql):
    res = cur.execute(sql)
    res = cur.fetchall()
    return res




