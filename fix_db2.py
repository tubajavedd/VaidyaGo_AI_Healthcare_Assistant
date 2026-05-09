import sqlite3
import datetime

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('admin', '0001_initial', ?)", (datetime.datetime.now(),))
cur.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('AdminLogin', '0001_initial', ?)", (datetime.datetime.now(),))
conn.commit()
conn.close()
print("Success")
