import application as core
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

core.save_qburst()
core.technopark_save()
core.infopark_save()
core.cyberpark_save()

# db  = core.get_db()
# db.row_factory = dict_factory

# sql = 'select * from "mnc-jobs"'

# mycursor = db.cursor()

# mycursor.execute(sql)
# myresult = mycursor.fetchall()
# # print(myresult)
# print(json.dumps({'status':True,'job_list':myresult,'message':''}))