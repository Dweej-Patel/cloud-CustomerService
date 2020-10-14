import pymysql
import os

pw = os.environ['dbuser']

c_info = {
    "host": "userservicesdb.c5wltorex9gc.us-east-1.rds.amazonaws.com",
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




