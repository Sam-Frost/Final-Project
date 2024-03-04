from flask import Flask, jsonify, redirect, render_template, request, url_for
from firebase import create_document, read_documents

from models import student_model, notice_model, faculty_model, peer_tutoring_model, pyq_model, opportunity_model, rules_and_procedures_model

# Create the Flask application
app = Flask(__name__)

# TODO : Add checks whenever adding data, if the data already exists!

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
        return render_template('admin_dashboard.html')
    elif request.method == 'POST':
        return 'This is a POST request to the notices page.'
    


# --------------------------------------------------------------------------------------------
# Route for viewing students
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        # Reading all studetns from the database and printing on webpage
        student_data = read_documents(student_model.table)
        return student_data
        # return render_template('students/students.html')
    
    elif request.method == 'POST':
        # Retrieve student data from the database based on the roll number and display it on the webpage
        student_roll = request.form.get(student_model.student_roll)
        
        params = {
            student_model.student_roll: student_roll
        }

        student_data = read_documents(student_model.table, params)

        if student_data:
            return student_data
            # return render_template('students/view_student.html', student_data=student_data[0])
        else :
            return jsonify({"message": "An error occurred while reading the student."}), 500
        
# Route for adding students
@app.route('/add_students', methods=['GET', 'POST'])
def add_students():
    if request.method == 'GET':
        return render_template('students/add_student.html')
    
    elif request.method == 'POST':
        student_data = {}
        for field in student_model.fields:
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
        return faculty_data
        # return render_template('faculty/faculty.html')
    
    elif request.method == 'POST':
        # Retrieve student data from the database based on the roll number and display it on the webpage
        faculty_roll = request.form.get(faculty_model.faculty_roll)
        
        params = {
            faculty_model.faculty_roll: faculty_roll
        }

        faculty_data = read_documents(faculty_model.table, params)

        if faculty_data:
            return faculty_data[0]
            # return render_template('faculty/view_faculty.html', faculty_data=faculty_data[0])
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
            faculty_data[field] = request.form.get(field)

        if create_document(faculty_model.table, faculty_data):
            return jsonify({"message": "Faculty record created!."}), 201
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
        return notice_data
        # return render_template('notice/notices.html', notice_data=notice_data)
    
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
            
            # TODO HANDLE THE CASE OF STORING THE ACTUAL FILE

            notice_data[field] = request.form.get(field)

        if create_document(notice_model.table, notice_data):
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
        return render_template('rules_and_procedures/rules_and_procedures.html',rules_and_procedures_data=rules_and_procedures_data)
   
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

        # TODO hanle the actual file

        if create_document(rules_and_procedures_model.table, rules_and_procedures_data):
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
        return opportunity_data
        # return render_template('opportunity/opportunities.html', opportunity_data=opportunity_data)
    elif request.method == 'POST':
        
        notice_number = request.form.get(opportunity_model.notice_number)
        param = {
            opportunity_model.notice_number: notice_number
        }
        opportunity_data = read_documents(opportunity_model.table, param)

        return opportunity_data
        # return render_template('opportunity/opportunity.html', opportunity_data=opportunity_data)
    
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
            return jsonify({"message": "Opportunity added!."}), 201
        else :
            return jsonify({"message": "An error occurred while adding the opportunity."}), 500
# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# Route for previous year papers
@app.route('/previous_year_papers', methods=['GET', 'POST'])
def previous_year_papers():
    if request.method == 'GET':
        pyqs_data = read_documents(pyq_model.table)
        return pyqs_data
        # return render_template('pyq/pyqs.html', pyqs_data=pyqs_data)
    
    elif request.method == 'POST':
        params = {}
        for field in pyq_model.fields:
            params[field] = request.form.get(field)

        # TODO Add the code to read the pdf file for firestore storage

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
            
            # TODO HANDLE THE CASE OF STORING THE ACTUAL FILE
            # if field == pyq_model.file_name:

            #     if pyq_model.file_name not in request.files:
            #         return jsonify({"mesage":'No file uploaded'}), 400

            #     pdf_file = request.files['pdf_file']

            #     # Save the file to the server or process it as needed
            #     # TODO Save in firebase stoage
            #     pdf_file.save('uploaded_file.pdf')
            #     pyq_data[field] = request.form.get(field)
            #     continue

            pyq_data[field] = request.form.get(field)

        if create_document(pyq_model.table, pyq_data):
            return jsonify({"message": "PYQ added!."}), 201
        else :
            return jsonify({"message": "An error occurred while adding the PYQ."}), 500
# --------------------------------------------------------------------------------------------
    


# --------------------------------------------------------------------------------------------
# Route for peer tutoring
@app.route('/peer_tutoring', methods=['GET'])
def peer_tutoring():
    if request.method == 'GET':
        peer_tutoring_data = read_documents(peer_tutoring_model.table)
        return peer_tutoring_data
        # return render_template('peer_tutoring/peer_tutoring.html', peer_tutoring_data=peer_tutoring_data)
# --------------------------------------------------------------------------------------------


# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
    