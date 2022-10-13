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
    """ Displays survey start page """

    return render_template("survey_start.html",
        title=survey.title,
        instructions=survey.instructions)


@app.post("/begin")
def start_survey():
    """ """

    return redirect('/question/0')


@app.get("/question/<int:question_id>")
def generate_question(question_id):
    """ """


    return render_template("question.html",
        question = survey.questions[question_id],  id = question_id)


@app.post("/answer")
def answer_question():
    """  """
    answer = request.form['answer']
    question_id = int(request.form['id'])

    responses.append(answer)

    return redirect(f'/question/{question_id+1}')









