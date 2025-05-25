import imp, uuid
from flask import render_template, Blueprint, redirect, request, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from model.link import *
from model.user_dao import User_dao
import bcrypt
from Utils.auth import User  # ✅ 引入 User 類別

user_bp = Blueprint('user', __name__)

@user_bp.route('/test', methods=['GET'])
def test_member():
    """
    測試用的會員 API
    ---
    tags:
      - Users
    responses:
      200:
        description: 成功返回測試訊息
        examples:
          application/json: { "message": "Hello from member" }
    """
    return jsonify(message="Hello from member")


@user_bp.route('/login', methods=['POST'])
def login():
    """
    會員登入
    ---
    tags:
      - Users
    parameters:
      - name: account
        in: formData
        required: true
        type: string
        description: 帳號
      - name: password
        in: formData
        required: true
        type: string
        description: 密碼
    responses:
      200:
        description: 登入成功
        examples:
          application/json: { "status": "success", "message": "登入成功" }
      400:
        description: 登入失敗
        examples:
          application/json: { "status": "error", "message": "登入失敗" }
    """
    if request.method == 'POST':
        # request body
        requestParams = request.get_json()

        account = requestParams['account']
        password = requestParams['password']
        dbParams = User_dao.get_member(account)

        if not dbParams:
            return jsonify({'status': 'error', 'message': f'找不到帳號: {account} !'}), 400

        try:
            DB_password = dbParams[0][1]
            user_id = dbParams[0][2]
            identity = dbParams[0][3]
            name = dbParams[0][4]

        except:
            return jsonify({'status': 'error', 'message': f'找不到帳號: {account} !'}), 400

         # 輸入的密碼轉bytes
        input_password = password.encode()

        # DB抓出來的密碼轉bytes
        if isinstance(DB_password, str):
            DB_password = DB_password.encode()
        if not DB_password:
            return jsonify({'status': 'error', 'message': '密碼錯誤或帳號不存在 !'}), 400
        # 驗證密碼
        is_correct = bcrypt.checkpw(input_password, DB_password)

        if (is_correct):
            user = User()
            user.id = user_id
            login_user(user)

            if (identity == 'user'):
                return jsonify({'status': 'success', 'message': f'{name} ，歡迎 ! '}), 200
            else:  # manager
                return jsonify({'status': 'success', 'message': f'{name} ，管理員登入 ! '}), 200
        else:
            return jsonify({'status': 'error', 'message': f'密碼錯誤 ! '}), 400


@user_bp.route('/register', methods=['POST'])
def register():
    """
    會員註冊
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            account:
              type: string
              description: 帳號
              maxLength: 20
              minLength: 3
              example: yenyu
            password:
              type: string
              description: 密碼
              minLength: 6
              maxLength: 32
              example: myPassword123
            user_name:
              type: string
              description: 名稱
              maxLength: 50
              example: 嚴育程
            sex:
              type: string
              description: 性別
              enum: [male, female, other]
              example: male
            email:
              type: string
              description: 電子信箱
              format: email
              example: c6121041210@gmail.com
            phone:
              type: string
              description: 手機
              pattern: '^[0-9]{10}$'
              example: "0912345678"
          required:
            - account
            - password
            - user_name
    responses:
      200:
        description: 註冊成功
        examples:
          application/json: { "status": "success", "message": "註冊成功" }
      400:
        description: 註冊失敗
        examples:
          application/json: { "status": "error", "message": "註冊失敗" }
    """
    if request.method == 'POST':
        requestParams = request.get_json()

        if not requestParams:
            return jsonify({'status': 'error', 'message': 'Json格式錯誤'}), 400

        required_fields = ['account', 'password', 'user_name']
        missing_fields = [field for field in required_fields if field not in requestParams]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        user_account = requestParams['account']
        exist_account = User_dao.get_all_account()
        account_list = {i[0] for i in exist_account}
        if user_account in account_list:
            return jsonify({'status': 'error', 'message': '帳號已經存在'}), 200

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(requestParams['password'].encode(), salt)

        sex = requestParams.get('sex')
        email = requestParams.get('email')
        phone = requestParams.get('phone')
        is_delete = 0
        user_id = str(uuid.uuid4())

        # 這裡指定預設role_code
        default_role_code = 'user'

        user_data = {
            'UserId': user_id,
            'RoleCode': default_role_code,
            'Account': user_account,
            'Password': hashed_password.decode(),
            'UserName': requestParams['user_name'],
            'Sex': sex,
            'Email': email,
            'Phone': phone,
            'IsDelete': is_delete
        }

        User_dao.create_member(user_data)
        return jsonify({'status': 'success', 'message': '註冊成功 ! '}), 200


@user_bp.route('/logout')
def logout():
    """
    會員登出
    ---
    tags:
      - Users
    responses:
      200:
        description: 登出成功
        examples:
        application/json: { "status": "success", "message": "登出成功" }
    """
    if current_user.is_authenticated:
        username = current_user.name
    else:
        # 還沒登入用 Guest
        username = "Guest"

    logout_user()
    return jsonify({'status': 'success', 'message': f'{username} 登出，歡迎再次登入 ! '}), 200
