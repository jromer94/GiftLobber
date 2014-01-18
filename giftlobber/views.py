from giftlobber import app
from flask import render_template, request, flash, session, redirect, url_for
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import helpers

client = MongoClient('mongodb://admin2:admin@linus.mongohq.com:10015/GiftLobber')
client = client.GiftLobber

@app.route('/contacts')
def listContacts():
    results = ''
    return client.contacts


@app.route('/?job')
def listJobs():
    results = ''
    return client.jobs
    
@app.route('/getContactByLastName/<name>')
def queryName(name):
    results = ''
    for aName in client.tasks.find({'last':name}):
        print aName
        results += str(aName)
    return 'name: '+ name+ "\n"+ results
    
@app.route('/getGift/<date>')
def queryTask(task):
    results = ''
    for subTask in client.tasks.find({'date':date}):
        results += str(subTask)
    return 'task: '+ task + "\n" + results

@app.route('/', methods=['GET', 'POST'])
def index():
    print session.get('logged_in')
    if session.get('logged_in') == None:
        return redirect(url_for('login'))


    return render_template('management.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print request.form['username']
        user = client.users.find_one({
            'name': request.form['username']
            })
        print user
        if user and user['pass'] == request.form['pass']:
            session['logged_in'] = True
            session['user'] = user['name']
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            flash('Incorrect login info')
 
    return render_template('landing2.html')   

@app.route('/contacts/add', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        values = {'name': request.form['first'] + " " + request.form['last'],
            'address_line1': request.form['address1'],
            'address_line2': request.form['address2'],
            'address_city': request.form['city'],
            'address_zip': request.form['zip'], 
            'address_country': "US"}
        address = helpers.lobPost('https://test_814e892b199d65ef6dbb3e4ad24689559ca:@api.lob.com/v1/addresses/', values)
        client.contacts.insert({
            "first": request.form['first'],
            "last": request.form['last'],
            "address1": request.form['address1'],
            "address2": request.form['address2'],
            "city": request.form['city'],
            "state": request.form["state"],
            "zip": request.form["zip"],
            "country": "US",
            "addressId": address['id']
            })
        return redirect(url_for('index'))
    
    return render_template('addContact.html')

@app.route('/gifts/add', methods=['GET', 'POST'])
def addGift():
    if request.method == 'POST':
        client.gifts.insert({
            "title": request.form['title'],
            "message": request.form['message'],
            "front": request.form['front']
            })
        return redirect(url_for('listGifts') )

    return render_template('addGift.html')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
