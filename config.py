import os
from urllib.parse import quote_plus

#  取得啟動文件資料夾路徑
basedir = os.path.abspath(os.path.dirname(__file__))

# TODO 修改資料庫串接內容，串接至MSSQL Server
# def create_sqlite_uri(db_name):
#     return "sqlite:///" + os.path.join(basedir, db_name)
# SQLALCHEMY_DATABASE_URI = create_sqlite_uri('EMI.db')

password = "1qaz@WSX"
encoded_password = quote_plus(password)

# def create_mssql_uri(username, password, server, database):
#     return f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# SQLALCHEMY_DATABASE_URI = create_mssql_uri('sa', encoded_password, '140.115.197.10:1433', 'EMI')

SECRET_KEY = os.urandom(32)

if os.name == 'nt':
    ENV = 'DEVELOPMENT'
    FORENTEND_URL = 'https://localhost:3000/EMI'
else:
    ENV = 'PRODUCTION'
    FORENTEND_URL = 'https://ncu.edu.tw/EMI'

SESSION_PROTECTION = 'strong'
UPLOADED_TXT_DEST = os.path.join(basedir, "static", "upload", "text")
UPLOADED_PHOTOS_DEST = os.path.join(basedir, "static", "upload")
UPLOADED_AUDIO_DEST = os.path.join(basedir, "static", "upload", "audio")
UPLOADED_TURTORIAL_DEST = os.path.join(basedir, "static", "upload", "turtorial")
CERT = os.path.join(basedir, 'cert.pem')
KEY = os.path.join(basedir, 'key.pem')
