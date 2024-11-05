
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


from joblib import load
model = load('fintech.joblib')

from flask import request
import pandas as pd

@app.route("/fintech")
def fintech():
    """ Calculating the model and taking decision """
    # dictionary with list object in values
    data = {
        'time_on_books' : [request.args["time_on_books"]],
        'total_paid_last_12_months' : [request.args["total_paid_last_12_months"]],
        'total_debt_in_arrears' : [request.args["total_debt_in_arrears"]],
    }

    # creating a Dataframe object
    X = pd.DataFrame(data)

    # predict
    prob_paying = model.predict_proba(X)[:,1]

    if(prob_paying > 0.7):
        message = "Your probability of repaying is {}, so your credit has been approved!".format(prob_paying)
    else:
        message = "Your probability of repaying is low, so your credit has been rejected!".format(prob_paying)

    return render_template("index.html", message=message)





