from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/insert_question', methods=['POST'])
def insert_question():
    question = request.form['question']
    choices = [request.form['choice1'], request.form['choice2'], request.form['choice3'], request.form['choice4']]
    answer = int(request.form['answer'])

    # Add code to insert the question, choices, and answer into your database here

    return "Question inserted successfully!"

if __name__ == '__main__':
    app.run(debug=True)