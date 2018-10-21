import sqlite3

con = sqlite3.connect('base.db')

cur = con.cursor()

sql = '''
   CREATE TABLE users(
       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       name VARCHAR(100),
       username VARCHAR(100),
       email VARCHAR(30),
       password VARCHAR(100),
       register_date Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
       ) 
'''

cur.execute(sql)
con.commit()

sql = '''
   CREATE TABLE editorials(
       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       title VARCHAR(255), 
       author VARCHAR(100),
       body TEXT,
       create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP); 
'''

cur.execute(sql)
con.commit()

con.close()