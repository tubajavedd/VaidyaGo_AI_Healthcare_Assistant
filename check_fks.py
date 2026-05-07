import sqlite3

def check_fks():
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        print("--- Foreign Key Check ---")
        cursor.execute("PRAGMA foreign_key_check;")
        violations = cursor.fetchall()
        if not violations:
            print("No FK violations found.")
        else:
            for v in violations:
                print(f"Table: {v[0]}, Rowid: {v[1]}, Referenced Table: {v[2]}, FK Index: {v[3]}")
                
        print("\n--- django_admin_log FKs ---")
        cursor.execute("PRAGMA foreign_key_list('django_admin_log');")
        fks = cursor.fetchall()
        for fk in fks:
            print(fk)
            
        print("\n--- AdminLogin_user Schema ---")
        cursor.execute("SELECT sql FROM sqlite_master WHERE name='AdminLogin_user';")
        print(cursor.fetchone()[0])
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_fks()
