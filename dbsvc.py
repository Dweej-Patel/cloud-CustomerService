import pymysql
import os

pw = os.environ['dbuser']

c_info = {
    "host": "ec2-3-237-172-82.compute-1.amazonaws.com",
    "user": "admin",
    "password": pw,
    "cursorclass": pymysql.cursors.DictCursor,
}

conn = pymysql.connect(**c_info)
cur = conn.cursor()
res = cur.execute("show database;")
res = cur.fetchall()
