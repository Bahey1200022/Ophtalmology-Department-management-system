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
        


if __name__=='__main__':
    app.run()