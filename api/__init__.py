"""API模組，提供HTTP接口。"""

from flask import Blueprint
from .user import user_bp
from .crawler import crawler_bp


# 創建API藍圖
api_bp = Blueprint('api', __name__, url_prefix='/')

# 註冊子藍圖
api_bp.register_blueprint(user_bp, url_prefix='/user')
api_bp.register_blueprint(crawler_bp, url_prefix='/crawlers')


# 導出藍圖
__all__ = ['api_bp']