from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(   #Check the info is correct
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'student'


#if call / then will redirect to this pg
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('StudLogin.html')

#if call /studLogin then will redirect to this pg
# @app.route("/companyLogin")
# def compnayLogin():
#     return render_template('CompanyLogin.html') 

#if call /studView then will redirect to this pg
# @app.route("/studView", methods=['POST'])
# def companyReg():
#     companyName = request.form['companyName']
#     companyEmail = request.form['companyEmail']
#     companyContact = request.form['companyContact']
#     companyAddress = request.form['companyAddress']
#     typeOfBusiness = request.form['typeOfBusiness']
#     numOfEmployee = request.form['numOfEmployee']
#     overview = request.form['overview']
#     companyPassword = request.form['companyPassword']
#     status = "Pending Approval"

   
#     insert_sql = "INSERT INTO company VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     cursor = db_conn.cursor()

     

#     try:

#         cursor.execute(insert_sql, (companyName, companyEmail, companyContact, companyAddress, typeOfBusiness, numOfEmployee, overview, companyPassword, status))
#         db_conn.commit()
        

#     except Exception as e:
#         return str(e) 
        

#     finally:
#         cursor.close()

#     print("all modification done...")
#     return render_template('CompanyLogin.html')


@app.route("/studLogin", methods=['GET', 'POST'])
def studLogin():
    studEmail = request.form['studEmail']
    studIc = request.form['studIc']
    #status = "Pending Approval"


    fetch_student_sql = "SELECT * FROM student WHERE studEmail = %s"
    #fetch_company_sql = "SELECT * FROM company WHERE status = %s"
    cursor = db_conn.cursor()

    if studEmail == "" and studIc == "":
        return render_template('StudLogin.html', empty_field=True)

    try:
        cursor.execute(fetch_student_sql, (studEmail))
        records = cursor.fetchall()

        # cursor.execute(fetch_company_sql, (status))
        # companyRecords = cursor.fetchall()

        if records and records[0][4] != studIc:
            return render_template('StudLogin.html', login_failed=True)
        else:
            return render_template('StudPage.html', student=records)

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
