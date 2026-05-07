import sqlite3
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("DELETE FROM django_migrations WHERE app='admin';")
conn.commit()
conn.close()
print("Success")
