from flask import Flask, request, jsonify
import application as core
import json
import mysql.connector

LIMIT = 30

app = Flask(__name__)



def query(sql,parameter=None):
    con =  mysql.connector.connect(host="localhost",user="root",password="password",database="job_app")
    dbcursor = con.cursor(dictionary=True)
    if parameter == None:
        dbcursor.execute(sql)
    else:
        dbcursor.execute(sql,parameter)
    data = dbcursor.fetchall()
    dbcursor.close()
    con.close()
    return data



@app.route('/', methods=['GET'])
def index():
    return "<h4 style='text-align:center;margin-top:35vh;'>******* Job App API *******</h4>"


@app.route('/itparks', methods=['GET'])
def parks():
    try:
        sql = "SELECT DISTINCT park FROM itpark_jobs"
        plist = []
        parks = query(sql)
        for p in parks:
            plist.append({
                'key':p['park'],
                'display':p['park'].title()
            })
        res = {'status':True,'it_parks':plist,'message':''}
    except Exception as e:
        res = {'status':False,'it_parks':[],'message':str(e)}
    return json.dumps(res)

@app.route('/mncs', methods=['GET'])
def mncs():
    try:
        sql = "SELECT DISTINCT mnc FROM mnc_jobs"
        mncs = query(sql)
        plist = []
        for p in mncs:
            plist.append({
                'key':p['mnc'],
                'display':p['mnc'].title()
            })
        res = {'status':True,'mncs':plist,'message':''}
        
    except Exception as e:
        res = {'status':False,'mncs':[],'message':str(e)}
    return json.dumps(res)

@app.route('/itpark/jobs', methods=['POST'])
def park_job():
    try:
        req_data = request.get_json()
        sql = "SELECT * FROM itpark_jobs WHERE park = %s"
        parameter = (req_data['park'],)
        if('page' in req_data):
            first = int(req_data['page']) * 10
            last = LIMIT #first + 10
            sql = "SELECT * FROM itpark_jobs WHERE park = %s LIMIT {},{}".format(first,last)

        
        jobs = query(sql,parameter)
        res = {'status':True,'job_list':jobs,'message':''}
    except Exception as e:
        res = {'status':False,'job_list':[],'message':str(e)}
    return json.dumps(res)

@app.route('/mnc/jobs', methods=['POST'])
def mnc_job():
    try:
        req_data = request.get_json()
        sql = "SELECT * FROM mnc_jobs WHERE mnc = %s"
        parameter = (req_data['mnc'],)
        if('page' in req_data):
            first = int(req_data['page']) * 10
            last = LIMIT #first + 10
            sql = "SELECT * FROM mnc_jobs WHERE mnc = %s LIMIT {},{}".format(first,last)

        jobs = query(sql,parameter)
        res = {'status':True,'job_list':jobs,'message':'','length':len(jobs)}
    except Exception as e:
        res = {'status':False,'job_list':[],'message':str(e),'length':0}
    return json.dumps(res)
    
@app.route('/other/jobs', methods=['POST'])
def other_job():
    try:
        req_data = request.get_json()
        sql = "SELECT * FROM other_jobs"
        if('page' in req_data):
            first = int(req_data['page']) * 10
            last = LIMIT #first + 10
            sql = "SELECT * FROM other_jobs LIMIT {},{}".format(first,last)

        jobs = query(sql)
        res = {'status':True,'job_list':jobs,'message':'','length':len(jobs)}
    except Exception as e:
        res = {'status':False,'job_list':[],'message':str(e),'length':0}

    return json.dumps(res)

@app.route('/job/search', methods=['POST'])
def search_job():
    try:
        req_data = request.get_json()
        search_key = req_data['search']
        job_list =[]
        
        sql = "SELECT * FROM other_jobs WHERE title LIKE '%{}%' OR description LIKE '%{}%'".format(search_key,search_key)
        jobs = query(sql)
        job_list.extend(jobs)

        sql = "SELECT * FROM itpark_jobs WHERE title LIKE '%{}%' OR description LIKE '%{}%'".format(search_key,search_key)
        jobs = query(sql)
        job_list.extend(jobs)

        res = {'status':True,'job_list':job_list,'message':'','length':len(job_list)}
    except Exception as e:
        res = {'status':False,'job_list':[],'message':str(e),'length':0}
    return json.dumps(res)

if __name__ == '__main__':
    app.run()

