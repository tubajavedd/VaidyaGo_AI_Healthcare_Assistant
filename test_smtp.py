import smtplib
import os

try:
    server = smtplib.SMTP("smtp.sendgrid.net", 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("apikey", "06263ff2-27a8-4392-b9e5-4961e06e119e")
    print("Login successful")
    server.quit()
except Exception as e:
    print(f"Error: {e}")
