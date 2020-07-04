from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
#from .user_admin import list_users, option_one
from ..data.user import User
from ..data.postgres_user_dao import PostgresUserDAO
from ..data.db import connect, delete_user_db, modify_user_og, insert_user
from functools import wraps

app = Flask(__name__)
app.secret_key = b'123'
connect()
@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html>
   <head>
      <title>Hello</title>
      <meta charset="utf-8" />
   </head>
   <body>
     <h1>Hello, Angelo!</h1>
   </body>
</html>
"""

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
            return redirect('/admin')
    else:
        return render_template('login.html')

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
    return 'username' in session and session['username'] == 'steve'


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
