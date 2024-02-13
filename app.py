from flask import Flask, request, render_template, redirect, flash, make_response
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
responses = []

@app.route("/", methods=["POST","GET"])
def home():
    return render_template("home.html")

@app.route("/question/<int:question_num>", methods=['POST','GET'])
def question(question_num):

    if question_num == 0:
        survey = request.form['surveyselection']
        question = surveys[survey].questions[question_num]
        res = make_response(render_template("question.html", question=question, question_num=question_num, survey=survey))
        res.set_cookie('surveyselection', survey)
        return res
    
    survey = request.cookies.get('surveyselection')

    if (len(responses) == len(surveys[survey].questions)):
        return redirect("/complete")

    if (len(responses) != question_num):
        flash(f"Invalid question id: {question_num}.")
        return redirect(f"/question/{len(responses)}")

    survey = request.cookies.get('surveyselection')
    question = surveys[survey].questions[question_num]
    return render_template("question.html", question=question, question_num=question_num, survey=survey)

@app.route("/answer", methods=['POST','GET'])
def answer():
    answer = request.form["answer"]
    responses.append(answer)

    if (len(responses) == len(surveys[request.cookies.get('surveyselection')].questions)):
       
        return redirect("/complete")

    else:
        return redirect(f"/question/{len(responses)}")
    
@app.route("/complete")
def finished():
    
    return render_template("complete.html")