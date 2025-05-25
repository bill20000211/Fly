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


class RawData_dao():
    @staticmethod
    def create_rawdata(input):
        all_columns = [
            'supplier', 'prod_oid', 'pkg_oid', 'prod_name', 'description',
            'departure_date', 'return_date', 'seats_total', 'seats_quota', 'seats_spare',
            'seats_actual', 'seats_wait', 'seats_kk', 'seats_keep', 'seats_ob',
            'prod_type', 'straight_lowest_price', 'industry_lowest_price', 'price', 'pax_type',
            'src', 'last_updated', 'status'
        ]

        input['status'] = 'import'
        provided_columns = [col for col in all_columns if col in input]

        sql = f"""
                INSERT INTO fly_product_raw ({', '.join(provided_columns)})
                VALUES ({', '.join([f':{col}' for col in provided_columns])})
              """

        session = DB.get_session()
        DB.execute(session, sql, input)
        DB.commit(session)

    @staticmethod
    def create_rawdata_kkday(input):
        sql = """
                INSERT INTO fly_product_raw(
                    supplier,       prod_oid,  pkg_oid, pkg_name, description, 
                    departure_date, prod_type, price,   pax_type, src, 
                    last_updated,   status
                )
                VALUES (
                    :supplier,       :prod_oid,  :pkg_oid, :pkg_name, :description, 
                    :departure_date, :prod_type, :price,   :pax_type, :src, 
                    :last_updated,   'import'
                )
              """
        session = DB.get_session()
        DB.execute(session, sql, input)
        DB.commit(session)

    @staticmethod
    def create_rawdata_lion(input):
        sql = """
                INSERT INTO fly_product_raw (
                    supplier,     prod_oid,       pkg_oid,        prod_name,      pkg_name, 
                    description,  departure_date, return_date,    seats_total,    seats_quota, 
                    seats_spare,  seats_actual,   seats_wait,     seats_kk,       seats_keep, 
                    seats_ob,     straight_lowest_price,  industry_lowest_price,  price,       
                    src,          last_updated,   status
                )
                VALUES (
                    :supplier,     :prod_oid,              :pkg_oid,               :prod_name,   :pkg_name, 
                    :description,  :departure_date,        :return_date,           :seats_total, :seats_quota, 
                    :seats_spare,  :seats_actual,          :seats_wait,            :seats_kk,    :seats_keep, 
                    :seats_ob,     :straight_lowest_price, :industry_lowest_price, :price,       :src, 
                    :last_updated, 'import'
                )
              """
        session = DB.get_session()
        DB.execute(session, sql, input)
        DB.commit(session)

    @staticmethod
    def check_data_exsit(input):
        conditions = []
        params = {}
        columns = [
            'supplier', 'prod_oid', 'pkg_oid', 'prod_name', 'description',
            'departure_date', 'return_date', 'seats_total', 'seats_quota', 'seats_spare',
            'seats_actual', 'seats_wait', 'seats_kk', 'seats_keep', 'seats_ob',
            'prod_type', 'straight_lowest_price', 'industry_lowest_price', 'price',
            'pax_type', 'src', 'pkg_name'
        ]

        for column in columns:
            if column in input:
                conditions.append(f"{column} = :{column}")
                params[column] = input[column]
            else:
                conditions.append(f"{column} IS NULL")

        sql = f"""
                SELECT COUNT(*)
                  FROM fly_product_raw
                 WHERE {' AND '.join(conditions)}
              """
        session = DB.get_session()
        result = DB.execute(session, sql, params)
        return DB.fetchone(result)

    @staticmethod
    def check_key_data_exsit(input):
        sql = """
                SELECT COUNT(*)
                  FROM fly_product_raw
                 WHERE prod_oid = :prod_oid
                   AND pkg_oid  = :pkg_oid
              """
        session = DB.get_session()
        result = DB.execute(session, sql, input)
        return DB.fetchone(result)

    @staticmethod
    def refresh_data_by_key(input):
        RawData_dao.delete_data_by_key(input)
        RawData_dao.create_rawdata(input)

    @staticmethod
    def raw_import_to_ready(input):
        sql = """
                UPDATE fly_product_raw
                   SET status   = 'ready'
                 WHERE status   = 'import'
                   AND supplier = :supplier
              """
        session = DB.get_session()
        DB.execute(session, sql, input)
        DB.commit(session)

    @staticmethod
    def delete_data_by_key(input):
        sql = """
                DELETE FROM fly_product_raw
                 WHERE prod_oid = :prod_oid
                   AND pkg_oid  = :pkg_oid  
                   AND status   = 'ready'   
              """
        session = DB.get_session()
        DB.execute(session, sql, input)
        DB.commit(session)
