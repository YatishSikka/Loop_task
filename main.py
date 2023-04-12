from fastapi import FastAPI
from report import uptime_last_hour, uptime_last_day, uptime_last_week
import random
import mysql.connector

app = FastAPI()


@app.get("/trigger_report/{store_id}")
def report_gen(store_id: str):
    conn=mysql.connector.connect(host="localhost",username="root", password="", database="loopdb")
    cur=conn.cursor()
    report_id=str(random.randint(1001,100000))
    hour_uptime,hour_downtime = uptime_last_hour(store_id)
    day_uptime,day_downtime = uptime_last_day(store_id)
    week_uptime,week_downtime = uptime_last_week(store_id)

    cur.execute(f"insert into reports values({report_id},{store_id},{hour_uptime},{day_uptime},{week_uptime},{hour_downtime},{day_downtime},{week_downtime})")
    conn.commit()
    return report_id

@app.get("/get_report/{report_id}")
def report_out(report_id: str):
    conn=mysql.connector.connect(host="localhost",username="root", password="", database="loopdb")
    cur=conn.cursor()
    cur.execute(f"select store_id,uptime_last_hour,uptime_last_day,uptime_last_week,downtime_last_hour,downtime_last_day,downtime_last_week from reports where report_id={report_id}")
    res=cur.fetchall()

    if(len(res)!=0):
        return "Success",{"store_id":res[0][0],
                "uptime_last_hour":res[0][1],
                "uptime_last_day":res[0][2],
                "uptime_last_week":res[0][3],
                "downtime_last_hour":res[0][4],
                "downtime_last_day":res[0][5],
                "downtime_last_week":res[0][6]}
    else:
        return "Running"

