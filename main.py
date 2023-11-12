from flask import Flask, render_template, request,Response,send_file
import time
from datetime import datetime,date
from module import generate_frames,classify_frame,save_Pic
import mysql.connector


app = Flask(__name__)

# *********************************************************************************************************
# database collecting

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
# ***************************************************************************************************

@app.route('/')
def home():

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('home.html', live_time=current_time)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame', content_type='multipart/x-mixed-replace; boundary=frame')



@app.route('/camera')
def camera():
   
    class_name=classify_frame()
    

    # attendence marking
    date_=datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')

    query="select student_id from students where name = %s"
    cursor.execute(query,(class_name,))
    id=cursor.fetchone()


# detecting student morethan once it gives repetation error
    try:
        query1="insert into attendance (student_id,attendance_date,is_present) values (%s,%s,%s)"
        value=(id[0],date_,time)
        cursor.execute(query1,value)
        connection.commit()
    except Exception as e:
        pass
    finally:
        # show department
        query='select department from students where name = %s'
        cursor.execute(query,(class_name,))
        dep=cursor.fetchone()

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('camera.html', live_time=current_time,name=class_name,reg_no=id[0],dep=dep[0])





@app.route('/admin_page')
def admin_page():

    return render_template('admin.html')

# saving attendence sheet
@app.route('/print_attendance', methods=['GET', 'POST'])
def print_attendance():
    if request.method == 'POST':
    
        start_date = request.form['strt_date']
        end_date = request.form['end_date']
        
        # Fetch data from the database based on the date range
        query = "SELECT students.name,students.student_id,attendance.attendance_date,attendance.is_present FROM students join attendance ON students.student_id = attendance.student_id \
        where attendance.attendance_date BETWEEN %s and %s order by attendance.attendance_date;"              
        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()

        # Process the retrieved data 
        # we'll save it to a CSV file
        with open('data1.csv', 'w') as f:
            for row in data:
                formatted_data = [str(val) if not isinstance(val,date) else val.strftime('%Y-%m-%d') for val in row]
                f.write(','.join(formatted_data) + '\n')
        f.close()
        
     # Return the file to the user for download
    return send_file('data1.csv', as_attachment=True)


# Handle the submission of the "Add Member" form here
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        dep = request.form['dep']

        query = "insert into students ( name, age, email, department) VALUES (%s,%s,%s,%s)"
        values = ( name, age, email, dep)
        cursor.execute(query,values)
        connection.commit()
                    
    return render_template('admin.html')


@app.route('/add_cam')
def add_cam():
    return render_template('add_cam.html')

@app.route('/video_feed1')
def video_feed1():
    query="select name from students order by student_id desc limit 1"
    cursor.execute(query)
    name=cursor.fetchone()
    return Response(save_Pic(name[0]), mimetype='multipart/x-mixed-replace; boundary=frame', content_type='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)


    