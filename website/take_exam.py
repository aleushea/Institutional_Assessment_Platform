from flask import Blueprint, request, jsonify
from .models import db, Exam

take_Exam = Blueprint('exam', __name__)

@take_Exam.route('/submit_exam', methods=['POST'])
def submit_exam():
    user_full_name = request.json.get('user_full_name')
    stud_ans = request.json.get('stud_ans')
    question_id = request.json.get('question_id')

    # Update the user's answer in the Exam table
    exam = Exam.query.get(question_id)
    exam.stud_ans = stud_ans
    db.session.commit()

    return jsonify({'message': 'Exam submitted successfully'})

@take_Exam.route('/get_exam_result/<int:question_id>', methods=['GET'])
def get_exam_result(question_id):
    # Retrieve exam result for a specific question
    exam = Exam.query.get(question_id)
    if not exam:
        return jsonify({'error': 'Exam result not found'}), 404

    return jsonify({'user_full_name': exam.user_full_name, 'stud_ans': exam.stud_ans})

@take_Exam.route('/calculate_score', methods=['GET'])
def calculate_score():
    # Calculate the score based on the correct answers
    total_questions = Exam.query.count()
    correct_answers = Exam.query.filter_by(correct_ans=Exam.stud_ans).count()
    score = (correct_answers / total_questions) * 100

    return jsonify({'total_questions': total_questions, 'correct_answers': correct_answers, 'score': score})

@take_Exam.route('/delete_exam/<int:question_id>', methods=['DELETE'])
def delete_exam(question_id):
    exam = Exam.query.get(question_id)
    if not exam:
        return jsonify({'error': 'Exam result not found'}), 404

    db.session.delete(exam)
    db.session.commit()

    return jsonify({'message': 'Exam result deleted successfully'})