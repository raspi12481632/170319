import sqlite3
conn = sqlite3.connect('arduino_log.db')
c = conn.cursor()
c.execute('''CREATE TABLE humidity (date text, value real)''')
c.execute('''CREATE TABLE temperature (date text, value real)''')
c.execute('''CREATE TABLE light (date text, value real)''')
conn.commit()
conn.close()
