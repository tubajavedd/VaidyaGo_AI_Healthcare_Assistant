import sqlite3
from datetime import datetime

def fix_migrations():
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Check if AdminLogin 0001_initial is already there
        cursor.execute("SELECT * FROM django_migrations WHERE app='AdminLogin' AND name='0001_initial';")
        if cursor.fetchone():
            print("AdminLogin 0001_initial already exists in django_migrations.")
        else:
            print("Inserting AdminLogin 0001_initial into django_migrations...")
            cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?);", 
                           ('AdminLogin', '0001_initial', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            print("Done.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_migrations()
