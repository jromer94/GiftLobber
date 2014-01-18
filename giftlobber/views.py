from giftlobber import app
from flask import render_template, request
from flask.ext.pymongo import PyMongo


client = MongoClient('mongodb://admin:admin@linus.mongohq.com:10015/GiftLobber')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    
    return render_template('landing2.html')   
