from flask import Flask, request, jsonify
import application as core
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "<h4 style='text-align:center;margin-top:35vh;'>******* Job App API *******</h4>"


@app.route('/technopark/jobs', methods=['GET'])
def technopark_job():
    jobs = core.generate_techno_park_jobs()
    return json.dumps(jobs)

@app.route('/infopark/jobs', methods=['GET'])
def infopark_job():
    jobs = core.generate_infopark_jobs()
    return json.dumps(jobs)

@app.route('/ulpark/jobs', methods=['GET'])
def ulpark_job():
    jobs = core.ulparkjobs()
    return json.dumps(jobs)


@app.route('/cyberpark/jobs', methods=['GET'])
def cyberpark_job():
    jobs = core.generate_cyberpark_jobs()
    return json.dumps(jobs)




@app.route('/technopark/job/details/', methods=["POST"])
def technopark_job_details():
    req = request.json
    details = core.technopark_job_details(req['ref_link'])
    return json.dumps(details)

@app.route('/infopark/job/details/', methods=["POST"])
def infopark_job_details():
    req = request.json
    details = core.infopark_job_details(req['ref_link'])
    return json.dumps(details)

@app.route('/ulpark/job/details/', methods=["POST"])
def ulpark_job_details():
    req = request.json
    details = core.ulpark_job_details(req['ref_link'])
    return json.dumps(details)

@app.route('/cyberpark/job/details/', methods=["POST"])
def cyberpark_job_details():
    req = request.json
    details = core.cyberpark_job_details(req['ref_link'])
    return json.dumps(details)

if __name__ == '__main__':
    app.run()