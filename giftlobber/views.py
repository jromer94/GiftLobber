from giftlobber import app
from flask import render_template, request, flash, session, redirect, url_for
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient


client = MongoClient('mongodb://admin2:admin@linus.mongohq.com:10015/GiftLobber')
client = client.GiftLobber

@app.route('/contacts', methods=['GET','POST'])
def manageContacts():
    if request.method == "POST":
        #add address data to contacts
        pass
    
    return render_template('manageContacts.html')

@app.route('/gifts',methods=['GET','POST'])
def manageGifts():
    if request.method == "POST":
        #add gift data jobs
        pass
    return render_template('manageGifts.html')
    
@app.route('/getContactByLastName/<name>')
def queryName(name):
    results = client.tasks.find({'last':name})
    return results
    
@app.route('/getGiftByDate/<date>')
def queryDate(date):
    result = client.tasks.find({'date':date})
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    print session.get('logged_in')
    if session.get('logged_in') == None:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        button = request.form["submit"]
        print button
        if button == "Manage Contacts":
            return redirect(url_for('manageContacts'))
        elif button == "Manage Gifts":
            return redirect(url_for('manageGifts'))
    
    else:
        return render_template('management.html')
    
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
        lobURI='https://api.lob.com/v1/addresses/?'
        lobURI+='name='
        lobURI+=request.form['first']
        lobURI+=''
        lobURI+=request.form['last']
        lobURI+='&address_line1='
        lobURI+=request.form['address1']
        lobURI+='&address_line2='
        lobURI+=request.form['address2'],
        lobURI+='&address_city='
        lobURI+=request.form['city']
        lobURI+='&address_state='
        lobURI+=request.form['state']
        lobURI+='&address_zip='
        lobURI+=request.form['zip']
        lobURI+='&address_country=US'
        
        client.contacts.insert({
            "first": request.form['first'],
            "last": request.form['last'],
            "address1": request.form['address1'],
            "address2": request.form['address2'],
            "city": request.form['city'],
            "state": request.form["state"],
            "zip": request.form["zip"],
            "country": "US"
            })
    
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
