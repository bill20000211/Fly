from flask_login import LoginManager, UserMixin
from model.user_dao import User_dao

# 建立 LoginManager 物件
login_manager = LoginManager()
login_manager.login_view = "api.member.login"
login_manager.login_message = "請先登入"

# 定義 User 類別


class User(UserMixin):
    def __init__(self, user_id=None, role=None, name=None):
        self.id = user_id
        self.role = role
        self.name = name

# 設定用戶加載函數


@login_manager.user_loader
def user_loader(userid):
    data = User_dao.get_role(userid)
    if not data:
        return None  # 如果查無此用戶，回傳 None

    return User(user_id=userid, role=data[0], name=data[1])
