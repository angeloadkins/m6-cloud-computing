from flask import Flask
from flask import request
from flask import render_template
from .user_admin import list_users, option_one, delete_user_db, insert_user, modify_user_og

app = Flask(__name__)

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

@app.route('/goodbye')
def goodbye():
    return 'Goodbye'

@app.route('/greet/<name>')
def greet(name):
    return 'Nice to meet you ' + name

@app.route('/add/<int:x>/<int:y>', methods = ['GET'])
def add(x, y):
    return 'The sum is ' + str(x + y)

@app.route('/mult', methods=['POST'])
def mult():
    x = request.form['x']
    y = request.form['y']
    return 'The product is ' + str(x*y)

@app.route('/calculator/<personsName>')
def calculator(personsName):
    return render_template('calculator.html', name=personsName)
   

@app.route('/admin')
def mainAdmin():
    list = list_users()
    return render_template('admin.html', numbers=list)

@app.route('/admin/hello')
def hello_test():
    return render_template('hello_test.html')

@app.route('/admin/delete/<string:user>')
def delete_user(user):
    delete_user_db(user)
    return mainAdmin()

@app.route('/admin/addUser')
def add_new_user():
    return render_template('adduser.html')

@app.route('/admin/newUser')
def new_user():
    y = request.args['user']
    x = request.args['fullname']
    z = request.args['password']
    insert_user(y, z, x)
    return mainAdmin()

@app.route('/admin/modifyUser/<string:user>/<string:password>/<string:fullname>')
def modifyUser(user, password, fullname):
    return render_template('modifyuser.html', user=user, password=password, fullname=fullname)

@app.route('/admin/modifyUser')
def change_user():
    x = request.args['fullname']
    y = request.args['password']
    z = request.args['user']
    modify_user_og(z, y, x)
    return mainAdmin()
