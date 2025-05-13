import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from model.link import *
from model.member_dao import Member_dao
import bcrypt
from Utils.auth import User  # ✅ 引入 User 類別

member_bp = Blueprint('member', __name__)


@member_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # request body
        requestParams = request.get_json()

        account = requestParams['account']
        password = requestParams['password']
        dbParams = Member_dao.get_member(account)

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


@member_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # request body
        requestParams = request.get_json()

        if not requestParams:
            return jsonify({'status': 'error', 'message': 'Json格式錯誤'}), 400

        # 檢查Json的欄位有沒有空
        required_fields = ['name', 'account', 'password', 'identity']
        missing_fields = [
            field for field in required_fields if field not in requestParams]

        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        user_account = requestParams['account']
        exist_account = Member_dao.get_all_account()
        account_list = {i[0] for i in exist_account}

        # 檢查帳號是否已經存在
        if user_account in account_list:
            return jsonify({'status': 'error', 'message': '帳號已經存在'}), 200
        else:
            # 密碼加密
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(
                requestParams['password'].encode(), salt)

            # 用字典存輸入的參數
            input = {
                'name': requestParams['name'],
                'account': user_account,
                'password': hashed_password,
                'identity': requestParams['identity']
            }
            # call Member sql
            Member_dao.create_member(input)
            return jsonify({'status': 'success', 'message': '註冊成功 ! '}), 200


@member_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        username = current_user.name
    else:
        # 還沒登入用 Guest
        username = "Guest"

    logout_user()
    return jsonify({'status': 'success', 'message': f'{username} 登出，歡迎再次登入 ! '}), 200
