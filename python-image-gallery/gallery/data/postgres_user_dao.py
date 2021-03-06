from . import db 
from .user import User 
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass
    
    def get_users(self):
        results = []
        cursor = db.execute("select username, password, full_name from users")
        for t in cursor.fetchall():
            results.append(User(t[0], t[1], t[2]))
        return results

    def get_user_by_username(self, username):
        cursor = db.execute("select username, password, full_name from users where username=%s",(username,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return User(row[0], row[1], row[2])
