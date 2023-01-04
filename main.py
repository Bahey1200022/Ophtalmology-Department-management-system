from flask import Flask, render_template, flash, request, url_for, redirect, session,send_file
import mysql.connector
from flask_session import Session
from io import BytesIO
#


app=Flask(__name__, static_url_path='/static')

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="palmhome",
  database="optha"
)

mycursor = mydb.cursor()

@app.route('/')
def home():
   return render_template('p1.html')
 

   
   ############################################################################################################################################################3
@app.route('/loginDr',methods =['POST','GET'])
def loginDr():
    if request.method =='POST':
        n=request.form['x']
        d=request.form['y']
        sql="SELECT * FROM doctors WHERE (email=%s AND password =%s)"
        val=(n,d)
        mycursor.execute(sql, val)
        r=mycursor.fetchone()
        if r==None:
          return render_template('doctorslogin.html')
        k=r[1]
        sql12 ="SELECT patientFname,PatientLname,Adate,Pid,status FROM appointments WHERE (Doctor =%s)"
        val12=[k]
        mycursor.execute(sql12, val12)
        patients=mycursor.fetchall()
        sql13 ="SELECT PFname,PLname,oldAdate,oldPid,old_status FROM old_appointment WHERE (DR =%s)"
        val13=[k]
        mycursor.execute(sql13, val13)
        oldappointments=mycursor.fetchall()
        dr={"drname":k,"p":patients,"oldp":oldappointments}
        
         
        
        return render_template('doctorsaddorview.html',data=dr)
    else :
      return render_template('doctorslogin.html')    
     #########################################################################################################################################  ################################################# 
@app.route('/loginPt',methods =['POST','GET'])
def loginPt():
  if request.method =='POST':
        n=request.form['Patient_Email']
        d=request.form['Patient_Password']
        sql="SELECT * FROM patients WHERE (email=%s AND passpatient =%s)"
        val=(n,d)
        mycursor.execute(sql, val)
        f=mycursor.fetchone()
        sql1="select* from doctor_availability"
        mycursor.execute(sql1)
  
        
        #rowheaders=[x[0] for x in mycursor.description ]
        r=mycursor.fetchall()
        data1={"rec":r,"patient":f}
        session['p']=f
        if f==None:
          return render_template('Patient.html')
        else :
          return render_template('appointment.html',msg=data1)
          
  return render_template('Patient.html') 

###############################################################################################################################################
@app.route('/SignUpPt',methods =['POST','GET'])
def SignUpPt():
  if request.method =='POST':
    Fname=request.form['Patient_FName']
    lname=request.form['Patient_LName']
    mob=request.form['Patient_Mobile']
    pbd=request.form['Patient_BirthDay']
    pemail=request.form['Patient_Email']
    Ppassword=request.form['Patient_Password']
    Ppass2=request.form['Patient_Password_ReEntered']
    disease=request.form['Patient_Diseases']
    fileP=request.form['Patient_Data']
    ephone=request.form['Patientrelative_Mobile']
    insurance=request.form['insurance']
    gender =request.form['gender']
    address=request.form['ad']
    if Fname =="" or lname=="" or pemail=="" or mob=="" or Ppass2=="" or Ppassword=="" or gender=="" or Ppassword !=Ppass2:
        return render_template('SignUpPt.html')
    else:
      sql1="INSERT INTO patients(PFname,PLname,Mnum,Enum,Sex,DOT,Address,email,passpatient,insuranceN,diseases,MR) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      val1=(Fname,lname,mob,ephone,gender,pbd,address,pemail,Ppassword,insurance,disease,fileP)
      mycursor.execute(sql1, val1)
      mydb.commit()
      return render_template('Patient.html')
    
  else:  
    return render_template('SignUpPt.html')
###############################################################################################################################################################################

@app.route('/booking_successful',methods =['POST','GET'])
def appoint():
    f=session.get('p',None)
    if request.method =='POST':
      f=session.get('p',None)
      x=request.form['doctor']
      y=request.form['date']
      z=request.form['stat']
      sql3="Insert into appointments(patientFname,Adate,Doctor,PatientLname,Pid,status)Values(%s,%s,%s,%s,%s,%s)"
      val3=(f[0],y,x,f[1],f[2],z)
      mycursor.execute(sql3, val3)
      mydb.commit()
      sql4="UPDATE patients SET AssignedDr=%s WHERE PID=%s"
      val4=(x,f[2])
      mycursor.execute(sql4, val4)
      mydb.commit()
      return render_template('p1.html')
    else:
      return render_template('aboutus.html')
        
##################################################################################################################################################        
@app.route('/aboutus')
def aboutuss():
   return render_template('aboutus.html')
 
################################################################################################################################################################################333 
@app.route('/doctors')
def doctorss():
   return render_template('Doctors.html')  
###################################################################################################################################################################
@app.route('/contactus')
def contactus():
   return render_template('contactus.html')  
 
######################################################################################################################################### 
@app.route('/prices')
def prices():
   return render_template('prices.html') 
 

 ###############################################################################
@app.route('/complaints',methods =['POST','GET'])
def complaints():
  if request.method =='POST':
    email=request.form['email']
    passw=request.form['passw']
    complaint=request.form['text']
    sql="Select PFname,PLname,PID from patients WHERE(email=%s AND passpatient=%s)"
    val=(email,passw)
    mycursor.execute(sql, val)
    p=mycursor.fetchone()
    sql2="INSERT INTO complaints(Complaint,PatientID,Pfname,Plname)Values(%s,%s,%s,%s)"
    val2=(complaint,p[2],p[0],p[1])
    mycursor.execute(sql2, val2)
    mydb.commit()
    return render_template('p1.html')
  else :
    return render_template('complaints.html')


###########################################################################################################################################################################3
@app.route('/cancellation_done',methods =['POST','GET'])
def cancel():
  if request.method =='POST':
      f=session.get('p',None)
      x=request.form['doctor']
      y=request.form['date']
      sql="DELETE FROM appointments WHERE (patientFname=%s AND Adate=%s AND Doctor=%s AND PatientLname=%s) "
      val=(f[0],y,x,f[1])
      mycursor.execute(sql, val)
      mydb.commit()
      sql4="UPDATE patients SET AssignedDr=NULL WHERE PID=%s"
      val4=[f[2]]
      mycursor.execute(sql4, val4)
      mydb.commit()
      return render_template('p1.html')
  else:
      return render_template('aboutus.html')
  


############################################################################################################################################################
@app.route('/admin',methods =['POST','GET'])
def admin():
  if request.method =='POST':
    admin=request.form['x']
    passw=request.form['y']
    # mycursor.execute("SELECT * FROM appointments")
    # data=mycursor.fetchall()
    if admin=="admin" and passw=="dbdemo":
      return redirect('/view_appointments')
    else:
      return render_template('adminlogin.html')
  else:
    return render_template('adminlogin.html')
 ##############################################################################################################################################################################     
@app.route('/view_appointments')
def viewapp():
  mycursor.execute("SELECT * FROM appointments")
  data=mycursor.fetchall()
  return render_template('admin.html',msg=data)
  
###############################################################################################################  
@app.route('/appointment_marked',methods=['POST','GET'])
def complete():
  if request.method =='POST':
    fname=request.form['Pfname']
    lname=request.form['Plname']
    date=request.form['date']
    pid=request.form['id']
    dr=request.form['dr']
    s=request.form['stat']
    sql2="Delete from appointments WHERE (patientFname=%s) "
    val2=[fname]
    mycursor.execute(sql2, val2)
    mydb.commit()
    sql1="INSERT INTO old_appointment(PFname,PLname,oldPid,oldAdate,DR,old_status) VALUES(%s,%s,%s,%s,%s,%s)"
    val1=(fname,lname,pid,date,dr,s)
    mycursor.execute(sql1, val1)
    mydb.commit()
    # sql2="DELETE FROM appointments WHERE (patientFname=%s AND Adate=%s AND Doctor=%s AND PatientLname=%s) "
    # val2=(fname,date,dr,lname)
    # mycursor.execute(sql2, val2)
    # mydb.commit()
    return redirect('/old_appointments')
  else:
    return render_template('admin.html')
#########################################################################################
@app.route('/old_appointments',methods=['GET'])
def retrieve():
  mycursor.execute("SELECT * FROM old_appointment")
  r=mycursor.fetchall()
  return render_template('oldapp.html',data=r)
###############################################################################################################################################    
@app.route('/plist',methods=['GET'])
def p():
  mycursor.execute("SELECT * FROM patients")
  r=mycursor.fetchall()
  mycursor.execute("SELECT MR FROM patients ")
    #row_headers=[x[0] for x in mycursor.description] #this will extract row headers
  r2 = mycursor.fetchall()
  data1={
    "rec":r,"rr":r2
  }
  
  
  return render_template('patient_table.html',data=data1)
 
 ####################################################3333333333333333333333333333333333333333333333333      
app.route('/download/<fileId>')#href="http://127.0.0.1:5000/download/{{r[0]}}" 
def downloadFile(fileId):
    
    mycursor.execute("SELECT PFNAME, MR FROM patients ")
    #row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    file_data = mycursor.fetchall()
    return send_file(BytesIO(file_data[0]),attachment_filename=file_data[1], as_attachment=True)
##############################################################################################3333
@app.route('/Nurses')
def nurses():
  mycursor.execute("SELECT * FROM nurses")
  r=mycursor.fetchall()
  return render_template('nurses.html',msg=r)
#####################################################################################################  

@app.route('/nurse_added',methods=['POST','GET']) 
def nurseadd():
  if request.method =='POST':
    fname=request.form['Pfname']
    g=request.form['sex']
    date=request.form['date']
    salary=request.form['salary']
    ssn=request.form['ssn']
    number=request.form['number']
    sql="INSERT INTO nurses(NName,Gender,SSN,Birthdate,salary,phoneN)Values(%s,%s,%s,%s,%s,%s)"
    val=(fname,g,date,salary,ssn,number)
    mycursor.execute(sql,val)
    mydb.commit()
    # mycursor.execute("SELECT * FROM nurses")
    # r=mycursor.fetchall()
    return redirect('/Nurses')
#################################################################################################################  
@app.route('/prices')
def knowprice():
  return render_template('prices.html')
######################################################################################################################################3       
@app.route('/viewdoctors')  
def dr():
  mycursor.execute("SELECT * FROM doctors")
  r=mycursor.fetchall()
  return render_template('doctorslist.html',msg=r)
############################################################
@app.route('/doctor_added',methods=['POST','GET'])
def addoc():
  if request.method =='POST':
    name=request.form['Pfname']
    g=request.form['sex']
    date=request.form['dep']
    salary=request.form['salary']
    ssn=request.form['ssn']
    number=request.form['number']
    email=request.form['email']
    passw=request.form['passw']
    add=request.form['ad']
    sql="INSERT INTO doctors(Dname,Dphone,SSN,Address,Salary,email,password,Department,Sex)Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(name,number,ssn,add,salary,email,passw,date,g)
    mycursor.execute(sql,val)
    mydb.commit()
    return redirect('/viewdoctors')
  ############################################################################################################################
@app.route('/viewcomplaints')
def viewcomplaints():
  sql=mycursor.execute("SELECT * FROM complaints")
  r=mycursor.fetchall()
  return render_template('viewcomplaints.html',msg=r)
#############################################################
@app.route('/complain_received',methods=['POST','GET'])
def complainread():
  if request.method =='POST':
    id=request.form['id']
    status=request.form['status']
    sql="Update complaints SET status=%s WHERE idComplaints=%s"
    val=(status,id)
    mycursor.execute(sql,val)
    mydb.commit()
    return redirect('/viewcomplaints')
  ######################################################################################
##############################################################################################  
@app.route('/equipments')  
def equip():
  mycursor.execute("SELECT * FROM devices")
  r=mycursor.fetchall()
  return render_template('viewequipments.html',msg=r)
##################################################################################################
@app.route('/dev_added',methods=['POST','GET'])
def addeq():
  if request.method =='POST':
    name=request.form['name']
    serialn=request.form['sn']
    companyn=request.form['cn']
    stat=request.form['stat']
    sql="INSERT INTO devices (serialn,name,conum,status)Values(%s,%s,%s,%s)"
    val=(serialn,name,companyn,stat)
    mycursor.execute(sql,val)
    mydb.commit()
    return redirect('/equipments') 
##############################################################################################################################  
@app.route('/dev_status',methods=['POST','GET'])
def changes():
  if request.method =='POST':
    serialn=request.form['s']
    stat=request.form['stat2']
    sql1="Update devices SET status=%s WHERE serialn=%s"
    val1=(stat,serialn)
    mycursor.execute(sql1,val1)
    mydb.commit()
    mycursor.execute("SELECT * FROM devices")
    r=mycursor.fetchall()
    return render_template('viewequipments.html',msg=r)
  else:
    return redirect('/equipments')
#####################################################################################################################################################################################
@app.route('/deleteequip',methods =['POST','GET'])
def delequipment():
  if request.method =='POST':
    x=request.form['s']
    sql2="DELETE FROM devices WHERE name=%s"
    val2=[x]
    mycursor.execute(sql2,val2)
    mydb.commit()
    return redirect('/equipments')
  else:
    return redirect('/equipments')    
###################################################################3333  
    
  
  
  

if __name__=='__main__':
    app.run(debug=True)