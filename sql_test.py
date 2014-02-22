import sqlite3

db = sqlite3.connect(':memory:')

test_date = '2014 Jun 22 23:43:27'
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE users(id INTEGER PRIMARY KEY, user TEXT,
                       module TEXT, version TEXT, date TEXT, time TIME)
''')
db.commit()

db.close()
