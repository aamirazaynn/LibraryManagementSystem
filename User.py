
logged_in_user = None

class User:
    def __init__(self, firstName, lastName, userID, email, role, password):
        self.firstName = firstName
        self.lastName = lastName
        self.userID = userID
        self.email = email
        self.role = role
        self.password = password
    
    def get_firstName(self):
        return self.firstName
    
    def get_lastName(self):
        return self.lastName
    
    def get_userID(self):
        return self.userID
    
    def get_email(self):
        return self.email
    
    def get_role(self):
        return self.role
    
    def get_password(self):
        return self.password
    
    