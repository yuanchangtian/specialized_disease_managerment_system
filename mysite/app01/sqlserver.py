#-*- coding:utf-8 -*-
"""
Author: yuanchangtian
Data: 2024-07-04
Owner: Shanghai Dermatology Hospital
"""

import pyodbc  
import configparser
  
class SQLServerDB:  
    def __init__(self, server, port, database, username, password):  
        """  
        初始化SQL Server数据库连接。  
  
        参数:  
        server (str): 数据库服务器的地址或名称。  
        database (str): 要连接的数据库名。  
        username (str): 用户名。  
        password (str): 密码。  
        """  
        self.server = server  
        self.database = database  
        self.port = port
        self.username = username  
        self.password = password  
        self.connection = None  
        self.cursor = None  
        #查看driver
  
    def connect(self):  
        """  
        建立到SQL Server的连接。  
        """  
 
        info_str = (f'DRIVER={{SQL Server}};'
                    f'SERVER={self.server};'
                    f'PORT={self.port};'
                    f'DATABASE={self.database};'
                    f'UID={self.username};'
                    f'PWD={self.password};')
        self.connection = pyodbc.connect(info_str)
        self.cursor = self.connection.cursor()  

    def execute_query(self, query):  
        """  
        执行SQL查询。  
  
        参数:  
        query (str): 要执行的SQL查询语句。  
  
        返回:  
        list of tuples: 查询结果（如果有的话）。  
        """  
        try:  
            self.cursor.execute(query)  
            if self.cursor.description:  
                columns = [column[0] for column in self.cursor.description]  
                return [dict(zip(columns, row)) for row in self.cursor.fetchall()]  
            else:  
                self.connection.commit()  
                return None  
        except Exception as e:  
            print(f"查询执行失败: {e}")  
            return None  
    def send_message(self, message, phone_number):
        try:
            self.connection.autocommit = True
            #self.cursor.execute("{CALL sp_sy_send_sms(?,?,?,?)}", 'DXPT', '短信测试！', '18616020920', 0)
            self.cursor.execute("EXEC sp_sy_send_sms ?,?,?,?", 'DXPT', message, phone_number, 0)
            self.connection.autocommit = False
            return None
        except Exception as e:
            print (e)
            return None
 
    def first_visit(self, start, end):
        try:
            self.connection.autocommit = True
            self.cursor.execute("EXEC SP_DP_OP_FirstVisit ?,?", start, end)
            self.connection.autocommit = False
            result = []
            if self.cursor.description: 
                #包含schema
                columns = [column[0] for column in self.cursor.description]  
                result.append('\t'.join(columns))
                for row in self.cursor.fetchall():
                    result.append('\t'.join(map(str, row)))
                return '\n'.join(result)
            for data in self.cursor.fetchall():
                print (data)
            return  None
        except Exception as e:
            print (e)
            return None
    def close_connection(self):  
        """  
        关闭数据库连接。  
        """  
        if self.cursor:  
            self.cursor.close()  
        if self.connection:  
            self.connection.close()  
        print("数据库连接已关闭")  

if __name__ == "__main__":  
    config = configparser.ConfigParser()
    config.read('./conf/config.ini', encoding='utf-8')
    server = config.get('Database', 'server')
    port = config.get('Database', 'port')
    database = config.get('Database', 'database')
    username = config.get('Database', 'username')
    password = config.get('Database', 'password')
  
    db = SQLServerDB(server, port, database, username, password)  
    db_connect = db.connect()  
    #result = db.execute_query("SELECT * FROM aa WHERE id > 1") 
    result = db.first_visit('20240801', '20240801')
    #print(result)  
    db.close_connection()
