import psycopg2
import json
from ..aws.secrets import get_secret_image_gallery
import os

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']

def get_dbname(secret):
    return secret['database_name']

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
   # connection = psycopg2.connect(host=os.environ['PG_HOST'], dbname=os.environ['IG_DATABASE'], user=os.environ['IG_USER'], password=os.environ['IG_PASSWD'])

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def delete_user_db(user):
    global connection
    cursor = connection.cursor()
    cursor.execute("DELETE from users where username=%s",(user,))
    cursor.close()
    return "user deleted"

def modify_user_og(username, new_password, new_name):
    global connection
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET password=%s, full_name=%s  where username=%s",(new_password, new_name, username))
    cursor.close()
    s = "Name and password updated"
    return s

def insert_user(username, password, fullname):
    global connection
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s);', (username, password, fullname))
    s = "Username Inserted"
    cursor.close()
    return s

def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)

if __name__ == "__main__":
    main()
