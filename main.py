from flask import Flask, render_template, flash, request, url_for, redirect, session
import mysql.connector
import time 



app=Flask(__name__, static_url_path='/static')
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
 

   
   #########################################################################
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
          
        
        
         
        
        return render_template('doctorsaddorview.html',data=r)
    else :
      return render_template('doctorslogin.html')    
     #########################################################################################################################################   
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
        data={'rec':r,'patient':f}
        if f==None:
          return render_template('Patient.html')
        else :
          return render_template('appointment.html',msg=data)
          
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

# @app.route('/book_an_appointment')
# def appoint():
#     sql="select* from doctor_availability"
#     mycursor.execute(sql)
    
#     r=mycursor.fetchall()
#     sql1 =
#     return render_template('appointment.html')
  
  

if __name__=='__main__':
    app.run()