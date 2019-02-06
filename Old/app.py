import smtplib

from flask import Flask, render_template, flash, request, url_for, redirect, session
from util.database import *
from util.pyrest import *
from forms.sign_in import SignInForm
from models.user import *


app = Flask(__name__)
app.config.from_object('config')
#db= Database().db
#app.config mongo
###########3
#mongo=pymongo(ap#p)

#print(db.collection_names())

@app.route('/', methods=['GET', 'POST'])
def index():
   #all_requests = db.Tasks.find({})
   print
    return render_template('index.html', username = session['username'] if 'username' in session else None, requests=all_requests)

@app.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    sign_in_form = SignInForm(request.form)
    print(request.method)
    if request.method == "POST" and sign_in_form.validate_on_submit():
        print('fdsafa')
        if not db.users.find_one({'username': sign_in_form.username.data}):
            user = User(sign_in_form.email.data, sign_in_form.username.data, sign_in_form.password.data)
            db.users.insert_one(user.json())
            session['username']= user.username
            session['email']= user.email
            return redirect(url_for('index'))
        else:
            flash('username already exists')
            return render_template('sign_in.html', form=sign_in_form)
    return render_template('sign_in.html', form=sign_in_form)


@app.route('/login/', methods = ['GET','POST'])
def login_page():
    error = ''
    try:
        if request.method== "POST":
            attempted_username = request.form['username']
            attempted_password= request.form['psw']
            attempted_email = request.form['email']

            flash(attempted_username)
            flash(attempted_password)
        """
            if  db.users.find_one({u'username':"{}".format(attempted_username),u'password':attempted_password}):
                flash("found")
                session['username'] = attempted_username
                session['email'] = attempted_email
                return redirect(url_for('index'))
            else:
                error = "Not Valid Credentials. Try again."

        return render_template("login.html", error = error)
"""
    except Exception as e:
        flash(e)
        return render_template("login.html", error= error)

    return render_template('login.html')

@app.route('/newrequest/', methods = ['GET','POST'])
def newrequest():
    if request.method == "POST":
        requestname = request.form['requestname']

        description = request.form['description']
        task = Task(requestname, session['username'], description, session['email']).json()
        print(task.items())
        db.Tasks.insert_one(task)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



#####



if __name__ == '__main__':
   app.run(debug=app.config['DEBUG'])
