import datetime
from database_data import get_business_hours, get_store_status,get_timezone
from dateutil import tz

def uptime_last_day(store_id: str):
    dt=datetime.datetime.now() - datetime.timedelta(days=1)
    start,end=get_business_hours(store_id,dt.weekday())

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(get_timezone(store_id))
    
    start = datetime.datetime.strptime(start, "%H:%M:%S")
    end = datetime.datetime.strptime(end, "%H:%M:%S")
    uptime=end-start
    downtime = datetime.timedelta(0,0,0)

    sts=get_store_status(store_id,str(dt.date()))
    sts.sort()
    for i in range(len(sts)):
         x = datetime.datetime.strptime(sts[i][1],"%Y-%m-%d %H:%M:%S")
         x = x.replace(tzinfo=from_zone)
         x = x.astimezone(to_zone)

         if(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='active'):
              continue
         elif(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='inactive' and i>0):
            if(sts[i-1][0]=='inactive'):
                y = datetime.datetime.strptime(sts[i-1][1],"%Y-%m-%d %H:%M:%S")
                y = y.replace(tzinfo=from_zone)
                y = y.astimezone(to_zone)
                uptime-=(datetime.datetime.time(x)-datetime.datetime.time(y))
                downtime+=(datetime.datetime.time(x)-datetime.datetime.time(y))
            elif(i<len(sts)-1 and sts[i-1][0]=='active' and sts[i+1][0]=='active' ):
                y = datetime.datetime.strptime(sts[i-1][1],"%Y-%m-%d %H:%M:%S")
                y = y.replace(tzinfo=from_zone)
                y = y.astimezone(to_zone)
                z = datetime.datetime.strptime(sts[i+1][1],"%Y-%m-%d %H:%M:%S")
                z = z.replace(tzinfo=from_zone)
                z = z.astimezone(to_zone)
                avg = (datetime.datetime.time(z)-datetime.datetime.time(x))/2
                uptime-=avg
                downtime+=avg
         elif(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='inactive' and i==0):
             uptime-=(datetime.datetime.time(x)-start.time())
             downtime+=(datetime.datetime.time(x)-start.time())
         elif(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='inactive' and i==len(sts)-1):
             uptime-=(end.time()-datetime.datetime.time(x))
             downtime+=(end.time()-datetime.datetime.time(x))

    return (uptime.total_seconds()/3600),(downtime.total_seconds()/3600)


def uptime_last_hour(store_id: str):
    dt = datetime.datetime.now()
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(get_timezone(store_id))
    dt = dt.replace(tzinfo=from_zone)
    dt = dt.astimezone(to_zone)
    last_hour = dt - datetime.timedelta(hours=1)
    uptime = datetime.timedelta(hours=1)
    downtime = datetime.timedelta(0,0,0)
    sts=get_store_status(store_id,str(dt.date()))
    sts.sort()
    start,end=get_business_hours(store_id,dt.weekday())

    start = datetime.datetime.strptime(start, "%H:%M:%S")
    end = datetime.datetime.strptime(end, "%H:%M:%S")
    for i in range(len(sts)):
        x = datetime.datetime.strptime(sts[i][1],"%Y-%m-%d %H:%M:%S")
        x = x.replace(tzinfo=from_zone)
        x = x.astimezone(to_zone)
        if(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='inactive'):
                if(datetime.datetime.time(last_hour) <= datetime.datetime.time(x) <= datetime.datetime.time(dt)):
                    if(0<i<len(sts)-1):
                        if(sts[i-1][0]=='inactive' and sts[i+1][0]=='inactive'):
                            uptime-=datetime.timedelta(hours=1)
                            downtime+=datetime.timedelta(hours=1)
                        elif(sts[i-1][0]=='inactive' and sts[i+1][0]=='active'):
                            uptime-=(datetime.datetime.time(x)-datetime.datetime.time(last_hour))
                            downtime+=(datetime.datetime.time(x)-datetime.datetime.time(last_hour))
                        elif(sts[i-1][0]=='active' and sts[i+1][0]=='inactive'):
                            uptime-=(datetime.datetime.time(dt)-datetime.datetime.time(x))
                            downtime+=(datetime.datetime.time(dt)-datetime.datetime.time(x))
                    else:
                        if(i==0 and sts[i+1][0]=='inactive'):
                            uptime-=(datetime.datetime.time(dt)-datetime.datetime.time(x))
                            downtime+=(datetime.datetime.time(dt)-datetime.datetime.time(x))
                        elif(i==len(sts)-1 and sts[i-1][0]=='inactive'):
                            uptime-=(datetime.datetime.time(x)-datetime.datetime.time(last_hour))
                            downtime+=(datetime.datetime.time(x)-datetime.datetime.time(last_hour))
    
    return (uptime.total_seconds()/60),(downtime.total_seconds()/60)



def uptime_last_week(store_id: str):
    dt = datetime.datetime.now()
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(get_timezone(store_id))
    dt = dt.replace(tzinfo=from_zone)
    dt = dt.astimezone(to_zone)

    last_week = dt - datetime.timedelta(days=7)
    cur_day = last_week

    uptime_week = datetime.timedelta(0,0,0)
    downtime = datetime.timedelta(0,0,0)
    while(cur_day<=dt):
            start,end=get_business_hours(store_id,cur_day.weekday())
            start = datetime.datetime.strptime(start, "%H:%M:%S")
            end = datetime.datetime.strptime(end, "%H:%M:%S")
            uptime=end-start
            sts=get_store_status(store_id,"2023-01-24")
            sts.sort()
            for i in range(len(sts)):
                x = datetime.datetime.strptime(sts[i][1],"%Y-%m-%d %H:%M:%S")
                x = x.replace(tzinfo=from_zone)
                x = x.astimezone(to_zone)

                if(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='active'):
                    continue
                elif(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='inactive' and i>0):
                    if(sts[i-1][0]=='inactive'):
                        y = datetime.datetime.strptime(sts[i-1][1],"%Y-%m-%d %H:%M:%S")
                        y = y.replace(tzinfo=from_zone)
                        y = y.astimezone(to_zone)
                        uptime-=(datetime.datetime.time(x)-datetime.datetime.time(y))
                        downtime+=(datetime.datetime.time(x)-datetime.datetime.time(y))
                    elif(i<len(sts)-1 and sts[i-1][0]=='active' and sts[i+1][0]=='active' ):
                        y = datetime.datetime.strptime(sts[i-1][1],"%Y-%m-%d %H:%M:%S")
                        y = y.replace(tzinfo=from_zone)
                        y = y.astimezone(to_zone)
                        z = datetime.datetime.strptime(sts[i+1][1],"%Y-%m-%d %H:%M:%S")
                        z = z.replace(tzinfo=from_zone)
                        z = z.astimezone(to_zone)
                        avg = (datetime.datetime.time(z)-datetime.datetime.time(x))/2
                        uptime-=avg
                        downtime+=avg
                elif(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='inactive' and i==0):
                    uptime-=(datetime.datetime.time(x)-start.time())
                    downtime+=(datetime.datetime.time(x)-start.time())
                elif(start.time() <= datetime.datetime.time(x) <= end.time() and sts[i][0]=='inactive' and i==len(sts)-1):
                    uptime-=(end.time()-datetime.datetime.time(x))
                    downtime+=(end.time()-datetime.datetime.time(x))
                
            uptime_week+=uptime
            cur_day+=datetime.timedelta(days=1)
    
    return (uptime_week.total_seconds()/3600),(downtime.total_seconds()/3600)



                     
        
