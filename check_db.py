import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        print("--- Tables ---")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])
            
        print("\n--- Migrations ---")
        try:
            cursor.execute("SELECT app, name FROM django_migrations;")
            migrations = cursor.fetchall()
            for m in migrations:
                print(f"{m[0]}: {m[1]}")
        except sqlite3.OperationalError:
            print("django_migrations table not found")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
