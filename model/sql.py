from typing import Optional
from sqlalchemy.orm import sessionmaker
from model.link import *
import logging

# 設定 logging 設定
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', filename='app.log', filemode='w')

# 建立 Session 類別，並使用之前的 engine 來建立資料庫會話
Session = sessionmaker(bind=engine)


class DB():
    @staticmethod
    def get_session():
        # 返回一個資料庫 Session
        return Session()

    @staticmethod
    def execute(session, sql, params=None):
        # 使用 SQLAlchemy 的 Session 來執行 SQL 查詢
        result = session.execute(sql, params)
        return result

    @staticmethod
    def commit(session):
        # 提交變更
        session.commit()

    @staticmethod
    def fetchall(result):
        # 返回所有結果
        return result.fetchall()

    @staticmethod
    def fetchone(result):
        # 返回一個結果
        return result.fetchone()
