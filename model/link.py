from urllib.parse import quote_plus
from sqlalchemy import create_engine

# 設定資料庫連線參數
server_b = 'fly-dev.database.windows.net'
database_b = 'Fly_dev'
username_b = 'flyadmin'
password_b = quote_plus('1qaz@WSX')

# ====== 建立 SQLAlchemy 連線 ======
connection_string_b = (
    f"mssql+pyodbc://{username_b}:{password_b}@{server_b}:1433/{database_b}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=no"
    "&Encrypt=yes"
    "&ConnectionTimeout=10"
    "&authentication=SqlPassword"
)

# 使用 SQLAlchemy 來建立與資料庫的連線，並設定連線池參數
engine = create_engine(
    connection_string_b,
    pool_size=10,          # 連線池大小（預設為 5）
    max_overflow=20,       # 允許的額外連線數（預設為 10）
    pool_timeout=30,       # 等待連線的超時時間（秒）
    pool_recycle=1800      # 連線回收時間（秒，避免長時間閒置導致連線被關閉）
)

# 建立連線並確認連線是否成功
try:
    with engine.connect() as connection:
        print("Successfully connected to SQL Server")
        # 你可以在此進行資料庫操作，例：執行 SQL 查詢等
except Exception as e:
    print(f"Connection failed: {e}")
