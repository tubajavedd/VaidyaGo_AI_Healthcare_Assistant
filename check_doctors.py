import sqlite3

def check_doctors():
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        print("--- Dr_personalInfo Tables ---")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Dr_personalInfo%';")
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])
            cursor.execute(f"SELECT count(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"  Count: {count}")
            
        print("\n--- DoctorPersonalInfo Content ---")
        try:
            cursor.execute("SELECT id, first_name, last_name FROM Dr_personalInfo_doctorpersonalinfo LIMIT 5;")
            doctors = cursor.fetchall()
            for d in doctors:
                print(d)
        except Exception as e:
            print(f"Error reading doctors: {e}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_doctors()
