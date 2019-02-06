import pymongo
from flask import Flask, render_template, flash, request, url_for, redirect, session
from forms.sign_in import SignInForm
from forms.images import Images
from database import Database
from models.user import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config.from_object('config')


db= Database().db


@app.route('/')
def index():
    return render_template('index.html')
    #return render_template('main_page.html', username=session['username'] if 'username' in session else None)


@app.route('/view_results/', methods = ['GET', 'POST'])
def view_results():
    curr_user = 'fsdaf'
    #print(db.users.find({{"username":"fsdaf"}, {'$text': { '$search': "img_"}} }))
    users = db.users.find({})
    for user in users:
        if curr_user == user['username']:
            for item in user:
                if item[0:3] == 'img':
                    print("{}:{}".format(item,user[item]))

    all_requests = db.users.find_one({"username":"nba"})
    #print(all_requests['images'])
    return render_template('view_results.html', username = session['username'] if 'username' in session else None, requests=all_requests)


im=['fdsfads','fdsafdsa','fsdafdas']


@app.route('/sign_in/', methods=['GET', 'POST'])
#SIGN-UP
def sign_in():
    sign_in_form = SignInForm(request.form)
    print(request.method)
    if request.method == "POST":
        #if request.method == "POST" and sign_in_form.validate_on_submit():
        print('fdsafa')
        if not db.users.find_one({'username': sign_in_form.username.data}):
            user = User(sign_in_form.email.data, sign_in_form.username.data, sign_in_form.password.data)
            print(user.username)
            db.users.insert_one(user.json())
            session['username']= user.username
            session['email']= user.email
            print(session['username'])
            return render_template('view_results.html')
            #return redirect(url_for('index'))

        else:
            flash('username already exists')
            return render_template('sign_in.html', form=sign_in_form)
    return render_template('sign_in.html', form=sign_in_form)

@app.route('/login/', methods = ['GET','POST'])
def login_page():
    error = ''
    try:
        if request.method== "POST":
            print('fdsafdsafsdsda')
            attempted_username = request.form['username']
            attempted_password= request.form['psw']
            #attempted_email = request.form['email']

            flash(attempted_username)
            flash(attempted_password)
#

            if  db.users.find_one({u'username':"{}".format(attempted_username),u'password':attempted_password}):
                flash("found")
                session['username'] = attempted_username
                session['email'] = attempted_email
                return redirect(url_for('view_results'))
            else:
                error = "Not Valid Credentials. Try again."

        return render_template("login.html", error = error)

    except Exception as e:
        flash(e)
        return render_template("login.html", error= error)

    return render_template('login.html')


@app.route('/upload_photo/', methods=['GET', 'POST'])
def upload_photo():
    error = ''
    print(request.method)
    try:
        if request.method == 'POST':
            f = request.files['file']
            f.save(secure_filename("img_" + f.filename))
            new_image = Images("img_" + f.filename)
            print(new_image.url)
            #print(session['username'])
            #curr_user = session['email']
            curr_user = "fsdaf"
            #database = db.users.find_one({"username": curr_user})
            #db.users.updateOne({"username": curr_user, 'images': new_image.url })
            #db.users.updateOne({"username": curr_user}, {"$set"}: {"images": new_image.url})
            db.users.update({'username': curr_user}, {'$set': {new_image.url[:-4]: 0}})

            """
            for user in database:
                print(user)##
                if curr_user == user.username:
                    user['images'] = new_image
            
            user['images'] = new_image
            """
            return 'file uploaded successfully'

    except Exception as e:
        flash(e)
        return render_template("login.html", error=error)
    return render_template('upload_photo.html')


@app.route('/vote_page/', methods=["GET, POST"])
def vote_photo():
    if request.method == 'POST':
        curr_user = "guy"
        curr_photo = request.form('photo')
        f = request.form['username']
        db.users.update({'username': curr_user}, {"$inc": {curr_photo[:-4]: 1}})

if __name__ == '__main__':
    app.run()

