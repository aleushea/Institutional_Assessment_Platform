from flask import Blueprint, render_template
from .models import Question

exam_page_bp = Blueprint('exam_page', __name__)

@exam_page_bp.route('/exam_question', methods=['GET', 'POST'])
def display_exam_question():
    question = Question.query.first()  # Retrieve the first question from the database for demonstration
    return render_template('exam_question.html', 
                           question_text=question.question_text,
                           choice1=question.choice1,
                           choice2=question.choice2,
                           choice3=question.choice3,
                           choice4=question.choice4)