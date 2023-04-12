import mysql.connector
import datetime
from dateutil import tz

db = mysql.connector.connect(
    host="localhost",username="root",
    password="",database="loopdb"
)

cur=db.cursor()

def get_timezone(store_id: str):
    cur.execute(f"Select timezone_str from store_timezone where store_id={store_id}")
    tz = cur.fetchall()
    if(len(tz)!=0):
        return tz[0][0]
    else:
        return "America/Chicago"


def get_business_hours(store_id: str,day: int):
    cur.execute(f"select start_time_local,end_time_local from menu_hours where store_id={store_id} and day={day}")
    res=cur.fetchall()
    if(len(res)!=0):

        start=res[0][0]
        end=res[0][1]
        return start,end
    else:
        return "00:00:00","23:59:59"

def get_store_status(store_id: str,d:str):
    d=datetime.date.fromisoformat(d)
    d=datetime.datetime(year=d.year,month=d.month,day=d.day)
    d=d.replace(tzinfo=tz.gettz('UTC'))
    d=d.astimezone(tz.gettz(get_timezone(store_id)))
    d=d.date()
    cur.execute(f"select distinct status,timestamp_utc from store_status where store_id={store_id} and timestamp_utc like '{d}%'")
    res=cur.fetchall()
    return res


