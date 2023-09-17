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
    return "Hello World!"

@app.route("/temp_json/<sensor_id>")
def temp_json1(sensor_id):
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute('select substr(temp_dt,1,4),substr(temp_dt,6,2),substr(temp_dt,9,2),substr(temp_dt,12,2),substr(temp_dt,15,2),temp from temp_log where sensor_id = ' + sensor_id + " order by 1")
    all = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(all)

@app.route("/temp_json/hourly")
def temp_json3():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=7) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    q = """select substr(temp_h,1,4),substr(temp_h,6,2),substr(temp_h,9,2),substr(temp_h,12,2),0,avg(temp) from 
(select substr(temp_dt,1,13) temp_h,temp from temp_log where sensor_id=3 and temp_dt > '""" + yesterday_string + """')
group by temp_h
order by 1"""
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute(q)
    all = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(all)

@app.route("/temp_json/daily")
def temp_json_daily():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=30) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    q = """select substr(temp_h,1,4),substr(temp_h,6,2),substr(temp_h,9,2),0,0,avg(temp) from 
(select substr(temp_dt,1,10) temp_h,temp from temp_log where sensor_id=3 and temp_dt > '""" + yesterday_string + """')
group by temp_h
order by 1"""
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute(q)
    all = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(all)

@app.route("/temp_json/last24")
def temp_json_last24():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=1) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")

    q = "select substr(temp_dt,1,4),substr(temp_dt,6,2),substr(temp_dt,9,2),substr(temp_dt,12,2),substr(temp_dt,15,2), temp from temp_log where sensor_id=3 and temp_dt > '" + yesterday_string + "' order by 1"

    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute(q)
    all = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(all)

@app.route("/temp_json/all")
def temp_json2():
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    q= """select dt, sum(t0),sum(t1),sum(t3) from
(select substr(temp_dt,1,16) dt,temp t0,0 t1,0 t3 from temp_log where temp_dt >= '2017-12-06' and sensor_id=0
union all
select substr(temp_dt,1,16) dt,0 t0,temp t1,0 t3 from temp_log where temp_dt >= '2017-12-06' and sensor_id=1
union all
select substr(temp_dt,1,16) dt,0 t0,0 t1,temp t3 from temp_log where temp_dt >= '2017-12-06' and sensor_id=3
)
group by dt order by 1"""
    c.execute(q)
    all = c.fetchall()
    c.close()
    conn.close()  
    return json.dumps(all)

@app.route("/light_json")
def light_json():
    now  =  datetime.now(timezone.utc) 
    yesterday = now - timedelta(days=25) 
    yesterday_string = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute("select substr(light_dt,1,4),substr(light_dt,6,2),substr(light_dt,9,2),substr(light_dt,12,2),substr(light_dt,15,2),light from light_log where light_dt > '" + yesterday_string + "' order by 1")
    all = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(all)

@app.route("/stir_json")
def stir_json():
    conn = sqlite3.connect(config.DBPATH)
    c = conn.cursor()
    c.execute('select stir_dt,result from stir_log order by 1 desc')
    all = c.fetchall()
    c.close()
    conn.close()
    return json.dumps(all)

@app.route("/temp_chart.html")
def temp_chart():
    json_url = config.base_url + "/temp_json/daily"
    return render_template('temp_chart_template.html', json_url=json_url, pagetitle="Daily Temperature chart",temp_active="active",base_url=config.base_url)

@app.route("/temp_chart_24h.html")
def temp_chart_24h():
    json_url = config.base_url + "/temp_json/last24"
    return render_template('temp_chart_template.html', json_url=json_url, pagetitle="Temperature chart 24H",temp_24h_active="active")

@app.route("/temp_chart_avg.html")
def temp_chart_avg():
    json_url = config.base_url + "/temp_json/hourly"
    return render_template('temp_chart_template.html', json_url=json_url, pagetitle="Hourly Temperature chart",temp_avg_active="active")

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


