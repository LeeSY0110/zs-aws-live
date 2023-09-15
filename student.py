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
s3 = boto3.client('s3')


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

#View Student Information
@app.route("/studPage", methods=['GET','POST'])
def studPage():
    # cohort = request.form['cohort']
    # internPeriod = request.form['internPeriod']
    # studName = request.form['studName']
    # studId = request.form['studId']
    # studIc = request.form['studIc']
    # studGender = request.form['studGender']
    # programme = request.form['programme']
    #studEmail = request.form['studEmail']
    # studContact = request.form['studContact']
    # uniSupervisor = request.form['uniSupervisor']
    # uniEmail = request.form['uniEmail']
    companyName = request.form['companyName']
    companyAllowance = request.form['companyAllowance']
    companySvName = request.form['companySvName']
    companySvEmail = request.form['companySvEmail']
    studId = request.args.get('studId')
    companyApForm = request.files['companyApForm']
    parentAckForm = request.files['parentAckForm']
    letterOIdt = request.files['letterOIdt']
    hiredEvid = request.files['hiredEvid']
    

    #fetch_student_sql = "SELECT * FROM student WHERE studId = %s"
    sql = "UPDATE student SET companyName = %s AND companyAllowance = %s AND companySvName = %s AND companySvEmail = %s WHERE studId = %s"
    cursor = db_conn.cursor()

    try:
        # cursor.execute(fetch_student_sql, (studId))
        # records = cursor.fetchall()

        # if records == "":
        #     return render_template('studPage.html', invalid_error=True)
        cursor.execute(sql, (companyName, companyAllowance,companySvName, companySvEmail, studId,))
        db_conn.commit()
       
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "stud-id-" + str(studId) + "_file.pnf"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading files to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=companyApForm)
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=parentAckForm)
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=letterOIdt)
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=hiredEvid)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)
       
    finally:
        cursor.close()

    print("all modification done...")
    return render_template('StudPage.html')
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
