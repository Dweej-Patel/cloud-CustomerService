import pymysql
from db_config import *

c_info = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}

conn = pymysql.connect(**c_info)
cur = conn.cursor()


def getDbConnection(sql):
    res = cur.execute(sql)
    print(res)
    if res == 0:
        return res
    res = cur.fetchall()
    print(res)
    return res




