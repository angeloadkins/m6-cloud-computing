class User:
    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    
    def __repr__(self):
        return "Username with usernme: " + self.username + "password: " + self.password + "full name: " + self.full_name
