import sqlite3

def fix_admin_log():
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        print("Dropping django_admin_log table...")
        cursor.execute("DROP TABLE IF EXISTS django_admin_log;")
        
        print("Deleting admin migration records...")
        cursor.execute("DELETE FROM django_migrations WHERE app='admin';")
        
        conn.commit()
        print("Cleanup successful. Now run 'python manage.py migrate admin'")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_admin_log()
