from flask import Blueprint, jsonify, request, session

from firebase import create_document, read_documents

from models import student_model, faculty_model, peer_tutoring_model, notice_model, rules_and_procedures_model, opportunity_model

api = Blueprint('api', __name__)


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