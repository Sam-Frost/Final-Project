from flask import Blueprint, jsonify, request, session

from firebase import check_profile_picture_exists, create_document, get_file_url, read_documents, upload_to_firebase_storage

from models import student_model, faculty_model, peer_tutoring_model, notice_model, rules_and_procedures_model, opportunity_model, pyq_model, digil_model
from web_scraper.academics import get_attendance, get_timetable, store_profile_pic

import storage

api = Blueprint('api', __name__)



# API endpoint to retrieve attendance
@api.route('/attendance', methods=['POST'])
def attendance():
    data = request.get_json()
    if not check_profile_picture_exists(data['username']):
        store_profile_pic(data['username'], data['password'])
        
    return get_attendance(data['username'], data['password'])

# API endpoint to retrieve timetable
@api.route('/timetable', methods=['POST'])
def timetable():
    data = request.get_json()
    return get_timetable(data['username'], data['password'])

@api.route('/student_profile', methods=['POST'])
def student_profile():

    data = request.json
    roll_number = data['roll_number']

    params = {
        student_model.student_roll : roll_number
    }

    student_profile = read_documents(student_model.table, params)

    if student_profile:
        student_profile = student_profile[0]
        return jsonify(student_profile)
    else:
        return jsonify({"error": "Student not found"}), 404
        

@api.route('/faculty_profile', methods=['GET'])
def faculty_profile():
    faculty_profiles = read_documents(faculty_model.table)
    if faculty_profiles:
        return jsonify(faculty_profiles)
    else:
        return jsonify({"error": "Faculty not found"}), 404

    
@api.route('/peer_tutoring', methods=['POST'])
def peer_tutoring():
    data = request.json
    peer_tutoring_data = {}
    for field in peer_tutoring_model.fields:
        if field == peer_tutoring_model.department:
            continue
        peer_tutoring_data[field] = data[field]

    # Get the department of studeent using roll number
    param = {
        student_model.student_roll: data[peer_tutoring_model.student_mentor_roll]
    }
    student_data = read_documents(student_model.table, param)[0]
    peer_tutoring_data[peer_tutoring_model.department] = student_data[student_model.department]

    if create_document(peer_tutoring_model.table, peer_tutoring_data):
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failure"}), 500
    
@api.route('/peer_tutoring_list', methods=['POST'])
def peer_tutoring_list():

    # Recive the roll  number
    data = request.json
    roll_number = data['roll_number']
    
    # Get the department of studeent using roll number
    param = {
        student_model.student_roll: roll_number
    }
    student_data = read_documents(student_model.table, param)[0]
    department = student_data[student_model.department]

    # get all the peer tutoring sessions for that department
    param = {
        peer_tutoring_model.department: department
    }

    peer_tutoring_sessions = read_documents(peer_tutoring_model.table, param)

    if peer_tutoring_sessions:
        return jsonify(peer_tutoring_sessions)
    else:
        return jsonify({"error": "No peer tutoring sessions found"}), 404
    

@api.route('/notices', methods=['POST'])
def create_notice():
    notices = read_documents(notice_model.table)

    if notices:
        return jsonify(notices)
    else:
        return jsonify({"error": "No opportunities found"}), 404

@api.route('/rules_and_procedures', methods=['GET'])
def get_rules_and_procedures():
    rules_and_procedures = read_documents(rules_and_procedures_model.table)

    if rules_and_procedures:
        return jsonify(rules_and_procedures)
    else:
        return jsonify({"error": "No opportunities found"}), 404


@api.route('/opportunities', methods=['GET'])
def get_opportunities():
    opportunities = read_documents(opportunity_model.table)

    if opportunities:
        return jsonify(opportunities)
    else:
        return jsonify({"error": "No opportunities found"}), 404
    
@api.route('/pyq', methods=['POST'])
def pyq():

    # Recive the roll  number
    data = request.json
    year = data['year']
    programme = data['programme']
    department = data['department']
    
    # Get the department of studeent using roll number
    param = {
        pyq_model.programme : programme,
        pyq_model.year :  year,
        pyq_model.department : department
    }

    pyq_dta = read_documents(pyq_model.table, param)

    if pyq_dta:
        return jsonify(pyq_dta)
    else:
        return jsonify({"error": "No peer tutoring sessions found"}), 404
    

# 1.⁠ ⁠To get the documents
# POST REQUEST (DigiLoc):
# Request Body : 
# { roll_number, category}
# —————————————————
# 2.⁠ ⁠To upload the documents
# POST REQUEST BODY :
# { roll_number, category, fill_name, file}


@api.route('/getDocuments', methods=['POST'])
def getDocuments():
    if request.method == 'POST':

        data = request.json
        roll_number = data['roll_number']
        category = data['category']

        params = {
            digil_model.roll_number : roll_number,
            digil_model.category: category
        }

        documents = read_documents(digil_model.table, params)

        if documents:
            return jsonify(documents)
        else:
            return jsonify({"error": "Document not found"}), 404

@api.route('/uploadDocument', methods=['POST'])
def uploadDocument():
    if request.method == 'POST':

        data = request.json

        document_data = {}

        for field in digil_model.fields:
            if field == digil_model.file:
                continue
            document_data[field] = data[field]

        flag =  False

        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            if upload_to_firebase_storage(file, request.form.get(digil_model.fill_name), storage.digilocker): # Call the function to upload the file to Firebase Storage
                document_data[digil_model.file] = get_file_url(request.form.get(digil_model.fill_name), storage.digilocker)
                # return jsonify({"message" : 'File uploaded successfully'})
                flag = True
            else:
                return jsonify({"message" : 'An error occurred while uploading the file'}), 500

        if create_document(digil_model.table, document_data) and flag:
            return jsonify({"message": "Document added!."}), 201
        else :
            return jsonify({"message": "An error occurred while creating the notice."}), 500

        # TODO - how to handle file sent in post requst


