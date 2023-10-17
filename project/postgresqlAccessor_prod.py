#!/usr/local/bin/python3.4
# coding: utf-8
import psycopg2 
import psycopg2.extras
import sys

#
# 【本番環境】Postgresqlアクセス管理クラス
#
class postgresqlAccessor_prod:
         

    # -----------------------------------
    # コンストラクタ
    #
    # コネクションを取得し、クラス変数にカーソルを保持する。
    # -----------------------------------
    def __init__(self):
        print("start:__init__")

        host      = 'magcraft-prod-db-instance-1.cz2pm4xengae.ap-northeast-1.rds.amazonaws.com'
        users     = 'mits_migration'
        dbnames   = 'mitsdb'
        passwords = 'm1t5_m1gr@t10n'
        
        conn_string =" host=" + host +" user=" + users +" dbname=" + dbnames +" password=" + passwords
        
        try:
            self.connection = psycopg2.connect(conn_string)
            #クライアントプログラムのエンコードを設定（DBの文字コードから自動変換してくれる）
            self.connection.set_client_encoding('utf-8') 
            #select結果を辞書形式で取得するように設定 
            self.connection.cursor_factory=psycopg2.extras.DictCursor

        except psycopg2.OperationalError as e:
            print('Unable to connect!\n{0}').format(e)
            sys.exit(1)

        else:
            print ('Connected!')
            self.cur = self.connection.cursor()
           
        print("end:__init__")

    # -----------------------------------
    # クエリの実行
    #
    # クエリを実行し、取得結果を呼び出し元に通知する。
    # -----------------------------------
    def excecuteQuery(self, sql):
        print("start:excecuteQuery")

        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            return rows
        except psycopg2.OperationalError as e:
            print(e)

        print("end:excecuteQuery")

    # -----------------------------------
    # インサートの実行
    #
    # インサートを実行する。
    # -----------------------------------
    def excecuteInsert(self, sql):
        print("start:excecuteInsert")

        try:
            self.cur.execute(sql)
            self.connection.commit()
            return self.cur.rowcount
        except psycopg2.OperationalError as e:
            self.connection.rollback()
            print(e)

        print("end:excecuteInsert")

    # -----------------------------------
    # アップデートの実行
    #
    # アップデートを実行する。
    # -----------------------------------
    def excecuteUpdate(self, sql):
        print("start:excecuteUpdate")

        try:
            self.cur.execute(sql)
            self.connection.commit()
            return self.cur.rowcount
        except psycopg2.OperationalError as e:
            self.connection.rollback()
            print(e)

        print("end:excecuteUpdate")

    # -----------------------------------
    # デリートの実行
    #
    # デリートを実行する。
    # -----------------------------------
    def excecuteDelete(self, sql):
        print("start:excecuteDelete")

        try:
            self.cur.execute(sql)
            self.connection.commit()
            return self.cur.rowcount
        except psycopg2.OperationalError as e:
            self.connection.rollback()
            print(e)

        print("end:excecuteDelete")

    # -----------------------------------
    # デストラクタ
    #
    # コネクションを解放する。
    # -----------------------------------
    def __del__(self):
        print("start:__del__")
        try:
            self.connection.close()
        except psycopg2.OperationalError as e:
            print(e)
        print("end:__del__")