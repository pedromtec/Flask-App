import sqlite3

class Db:
    def __init__(self, path):
        self.path = path
    
    def execute_query(self, sql):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def save(self, sql):
        self.execute_query(sql)
        
    def find_one(self, sql):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        con.commit()
        con.close()
        return data
    def find_all(self, sql):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        con.commit()
        con.close()
        return data
    def update(self, sql):
        self.execute_query(sql)

