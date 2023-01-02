from flask import Flask, render_template, flash, request, url_for, redirect, session
import mysql.connector
from flask_session import Session



app=Flask(__name__, static_url_path='/static')

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="canyouseeme",
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
        sql12 ="SELECT patientFname,PatientLname,Adate,Pid FROM appointments WHERE (Doctor =%s)"
        val12=[k]
        mycursor.execute(sql12, val12)
        patients=mycursor.fetchall()
        sql13 ="SELECT PFname,PLname,oldAdate,oldPid FROM old_appointment WHERE (DR =%s)"
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
        # x=request.form['doctor']
        # y=request.form['date']
        # sql3="Insert into appointments(patientFname,Adate,Doctor,PatientLname,Pid)Values(%s,%s,%s,%s,%s)"
        # val3=(f[0],y,x,f[1],f[2])
        # mycursor.execute(sql3, val3)
        # mydb.commit()
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
      sql3="Insert into appointments(patientFname,Adate,Doctor,PatientLname,Pid)Values(%s,%s,%s,%s,%s)"
      val3=(f[0],y,x,f[1],f[2])
      mycursor.execute(sql3, val3)
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
@app.route('/admin')
def admin():
  
   return render_template('admin.html')


if __name__=='__main__':
    app.run(debug=True)