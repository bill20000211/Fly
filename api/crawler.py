import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from model.link import *
from model.sql import *
from Utils.RawToJson import CrawlertoRawData_kkday, CrawlertoRawData_lion
from Utils.auth import User  # ✅ 引入 User 類別

from service.crawler_service import crawler_service

crawler_bp = Blueprint('crawler', __name__)


@crawler_bp.route('/rawtojson', methods=['POST'])
def rawtojson():
    #hardcode 寫死的路徑
    v_kkday_from = './storage/kkday_crawler_output/'
    v_lion_from = './storage/lion_crawler_output/'
    v_kkday_to = './storage/kkday_rawdata'
    v_lion_to = './storage/lion_rawdata'

    try:
        requestParams = request.get_json()
        v_module = requestParams.get('module')

        if not requestParams or not isinstance(requestParams, dict):
            return jsonify({'status': 'error', 'message': '請提供有效的 JSON request'}), 400

        if requestParams.get('action') == 'by_manager':
            if not current_user.is_authenticated:
                return jsonify({'status': 'error', 'message': '尚未登入管理員帳號 !'}), 403
            
            if current_user.role != 'manager':
                return jsonify({'status': 'error', 'message': '權限不足 !'}), 403
        
        if requestParams.get('type') == 'kkday' or requestParams.get('type') == 'all':
            kkday_datas = crawler_service.process_data(v_kkday_from, v_kkday_to, 'kkday', v_module)
        if requestParams.get('type')== 'lion' or requestParams.get('type') == 'all':
            kkday_datas = crawler_service.process_data(v_lion_from, v_lion_to, 'lion', v_module)     

        return jsonify({'status': 'success', 'message': '資料已處理完畢 !'}), 200

    except Exception as e:
        print(f"發生錯誤: {str(e)}")  # 伺服器端 log
        return jsonify({'status': 'error', 'message': f'發生錯誤: {str(e)}'}), 500

