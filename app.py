from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def show_start_page():
    """ Returns html of survey start page """

    return render_template("survey_start.html",
        title=survey.title,
        instructions=survey.instructions)



@app.post("/begin")
def start_survey():
    """ Redirects user to first question in survey """

    return redirect('/question/0')


@app.get("/question/<int:question_id>")
def generate_question(question_id):
    """ Returns html for each question """

    return render_template("question.html",
        question = survey.questions[question_id],  id = question_id)



@app.post("/answer")
def answer_question():
    """ Redirects user to next question (or completion page), appends responses list """

    answer = request.form['answer']
    question_id = int(request.form['id'])

    responses.append(answer)

    if question_id == len(survey.questions) - 1:
        return redirect("/completion")

    return redirect(f'/question/{question_id+1}')



@app.get("/completion")
def complete_survey():
    """ Returns html of completion page with questions/responses """

    return render_template("completion.html",
        questions=survey.questions,
        responses=responses)






