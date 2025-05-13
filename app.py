import re, os, random, string
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint, url_for, redirect, flash, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
from sqlalchemy import null
from api import api_bp
# from api.crawler import *
# from api.member import *
from model.sql import *
from model.link import *
from werkzeug.utils import secure_filename
from Utils.auth import login_manager
## Flask-Login : 確保未登入者不能使用系統
# app = Flask(__name__)
# app.secret_key = 'Your Key' 

app = Flask(__name__, 
    template_folder='frontend/templates',
    static_folder='frontend/static')

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
app.config['PORT'] = int(os.getenv('PORT', 5000))
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

# 註冊API藍圖
app.register_blueprint(api_bp)

login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "Your Key"
    app.run()