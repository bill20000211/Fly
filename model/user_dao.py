from typing import Optional
from sqlalchemy.orm import sessionmaker
from model.link import *
import logging
from model.sql import DB

# 設定 logging 設定
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', filename='app.log', filemode='w')

# 建立 Session 類別，並使用之前的 engine 來建立資料庫會話
Session = sessionmaker(bind=engine)


class User_dao():
    @staticmethod
    def get_member(account):
        sql = """
                SELECT ACCOUNT, PASSWORD, ID, user_identity, NAME
                  FROM MEMBER
                 WHERE ACCOUNT = :account
              """
        session = DB.get_session()
        result = DB.execute(session, sql, {'account': account})
        return DB.fetchall(result)

    @staticmethod
    def get_all_account():
        sql = """
                SELECT ACCOUNT 
                  FROM MEMBER
              """
        session = DB.get_session()
        result = DB.execute(session, sql)
        return DB.fetchall(result)

    @staticmethod
    def create_member(input):
        sql = """
                INSERT INTO [USER] ( UserId, RoleCode, Account, Password, UserName, Sex, Email, Phone, IsDelete ) 
                VALUES ( :UserId, :RoleCode, :Account, :Password, :UserName, :Sex, :Email, :Phone, :IsDelete )
              """
        session = DB.get_session()
        DB.execute(session, sql, input)
        DB.commit(session)

    @staticmethod
    def get_role(userid):
        sql = """
                SELECT user_identity, NAME 
                  FROM MEMBER 
                 WHERE ID = :id
              """
        session = DB.get_session()
        result = DB.execute(session, sql, {'id': userid})
        return DB.fetchone(result)
