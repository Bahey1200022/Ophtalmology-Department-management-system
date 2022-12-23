from flask import Flask, render_template, flash, request, url_for, redirect, session
import mysql.connector




app=Flask(__name__)
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
 

   #5

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
        
@app.route('/loginPt',methods =['POST','GET'])
def loginPt():  
  return render_template('Patient.html') 


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
    if Ppassword !=Ppass2:
      return render_template('SignUpPt.html')
    else:
      return render_template('Patient.html')
    
  else:  
    return render_template('SignUpPt.html')

if __name__=='__main__':
    app.run()