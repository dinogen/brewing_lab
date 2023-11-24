from flask import Flask, render_template,request
import json
import sqlite3
import config
from datetime import datetime,timezone,timedelta
from timeconv import hhmm2secs, secs2hhmm

config.readConfig()

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('splash_template.html', pagetitle="Brewing Lab Web")

@app.route("/temp_json/<sensor_id>")
def temp_json1(sensor_id):
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute('select substr(temp_dt,1,4),substr(temp_dt,6,2),substr(temp_dt,9,2),substr(temp_dt,12,2),substr(temp_dt,15,2),temp from temp_log where sensor_id = ' + sensor_id + " order by 1")
    rows = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(rows)

@app.route("/temp_json/hourly")
def temp_json3():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=7) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    q = """select substr(temp_h,1,4),substr(temp_h,6,2),substr(temp_h,9,2),substr(temp_h,12,2),0,avg(temp) from 
(select substr(temp_dt,1,13) temp_h,temp from temp_log where sensor_id=3 and temp_dt > '""" + yesterday_string + """')
group by temp_h
order by 1,2,3,4"""
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute(q)
    rows = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(rows)

@app.route("/temp_json/daily")
def temp_json_daily():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=30) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    q = """select substr(temp_h,1,4),substr(temp_h,6,2),substr(temp_h,9,2),0,0,avg(temp) from 
(select substr(temp_dt,1,10) temp_h,temp from temp_log where sensor_id=3 and temp_dt > '""" + yesterday_string + """')
group by temp_h
order by 1,2,3"""
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute(q)
    rows = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(rows)

@app.route("/temp_json/last24")
def temp_json_last24():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=1) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")

    q = """select substr(temp_dt,1,4),substr(temp_dt,6,2),substr(temp_dt,9,2),substr(temp_dt,12,2),substr(temp_dt,15,2), temp 
    from temp_log 
    where sensor_id=3 and temp_dt > '""" + yesterday_string + """' 
    order by 1,2,3,4,5"""

    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute(q)
    rows = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(rows)

@app.route("/temp_json/all")
def temp_json2():
    now  =  datetime.now(timezone.utc) 
    past = now - timedelta(days=30) 
    past_string = past.strftime("%Y-%m-%d %H:%M:%S")

    q = """SELECT y,m,d,hh,mm,sum(temp1), sum(temp2), sum(temp3)
from 
(select substr(temp_dt,1,4) as y,substr(temp_dt,6,2) as m,substr(temp_dt,9,2) as d,substr(temp_dt,12,2) as hh,substr(temp_dt,15,2) as mm,
  case sensor_id
    when 0 then temp
    else 0 
    end as temp1,
  case sensor_id
    when 1 then temp
    else 0 
    end as temp2,
  case sensor_id
    when 3 then temp
    else 0 
    end as temp3
  from temp_log 
  where temp_dt > '""" + past_string + """') T
  group by y,m,d,hh,mm
order by 1,2,3,4,5"""

    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute(q)
    rows = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(rows)

@app.route("/light_json")
def light_json():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=25) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute("select substr(light_dt,1,4),substr(light_dt,6,2),substr(light_dt,9,2),substr(light_dt,12,2),substr(light_dt,15,2),light from light_log where light_dt > '" + yesterday_string + "' order by 1")
    rows = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(rows)

@app.route("/stir_json")
def stir_json():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=15) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute("select stir_dt,result from stir_log where stir_dt > '" + yesterday_string + "' order by 1 desc")
    rows = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(rows)

@app.route("/temp_chart.html")
def temp_chart():
    json_url = config.base_url + "/temp_json/all"
    return render_template('three_sensors_chart_template.html', 
                           json_url=json_url, 
                           agetitle="Last month Temperature chart",
                           temp_active="active",
                           base_url=config.base_url)

@app.route("/temp_chart_24h.html")
def temp_chart_24h():
    json_url = config.base_url + "/temp_json/last24"
    return render_template('one_sensor_chart_template.html', json_url=json_url, pagetitle="Temperature chart 24H",temp_24h_active="active")

@app.route("/temp_chart_avg.html")
def temp_chart_avg():
    json_url = config.base_url + "/temp_json/hourly"
    return render_template('one_sensor_chart_template.html', json_url=json_url, pagetitle="Hourly Temperature chart",temp_avg_active="active")

@app.route("/stir_chart.html")
def stir_chart():
    json_url = config.base_url + "/stir_json"
    return render_template('stir_chart_template.html', json_url=json_url, pagetitle="Stirring log",onloadfunction="drawChart()",stir_active="active")

@app.route("/light_chart.html")
def light_chart():
    json_url = config.base_url + "/light_json"
    return render_template('light_chart_template.html', json_url=json_url, pagetitle="Light chart",light_active="active")

@app.route("/config.html", methods=['GET','POST'])
def config_page():
    config.readConfig()
    if request.method == 'POST':
        try: 
            config.STIR_TIME = int(request.form['stir_time'])
        except:
            config.STIR_TIME = 0
        try:
            config.ideal_temp = int(request.form['ideal_temp'])
        except:
            config.ideal_temp = 21
        config.STIR_DELAY = hhmm2secs(request.form['stir_delay'])
        config.TEMP_DELAY = hhmm2secs(request.form['temp_delay'])
        config.HEAT_DELAY = hhmm2secs(request.form['heat_delay'])
        config.writeConfig()
    stir_delay = secs2hhmm(config.STIR_DELAY)
    temp_delay = secs2hhmm(config.TEMP_DELAY)
    heat_delay = secs2hhmm(config.HEAT_DELAY)
    return render_template('config_template.html', \
        pagetitle="Configuration", \
        config_active="active", \
        stir_time=config.STIR_TIME, \
        stir_delay=stir_delay, \
        temp_delay=temp_delay, \
        heat_delay=heat_delay, \
        ideal_temp=config.ideal_temp, \
        config=config)


