from flask import Flask, request, render_template, session, redirect, flash, url_for
from ..data.user import User
from ..data.postgres_user_dao import PostgresUserDAO
from ..data.db import connect, delete_user_db, modify_user_og, insert_user
from functools import wraps
from ..aws.s3 import *
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/ec2-user/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'123'
connect()
@app.route('/')
def front_page():
    return redirect('/login')

@app.route('/invalidLogin')
def invalidLogin():
    return "Invalid"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_dao().get_user_by_username(request.form["username"])
        if user is None or user.password != request.form["password"]:
            return redirect('/invalidLogin')
        else:
            session['username'] = request.form["username"]
            return redirect('/mainMenu')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['username'] = ""
    session['password'] = ""
    return render_template('logout.html')

@app.route('/mainMenu')
def main_menu():
    return render_template('index.html')

def get_user_dao():
    return PostgresUserDAO()

@app.route('/admin/users')
def users():
    if not check_admin():
        return redirect('/login')
    return render_template('users.html', users=get_user_dao().get_users())

@app.route('/debugSession')
def debugSession():
    result = ""
    for key, value in session.items():
        result += key+"->"+str(value)+"<br />"
    return result

def check_admin():
    return 'username' in session and session['username'] == 'dongji'


@app.route('/admin')
def mainAdmin():
    if not check_admin():
        return redirect('/login')
    return render_template('admin.html', users=get_user_dao().get_users())


@app.route('/admin/delete/<string:user>')
def delete_user(user): 
    if not check_admin():
        return redirect('/login')
    delete_user_db(user)
    return mainAdmin()

@app.route('/admin/addUser')
def add_new_user():
    if not check_admin():
        return redirect('/login')
    return render_template('adduser.html')

@app.route('/uploadImage')
def upload_Image():
    return render_template('uploadImage.html')

@app.route('/uploads3', methods=['GET', 'POST'])
def uploads3():
    x = request.args['user_file']
    print(x)
    return mainAdmin()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadImage', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            directory_name = str(session["username"]) + "/" + filename 
            put_object('adkins-bucket-2', directory_name, file)
    return render_template('uploadImage.html')

@app.route('/viewImage')
def view_image():
    username = str(session["username"])   
    users = list_files('adkins-bucket-2', username)
    return render_template('viewImage.html', users=users, username=username)



@app.route('/admin/newUser')
def new_user():
    if not check_admin():
        return redirect('/login')
    y = request.args['user']
    x = request.args['fullname']
    z = request.args['password']
    insert_user(y, z, x)
    return mainAdmin()

@app.route('/admin/modifyUser/<string:user>/<string:password>/<string:fullname>')
def modifyUser(user, password, fullname):
    if not check_admin():
        return redirect('/login')
    return render_template('modifyuser.html', user=user, password=password, fullname=fullname)

@app.route('/admin/modifyUser')
def change_user():
    x = request.args['fullname']
    y = request.args['password']
    z = request.args['user']
    modify_user_og(z, y, x)
    return mainAdmin()
