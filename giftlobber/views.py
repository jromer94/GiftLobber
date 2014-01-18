from giftlobber import app
from flask import render_template, request

contacts = {}
jobs = {}

@app.route('/?contact')
def listContacts():
    return contacts


@app.route('/?job')
def listJobs():
    return jobs
    

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
