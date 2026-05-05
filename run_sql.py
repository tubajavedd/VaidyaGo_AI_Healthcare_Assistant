import sqlite3

def run_sql():
    sql = """
BEGIN;
--
-- Create model Doctor
--
CREATE TABLE "AdminLogin_doctor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "phone" varchar(15) NOT NULL UNIQUE, "specialty" varchar(100) NOT NULL, "experience" integer unsigned NOT NULL CHECK ("experience" >= 0), "is_active" bool NOT NULL);
--
-- Create model OTP
--
CREATE TABLE "AdminLogin_otp" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(254) NULL, "otp" varchar(6) NOT NULL, "is_verified" bool NOT NULL, "created_at" datetime NOT NULL);
--
-- Create model User
--
CREATE TABLE "AdminLogin_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "role" varchar(20) NOT NULL, "phone" varchar(15) NULL UNIQUE, "email" varchar(254) NULL UNIQUE);
CREATE TABLE "AdminLogin_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "AdminLogin_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "AdminLogin_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "AdminLogin_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model UserProfile
--
CREATE TABLE "AdminLogin_userprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address" varchar(255) NULL, "age" integer NULL, "user_id" bigint NOT NULL REFERENCES "AdminLogin_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Profile
--
CREATE TABLE "AdminLogin_profile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "phone_number" varchar(15) NOT NULL, "post" varchar(10) NOT NULL, "language" varchar(50) NOT NULL, "google_connected" bool NOT NULL, "google_email" varchar(254) NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "AdminLogin_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Address
--
CREATE TABLE "AdminLogin_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "country" varchar(100) NOT NULL, "city" varchar(100) NOT NULL, "pincode" varchar(10) NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "AdminLogin_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "AdminLogin_user_groups_user_id_group_id_e4db51fb_uniq" ON "AdminLogin_user_groups" ("user_id", "group_id");
CREATE INDEX "AdminLogin_user_groups_user_id_91fa648d" ON "AdminLogin_user_groups" ("user_id");
CREATE INDEX "AdminLogin_user_groups_group_id_bb332573" ON "AdminLogin_user_groups" ("group_id");
CREATE UNIQUE INDEX "AdminLogin_user_user_permissions_user_id_permission_id_f07ecdf1_uniq" ON "AdminLogin_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "AdminLogin_user_user_permissions_user_id_dee47d3f" ON "AdminLogin_user_user_permissions" ("user_id");
CREATE INDEX "AdminLogin_user_user_permissions_permission_id_0d646a98" ON "AdminLogin_user_user_permissions" ("permission_id");
CREATE INDEX "AdminLogin_userprofile_user_id_f7e9ac7f" ON "AdminLogin_userprofile" ("user_id");
COMMIT;
    """
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.executescript(sql)
        conn.commit()
        print("SQL executed successfully.")
        conn.close()
    except Exception as e:
        print(f"Error executing SQL: {e}")

if __name__ == "__main__":
    run_sql()
