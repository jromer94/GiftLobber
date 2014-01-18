from giftlobber import app
from flask import render_template, request, flash, session, redirect, url_for
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient


client = MongoClient('mongodb://admin2:admin@linus.mongohq.com:10015/GiftLobber')
client = client.GiftLobber
contacts = {}
jobs = {}

@app.route('/contacts')
def listContacts():
    return "temp"


@app.route('/?job')
def listJobs():
    return jobs
    

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
	print request.form['username']
   	user = client.users.find_one({'name': request.form['username']})
        print user
        if user and  user['pass'] == request.form['pass']:
            session['logged_in'] = True
            session['user'] = user['name']
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            flash('Incorrect login info')
 
    return render_template('landing2.html')   

@app.route('/contacts/add', methods['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        client.contacts.insert({"first": request.form['first'],
            "last": request.form['last'],
            "address1": request.form['address1'],
            "address2": request.form['address2'],
            "city": request.form['city'],
            "state": request.form["state"],
            "zip": request.form["zip"],
            "country": "US"})
        return redirect(url_for('index')    

    return render_template('addContact.html')

@app.route('/gifts/add', methods['GET', 'POST'])
def addGift():
    if request.method == 'POST':
        client.gifts.insert({"title": request.form['title'],
            "message" = request.form['message'],
            "front" = request.form['front']})
        return redirect(url_for('listGifts') 

    return render_template('addGift.html')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
