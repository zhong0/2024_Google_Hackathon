from dao.AthuDao import AthuDao
import utils.Const as const
import bcrypt

class AuthService:
    def __init__(self):
        self.auth_dao = AthuDao(const.uri, const.username, const.password, const.db_name, const.athu_collection)

    def register(self, username: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        if not self.auth_dao.is_username_registered(username) :
            return self.auth_dao.create_account(username, hashed_password) 
        
        return False

    def authenticate(self, username: str, password: str):
        if self.auth_dao.is_username_registered(username):
            if bcrypt.checkpw(password.encode('utf-8'), self.auth_dao.get_hashed_password(username)):
                return True
            
        return False