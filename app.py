from flask import Flask, request, jsonify
import application as core
import json
import mysql.connector

app = Flask(__name__)

con =  mysql.connector.connect(host="localhost",user="root",password="password",database="job_app")

dbcursor = con.cursor(dictionary=True)



@app.route('/', methods=['GET'])
def index():
    return "<h4 style='text-align:center;margin-top:35vh;'>******* Job App API *******</h4>"


@app.route('/itparks', methods=['GET'])
def parks():
    sql = "SELECT DISTINCT park FROM itpark_jobs"
    dbcursor.execute(sql)
    plist = []
    parks = dbcursor.fetchall()
    for p in parks:
        print(p)
        plist.append({
            'key':p['park'],
            'display':p['park'].title()
        })
    return json.dumps({'status':True,'it_parks':plist,'message':''})


@app.route('/mncs', methods=['GET'])
def mncs():
    sql = "SELECT DISTINCT mnc FROM mnc_jobs"
    dbcursor.execute(sql)
    mncs = dbcursor.fetchall()
    plist = []
    for p in mncs:
        plist.append({
            'key':p['mnc'],
            'display':p['mnc'].title()
        })
    return json.dumps({'status':True,'mncs':plist,'message':''})

@app.route('/itpark/jobs', methods=['POST'])
def park_job():
    try:
        req_data = request.get_json()
        sql = "SELECT * FROM itpark_jobs WHERE park = %s"
        parameter = (req_data['park'],)
        if('page' in req_data):
            first = int(req_data['page']) * 10
            last = 10 #first + 10
            sql = "SELECT * FROM itpark_jobs WHERE park = %s LIMIT {},{}".format(first,last)

        dbcursor.execute(sql,parameter)
        jobs = dbcursor.fetchall()
        return json.dumps({'status':True,'job_list':jobs,'message':''})
    except Exception as e:
        return json.dumps({'status':False,'job_list':[],'message':str(e)})
@app.route('/mnc/jobs', methods=['POST'])
def mnc_job():
    try:
        req_data = request.get_json()
        sql = "SELECT * FROM mnc_jobs WHERE mnc = %s"
        parameter = (req_data['mnc'],)
        if('page' in req_data):
            first = int(req_data['page']) * 10
            last = 10 #first + 10
            sql = "SELECT * FROM mnc_jobs WHERE mnc = %s LIMIT {},{}".format(first,last)

        dbcursor.execute(sql,parameter)
        jobs = dbcursor.fetchall()
        return json.dumps({'status':True,'job_list':jobs,'message':''})
    except Exception as e:
        return json.dumps({'status':False,'job_list':[],'message':str(e)})

@app.route('/other/jobs', methods=['POST'])
def other_job():
    try:
        sql = "SELECT * FROM other_jobs"
        if('page' in req_data):
            first = int(req_data['page']) * 10
            last = 10 #first + 10
            sql = "SELECT * FROM mnc_jobs LIMIT {},{}".format(first,last)

        dbcursor.execute(sql)
        jobs = dbcursor.fetchall()
        return json.dumps({'status':True,'job_list':jobs,'message':''})
    except Exception as e:
        return json.dumps({'status':False,'job_list':[],'message':str(e)})

@app.route('/job/search', methods=['POST'])
def search_job():
    try:
        req_data = request.get_json()
        search_key = req_data['search']
        job_list =[]
        sql = "SELECT * FROM other_jobs WHERE title LIKE '%{}%' OR description LIKE '%{}%'".format(search_key,search_key)
        print(sql)
        dbcursor.execute(sql)
    
        jobs = dbcursor.fetchall()
        job_list.append(jobs)

        sql = "SELECT * FROM itpark_jobs WHERE title LIKE '%{}%' OR description LIKE '%{}%'".format(search_key,search_key)
        dbcursor.execute(sql)
        jobs = dbcursor.fetchall()
        job_list.append(jobs)

        return json.dumps({'status':True,'job_list':job_list,'message':''})
    except Exception as e:
        return json.dumps({'status':False,'job_list':[],'message':str(e)})

if __name__ == '__main__':
    app.run()