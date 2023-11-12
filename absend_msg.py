# programme for sending automated absent message to the mailid given

import yagmail
import schedule
import time
from datetime import datetime
import mysql.connector

def send_emails():
    host = "localhost"
    user = "root"
    password = "Password@123"
    database = "dl_project"

   
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    date_=datetime.now().strftime('%Y-%m-%d')
    query = "SELECT s.name,s.email FROM students s LEFT JOIN attendance a ON s.student_id = a.student_id AND a.attendance_date = %s  \
            WHERE a.student_id IS NULL"
    cursor.execute(query, (date_,))
    name = cursor.fetchall()


    for i in name:
        print(i[0])

        # Email configuration
        sender_email = 'divasdivu98@gmail.com'
        app_password = 'qsgd bvfp zbap spse'  # If you generated an App Password
        recipient_email = i[1]
        

        subject = 'Attendance of student'
        message = f'{i[0]} is absent today'
        

        # # Initialize the yagmail SMTP client
        yag = yagmail.SMTP(sender_email, app_password)

        # # Send the email
        yag.send(
            to=recipient_email,
            subject=subject,
            contents=message
        )
        print('sentt')
        
        yag.close()

schedule.every().day.at("09:17").do(send_emails) 

while True:
    schedule.run_pending()
    time.sleep(5)
    
    

    