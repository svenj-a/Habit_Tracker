import questionary
#from db import DB


class User:
  
    def __init__(self, name):
        self.username = name
        self.current_user = None

    def log_in(self, username):
        # enter username, if name in DB users table prompt password, if not then call create_profile
        pass
        pw = questionary.text("Enter your password:").ask()
        # if pw == the user corresponding pw extracted from DB, then:
        self.current_user = username

    def get_current_username(self):
        return self.current_user

    def create_profile(self, name):
        pass
  
    def delete_profile(self, name):
        pass
  
    def edit_profile(self, name):
        pass
