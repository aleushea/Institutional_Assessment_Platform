from flask import Blueprint, request, jsonify
from .models import db, Exam

question_bp = Blueprint('question', __name__)

@question_bp.route('/insert_question', methods=['POST'])
def insert_question():
    question = request.json.get('question')
    correct_ans = request.json.get('correct_ans')

    new_question = Exam(question=question, correct_ans=correct_ans)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question inserted successfully'})

@question_bp.route('/update_questionquestion_bp/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Exam.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    new_question = request.json.get('question')
    new_correct_ans = request.json.get('correct_ans')

    question.question = new_question
    question.correct_ans = new_correct_ans

    db.session.commit()

    return jsonify({'message': 'Question updated successfully'})

@question_bp.route('/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Exam.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({'message': 'Question deleted successfully'})