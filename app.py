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

    session['responses'] = []

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
    # breakpoint()

    questions = survey.questions

    current_question_id = len(session['responses'])


    question = questions[question_id] if \
        (question_id == current_question_id) \
        else None

    # if trying to access invalid question
    if not question:
        flash('Accessing an invalid question!')

        return redirect(f'/question/{current_question_id}')


    return render_template(
        "question.html",
        question = question)



@app.post("/answer")
def answer_question():
    """ Redirects user to next question (or completion page),
     appends responses list """

    answer = request.form['answer']

    # cookie session storage
    responses = session['responses']
    responses.append(f'{answer}')
    session['responses'] = responses

    next_question_id = len(responses)

    if next_question_id == len(survey.questions):
        return redirect("/completion")

    return redirect(
        f"/question/{next_question_id}")

@app.get("/completion")
def complete_survey():
    """ Returns html of completion page with questions/responses """

    responses = session['responses']

    return render_template(
        "completion.html",
        questions=survey.questions,
        responses=responses)



