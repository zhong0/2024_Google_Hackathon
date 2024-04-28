from ..dao.AuthDao import AuthDao
from ..utils import Const as const
import bcrypt
import re

class AuthService:
    def __init__(self):
        self.auth_dao = AuthDao(const.uri, const.username, const.password, const.db_name, const.auth_collection)

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
    
    # 用戶名長度至少5個字符
    def is_validate_username(self, username: str) -> bool:
        
        return len(username) >= 2

    # 密碼至少8個字符且包含至少一個數字和一個字母
    def is_validate_password(self, password: str) -> bool:
        # if len(password) < 8:
        #     return False
        # if not re.search("[a-zA-Z]", password):
        #     return False
        # if not re.search("[0-9]", password):
        #     return False
        
        return True
