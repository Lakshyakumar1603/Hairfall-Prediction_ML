from flask import Flask,render_template,url_for,request
# print("Sucessfully imported")

import numpy as np 

#to import the ML Model 
import joblib
model=joblib.load("Hair_fall_Model_lgr.lb")
# print("Sucessfully Load the Model")

#Connect to mysql Data Base 
import mysql.connector as con

#create the Object of flask 
app=Flask(__name__)

# First Defualt route ("/")
@app.route("/")
def home():
    # return "servers stats sucessfully and Makes route "
    return render_template("form.html")

@app.route("/user_data",methods=["GET","POST"])
def user_data():
    if request.method=="POST":
        age=int(request.form["age"])
        gen=int(request.form["gen"])
        hc=int(request.form["hc"])
        mc=int(request.form["mc"])
        mt=int(request.form["mt"])
        nd=int(request.form["nd"])
        stress=int(request.form["stress"])
        wl=int(request.form["wl"])
        hl=int(request.form["hl"])
        
    #unseen Data points 
    id=0
    id=id+1
    data=[[id,age,gen,hc,mc,mt,nd,stress,wl]]
    
    
    #Prediction Work
    output = model.predict(data)
    output=output[0].ravel()
    output=int(output[0])
    if output==1:
        msg="Hair Fall"
    else:
        msg="No Hair Fall"
    
    main_data=(age,gen,hc,mc,mt,nd,stress,wl,int(output))
    #mysql connection work 
    conn=con.connect(
        host="localhost",
        user="root",
        password="",
        database="Hairfall"
    )
    
    #create the cursor object 
    cursor = conn.cursor()
    
    Qurey="insert into prediction(age,gen,hc,mc,mt,nd,stress,wl,phl) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(Qurey,main_data)
    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return msg
        

# The line if __name__ == "__main__": 
# ensures that the Flask application starts the server only when the script is executed directly, 
# not when the script is imported as a module into another script.
if __name__ == "__main__":
    #start a development server,which allows you to test your application.
    # The debug=True argument enables debugging mode, which provides helpful 
    # error messages and automatic reloading of the app when code changes.
    app.run(debug=True)

