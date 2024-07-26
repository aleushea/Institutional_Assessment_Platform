from flask import Blueprint, request, jsonify
from .models import db, Question

Add_question_bp = Blueprint('Add_question', __name__)

@Add_question_bp.route('/Add_question', methods=['POST'])
def Add_question():
    question_text = request.form['question']
    choices = [request.form['choice1'], request.form['choice2'], request.form['choice3'], request.form['choice4']]
    correct_answer = int(request.form[' correct_answer'])

    new_question = Question(question=question_text, choice1=choices[0], choice2=choices[1], choice3=choices[2], choice4=choices[3],  correct_answer= correct_answer)

    db.session.add(new_question)
    db.session.commit()

    return "Question inserted successfully!"
