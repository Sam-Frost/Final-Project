from flask import Flask, jsonify, redirect, render_template, request, url_for
from web_scraper.academics import get_attendance, get_timetable, store_profile_pic
from firebase import check_profile_picture_exists, create_document, docuemnt_count, get_file_url, read_documents, upload_to_firebase_storage

from models import student_model, notice_model, faculty_model, peer_tutoring_model, pyq_model, opportunity_model, rules_and_procedures_model

from api import api

import storage

# Create the Flask application
app = Flask(__name__)

# TODO : Add checks whenever adding data, if the data already exists!

# API endpoints router
app.register_blueprint(api,url_prefix='/api/v1')

# Define a route for the root URL "/"
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('homepage.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        print(password)
        return redirect(url_for('admin_dashboard'))


# Route for Admin Dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'GET':
        stats = {
            "student_count" : docuemnt_count(student_model.table), 
            "faculty_count" : docuemnt_count(faculty_model.table),
            "peer_session_count" : docuemnt_count(peer_tutoring_model.table),
            "notice_counts" : docuemnt_count(notice_model.table),
            "rules_and_procedures" : docuemnt_count(rules_and_procedures_model.table),
            "opportunity_count" : docuemnt_count(opportunity_model.table),
            "pyq_count" : docuemnt_count(pyq_model.table)
        }
        student_data = read_documents(student_model.table)
        return render_template('admin_dashboard.html', stats=stats, student_data=student_data)

    


# --------------------------------------------------------------------------------------------
# Route for viewing students
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        # Reading all studetns from the database and printing on webpage
    
        stats = {
            "student_count" : docuemnt_count(student_model.table), 
            "peer_session_count" : docuemnt_count(peer_tutoring_model.table)
        }
        student_data = read_documents(student_model.table)
        return render_template('students/students.html', stats=stats, student_data=student_data)
    
    elif request.method == 'POST':
        print("POST request received")
        # Retrieve student data from the database based on the roll number and display it on the webpage
        student_roll = request.form.get(student_model.student_roll)
        print("DATA recived: ", student_roll)
        
        params = {
            student_model.student_roll: student_roll
        }

        student_data = read_documents(student_model.table, params)

        if student_data:
            # return student_data
            return render_template('students/view_student.html', student_data=student_data[0])
        else :
            return jsonify({"message": "An error occurred while reading the student."}), 500
        
# Route for adding students
@app.route('/add_students', methods=['GET', 'POST'])
def add_students():
    if request.method == 'GET':
        return render_template('students/add_student.html', student_fields=student_model.fields)
    
    elif request.method == 'POST':
        student_data = {}
        for field in student_model.fields:
            
            # CODE TO ADD PROFILE PICTURE
            # ----------------------------------------
            if field == student_model.profile_picture:
                file = request.files['profile_picture']
                if file:
                    if file.filename.endswith('.jpg') or file.filename.endswith('.jpeg') or file.filename.endswith('.png'):
                        if upload_to_firebase_storage(file, request.form.get(student_model.student_roll), storage.profile_pictures):
                            student_data[student_model.profile_picture] = get_file_url(request.form.get(student_model.student_roll), storage.profile_pictures)
                continue
            # ----------------------------------------

            student_data[field] = request.form.get(field)

        if create_document(student_model.table, student_data):
            return jsonify({"message": "Student record created!."}), 201
        else :
            return jsonify({"message": "An error occurred while creating the student."}), 500
# --------------------------------------------------------------------------------------------
        

# --------------------------------------------------------------------------------------------
# Route for viewing faculty
@app.route('/faculty', methods=['GET', 'POST'])
def faculty():
    if request.method == 'GET':
        # Reading all studetns from the database and printing on webpage
        faculty_data = read_documents(faculty_model.table)
        stats = {
            "faculty_count" : docuemnt_count(faculty_model.table)
        }
        return render_template('faculty/faculty.html', faculty_data=faculty_data, stats=stats)
    
    elif request.method == 'POST':
        # Retrieve student data from the database based on the roll number and display it on the webpage
        faculty_roll = request.form.get(faculty_model.faculty_roll)
        print("DATA recived: ", faculty_roll)
        params = {
            faculty_model.faculty_roll: faculty_roll
        }

        faculty_data = read_documents(faculty_model.table, params)

        if faculty_data:
            # return faculty_data[0]
            return render_template('faculty/view_faculty.html', faculty_data=faculty_data[0])
        else :
            return jsonify({"message": "An error occurred while reading the faculty."}), 500
        
# Route for adding students
@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'GET':
        return render_template('faculty/add_faculty.html')
    
    elif request.method == 'POST':
        faculty_data = {}
        for field in faculty_model.fields:

            
            # CODE TO ADD PROFILE PICTURE
            # ----------------------------------------
            if field == faculty_model.profile_picture:
                file = request.files['profile_picture']
                if file:
                    if file.filename.endswith('.jpg') or file.filename.endswith('.jpeg') or file.filename.endswith('.png'):
                        if upload_to_firebase_storage(file, request.form.get(faculty_model.faculty_roll), storage.profile_pictures):
                            faculty_data[faculty_model.profile_picture] = get_file_url(request.form.get(faculty_model.faculty_roll), storage.profile_pictures)
                continue
            # ----------------------------------------



            faculty_data[field] = request.form.get(field)

        if create_document(faculty_model.table, faculty_data):
            return redirect(url_for('faculty')) 
            # return jsonify({"message": "Faculty record created!."}), 201
        else :
            return jsonify({"message": "An error occurred while creating the Faculty."}), 500
# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------

# Route for notices
@app.route('/notices', methods=['GET', 'POST'])
def notices():
    if request.method == 'GET':
        # Reading all notices from the database and printing on webpage
        notice_data = read_documents(notice_model.table)
        stats = {
            "notice_counts" : docuemnt_count(notice_model.table),
        }
        return render_template('notice/notices.html', stats=stats, notice_data=notice_data)
    
    elif request.method == 'POST':
        # Retrieve notice data from the database based on the notice_id and display it on the webpage
        notice_number = request.form.get(notice_model.notice_number)
        
        params = {
            notice_model.notice_number: notice_number
        }

        notice_data = read_documents(notice_model.table, params)

        if notice_data:
            return notice_data[0]
            # return render_template('notice/view_notice.html', notice_data=notice_data[0])
        else :
            return jsonify({"message": "An error occurred while reading the notice."}), 500


# Route for adding a notice
@app.route('/add_notice', methods=['GET', 'POST'])
def add_notice():
    if request.method == 'GET':
        return render_template('notice/add_notice.html')
    
    elif request.method == 'POST':

        notice_data = {}
        for field in notice_model.fields:
            if field == notice_model.file:
                continue
            notice_data[field] = request.form.get(field)

        flag =  False

        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            if upload_to_firebase_storage(file, request.form.get(notice_model.notice_number), storage.notice):     # Call the function to upload the file to Firebase Storage
                notice_data[notice_model.file] = get_file_url(request.form.get(notice_model.notice_number), storage.notice)
                # return jsonify({"message" : 'File uploaded successfully'})
                flag = True
            else:
                return jsonify({"message" : 'An error occurred while uploading the file'}), 500

        if create_document(notice_model.table, notice_data) and flag:
            return jsonify({"message": "Notice created!."}), 201
        else :
            return jsonify({"message": "An error occurred while creating the notice."}), 500
       
    
# --------------------------------------------------------------------------------------------
    

 # --------------------------------------------------------------------------------------------   

# Route for rules and procedures
@app.route('/rules_and_procedures', methods=['GET', 'POST'])
def rules_and_procedures():
    if request.method == 'GET':
        rules_and_procedures_data = read_documents(rules_and_procedures_model.table)
        stats = {
            "rules_and_procedures" : docuemnt_count(rules_and_procedures_model.table)
        }
        return render_template('rules_and_procedures/rules_and_procedures.html', stats=stats, rules_and_procedures_data=rules_and_procedures_data)
   
    elif request.method == 'POST':

        params = {
            rules_and_procedures_model.protocol_number: request.form.get(rules_and_procedures_model.protocol_number)
        }

        rules_and_procedures_data = read_documents(rules_and_procedures_model.table, params)
        return render_template('rules_and_procedures/rules_and_procedures.html',rules_and_procedures_data=rules_and_procedures_data)
    

# Route for rules and procedures
@app.route('/add_rules_and_procedures', methods=['GET', 'POST'])
def add_rules_and_procedures():
    if request.method == 'GET':
        return render_template('rules_and_procedures/add_rules_and_procedures.html')
    elif request.method == 'POST':
        
        rules_and_procedures_data = {}
        for field in rules_and_procedures_model.fields:
            rules_and_procedures_data[field] = request.form.get(field)

        flag = False

        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            if upload_to_firebase_storage(file, request.form.get(rules_and_procedures_model.protocol_number), storage.rules_and_procedures):     # Call the function to upload the file to Firebase Storage
                
                rules_and_procedures_data[rules_and_procedures_data.file] = get_file_url(request.form.get(rules_and_procedures_model.protocol_number), storage.rules_and_procedures)
                # return jsonify({"message" : 'File uploaded successfully'})
                flag = True
            else:
                return jsonify({"message" : 'An error occurred while uploading the file'}), 500


        if create_document(rules_and_procedures_model.table, rules_and_procedures_data) and flag:
            return jsonify({"message": "Rules and Procedures added!."}), 201
        else :
            return jsonify({"message": "An error occurred while adding the Rules and Procedures."}), 500
# --------------------------------------------------------------------------------------------
    
# --------------------------------------------------------------------------------------------

# Route for opportunities
@app.route('/opportunity', methods=['GET', 'POST'])
def opportunities():
    if request.method == 'GET':
        opportunity_data = read_documents(opportunity_model.table)
        stats = {
            "opportunity_count" : docuemnt_count(opportunity_model.table)
        }
        # return opportunity_data
        return render_template('opportunity/opportunity.html', stats=stats, opportunity_data=opportunity_data)
    elif request.method == 'POST':
        
        notice_number = request.form.get(opportunity_model.notice_number)
        param = {
            opportunity_model.notice_number: notice_number
        }
        opportunity_data = read_documents(opportunity_model.table, param)[0]
        # return opportunity_data
        return render_template('opportunity/view_opportunity.html', opportunity_data=opportunity_data)
    
# Route for adding opportunities
@app.route('/add_opportunity', methods=['GET', 'POST'])
def add_opportunities():
    if request.method == 'GET':
        return render_template('opportunity/add_opportunity.html')
    elif request.method == 'POST':
        opportunity_data = {}
        for field in opportunity_model.fields:
            opportunity_data[field] = request.form.get(field)

        if create_document(opportunity_model.table, opportunity_data):
            return render_template('opportunity/opportunity.html')
            # return jsonify({"message": "Opportunity added!."}), 201
        else :
            return jsonify({"message": "An error occurred while adding the opportunity."}), 500
# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# Route for previous year papers
@app.route('/previous_year_papers', methods=['GET', 'POST'])
def previous_year_papers():
    if request.method == 'GET':
        pyqs_data = read_documents(pyq_model.table)
        # return pyqs_data
        stats = {
            "pyq_count" : docuemnt_count(pyq_model.table)
        }
        return render_template('pyq/pyq.html',stats=stats, pyqs_data=pyqs_data)
    
    elif request.method == 'POST':
        params = {}
        for field in pyq_model.fields:
            params[field] = request.form.get(field)

        pyq_data = read_documents(pyq_model.table, params)
        return pyq_data
        # TODO This page will open the pyq pdf or make it aviailable for download
    

# Route for previous year papers
@app.route('/add_previous_year_papers', methods=['GET', 'POST'])
def add_previous_year_papers():
    if request.method == 'GET':
        return render_template('pyq/add_pyq.html')
    
    elif request.method == 'POST':
        pyq_data = {}
        for field in pyq_model.fields:
            pyq_data[field] = request.form.get(field)

        flag = False

        print(pyq_data)

        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            
            file_name = request.form.get(pyq_model.year) + "/" + request.form.get(pyq_model.subject_code) + "/" + request.form.get(pyq_model.exam_type)

            if upload_to_firebase_storage(file, file_name, storage.pyq): # Call the function to upload the file to Firebase Storage
                pyq_data[pyq_model.file] = get_file_url(file_name, storage.pyq)
                # return jsonify({"message" : 'File uploaded successfully'})
                flag = True
            else:
                return jsonify({"message" : 'An error occurred while uploading the file'}), 500


        if create_document(pyq_model.table, pyq_data) and flag:
            return render_template('pyq/pyq.html')
        else :
            return jsonify({"message": "An error occurred while adding the PYQ."}), 500
# --------------------------------------------------------------------------------------------
    


# --------------------------------------------------------------------------------------------
# Route for peer tutoring
@app.route('/peer_tutoring', methods=['GET', 'POST'])
def peer_tutoring():
    if request.method == 'GET':
        peer_tutoring_data = read_documents(peer_tutoring_model.table)
        # return peer_tutoring_data
        stats = {
            "peer_session_count" : docuemnt_count(peer_tutoring_model.table),
        }
        return render_template('peer_tutoring/peer_tutoring.html', stats=stats, peer_tutoring_data=peer_tutoring_data)
    else :
        params = {
            peer_tutoring_model.student_mentor_roll: request.form.get(peer_tutoring_model.student_mentor_roll),
            peer_tutoring_model.teacher_incharge_roll: request.form.get(peer_tutoring_model.teacher_incharge_roll),
            peer_tutoring_model.date: request.form.get(peer_tutoring_model.date),
            peer_tutoring_model.time: request.form.get(peer_tutoring_model.time),
            peer_tutoring_model.subject: request.form.get(peer_tutoring_model.subject),
            peer_tutoring_model.description: request.form.get(peer_tutoring_model.description)
        }


        peer_tutoring_data = read_documents(peer_tutoring_model.table, params)[0]
        print(peer_tutoring_data)
        return render_template('peer_tutoring/view_peer_tutoring.html', peer_tutoring_data=peer_tutoring_data)
# --------------------------------------------------------------------------------------------


# API endpoint to retrieve attendance
@app.route('/attendance', methods=['POST'])
def attendance():
    data = request.get_json()
    if not check_profile_picture_exists(data['username']):
        store_profile_pic(data['username'], data['password'])
        
    return get_attendance(data['username'], data['password'])

# API endpoint to retrieve timetable
@app.route('/timetable', methods=['POST'])
def timetable():
    data = request.get_json()
    return get_timetable(data['username'], data['password'])


# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
    