from flask import Flask,render_template,request,redirect,url_for,session
from sqlite3 import *
import numpy as np
from flask_mail import Mail,Message
from random import randrange
import pickle

app = Flask(__name__)
app.secret_key = "ayushrocks"

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "*******@gmail.com"
app.config['MAIL_PASSWORD'] = "*******"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
@app.route("/",methods = ["GET","POST"])
def dashboard():
	return render_template("dashboard.html")

@app.route("/home",methods = ["GET","POST"])
def home():
    if "username" in session:
        return render_template("home.html",name=session['username'])
    else:
        return redirect(url_for("login"))

@app.route("/logout",methods=["GET",'POST'])
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))

@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        un = request.form['un']
        pw = request.form['pw']
        con =None
        try:
            con = connect("ayush.db")
            cursor = con.cursor()
            sql = "select * from users where username = '%s' and password = '%s'"
            cursor.execute(sql % (un,pw))
            data = cursor.fetchall()
            if len(data) == 0:
                return render_template("login.html",msg="invalid login")
            else:
                session['username'] = un
                return redirect(url_for('home'))
        except Exception as e:
            msg = "issue" +e
            return render_template("signup.html",msg=msg)

        finally:
            if con is not None:
                con.close()
    else:
        return render_template("login.html")

@app.route("/signup",methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        un = request.form['un']

        try:
            con=connect("ayush.db")
            cursor=con.cursor()
            pw = ""
            text = "abcdefghijklmnopqrstuvwxyz"
            for i in range(6):
                pw = pw + text[randrange(len(text))]
            print(pw)
            sql = "insert into users values ('%s','%s')"
            cursor.execute(sql % (un,pw))
            con.commit()

            msg = Message("Welcome to Ayush tech",sender="s1032190095@gmail.com",recipients=[un])
            msg.body="Yr password is "+pw
            mail.send(msg)
            return redirect( url_for('login'))

        except Exception as e:
            con.rollback()
            return render_template("signup.html",msg="user already registerrd" + str(e))

        finally:
            if con is not None:
                con.close()


    else:
        return render_template("signup.html")

@app.route("/forgotpassword",methods=["GET","POST"])
def forgotpassword():
    if request.method == "POST":
        un = request.form["un"]
        con = None
        try:
            con = connect("ayush.db")
            cursor = con.cursor()
            sql = "select * from users where username = '%s'"
            cursor.execute(sql %(un))
            data=cursor.fetchall()
            if len(data) == 0:
                return render_template("fp.html",msg="Usr doesnot exists")
            else:
                pw = ""
                text = "abcdefghijklmnopqrstuvwxyz"
                for i in range(6):
                    pw = pw + text[randrange(len(text))]
                print(pw)
                sql = "update users set password = '%s' where username = '%s'"
                cursor.execute(sql % (pw,un))
                con.commit()

                msg = Message("Welcome to Ayush tech", sender="******@gmail.com", recipients=[un])
                msg.body = "Yr new password is " + pw
                mail.send(msg)
                return redirect(url_for('login'))
        except Exception as e:
            con.rollback()
            return render_template("fp.html", msg="Error -> "+str(e))

        finally:
            if con is not None:
                con.close()


    else:
        return render_template("fp.html")

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        # return render_template()
        
        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        data = np.array([temp_array])
        # my_prediction = int(model.predict(data)[0])


        with open("db2.model", "rb") as f:
            model = pickle.load(f)
        res = int(model.predict(data)[0])

        return render_template('result.html', lower_limit = res-10, upper_limit = res+5)

@app.route("/subs",methods = ["POST"])
def subs():
    em=request.form["em"]

    if request.form["btn"] == "Subscribe":
        con = None
        try:
            con=connect("ayush.db")
            cursor = con.cursor()
            sql = "select * from subs where email = '%s'"
            cursor.execute(sql % (em))
            data = cursor.fetchall()
            if len(data) == 0:
                sql = "insert into subs values ('%s')"
                cursor.execute(sql % (em))
                con.commit()
                msg = Message("Welcome to Tech ",sender="s1032190095@gmail.com",recipients=[em])
                msg.body = "Congrats For Yr Subscription"
                mail.send(msg)
                return render_template("dashboard.html",msg="U have been subscribed")
            else:
                return render_template("dashboard.html",msg="U have already subscribed")

        except Exception as e:
            if con is not  None:
                con.rollback()

            msg = "issue" +str(e)
            return render_template("dashboard.html",msg=msg)
        finally:
            if con is not None:
                con.close()

    if request.form["btn"] == "UnSubscribe":
        con = None
        try:
            con = connect("ayush.db")
            cursor = con.cursor()
            sql = "select * from subs where email = '%s'"
            cursor.execute(sql % (em))
            data = cursor.fetchall()
            print(data)
            if len(data) == 1:
                sql = "delete from subs where email = '%s'"
                cursor.execute(sql % (em))
                con.commit()
                msg = Message("Welcome to Tech ", sender="s1032190095@gmail.com", recipients=[em])
                msg.body = "U have been unsubscribed"
                mail.send(msg)
                return render_template("dashboard.html", msg="U have been un subscribed")
            else:
                return render_template("dashboard.html", msg="U are not subscribed")

        except Exception as e:
            if con is not None:
                con.rollback()

            msg = "issue" + str(e)
            return render_template("dashboard.html", msg=msg)
        finally:
            if con is not None:
                con.close()
            


if __name__ == "__main__":
    app.run(debug=True)