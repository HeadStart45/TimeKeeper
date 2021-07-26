import sqlite3 as sql

conn = sql.connect("time.db")
c = conn.cursor()


conn.commit()
conn.close()

#c.execute('''
#    CREATE TABLE IF NOT EXISTS timeslots(
#        id INTEGER PRIMARY KEY,
#        task TEXT,
#        length TEXT 
#     )
#''')