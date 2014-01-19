from giftlobber import app

from flask import render_template, request, flash, session, redirect, url_for
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

from datetime import datetime
from threading import Timer

import helpers

client = MongoClient('mongodb://admin2:admin@linus.mongohq.com:10015/GiftLobber')
client = client.GiftLobber

x=datetime.today()
y=x.replace(day = x.day+1,hour = 2, minute = 0, microsecond = 0)
delta_t = y-x
secs = delta_t.seconds+1

def run():
    for contact in client.contacts:
        for gift in contact.gifts:
            if datetime.date(gift[date]) == datetime.today()-5:
                values = {
                    "name":gift['name'],
                    "to":contact['addressID'],
                    "from":client.account["account_address"],
                    "front":"/static/dist/pdfs/"+gift['front'],
                    "back":gift['message']
                }
                postcard = helpers.lobPost('https://api.lob.com/v1/postcards', values, 'test_814e892b199d65ef6dbb3e4ad24689559ca')
                values = {
                    "name":gift['name'],
                    "to":contact['addressID'],
                    "from":client.account["account_address"],
                    "object1":postcard,
                    "object2":gift['check']
                }
                call = helpers.lobPost('https://api.lob.com/v1/jobs', values, 'test_814e892b199d65ef6dbb3e4ad24689559ca')
        

t=Timer(secs,run)
t.start()

    
def addCheck(amount, first, last):
    if request.method == 'POST':
        for contact in client.contacts.find():
            if contact['first']==first and contact['last'] == last:
                giftee = contact
                values = {
                    'bank_account':client.account.find_one({'user': session.get('user')})['account_id'],
                    'to':giftee['addressId'],
                    'amount':amount
                    }
        check=helpers.lobPost('https://api.lob.com/v1/checks', values, 'test_814e892b199d65ef6dbb3e4ad24689559ca')
        return check


@app.route('/sendGift')
def sendGift():
    contacts = client.contacts
    for contact in contacts.find():
        for gift in contact['gifts']:
            values = {
                "name":gift['name'],
                "to": contact['addressId'],
                "from":client.account.find_one({'user': session.get('user')})["account_address"],
               # "front":"https://github.com/jromer94/GiftLobber/blob/master/giftlobber/static/dist/pdfs/A.pdf?raw=true",
                "back": client.gifts.find_one({"title": gift['name']})['message']
            }
            postcard = helpers.lobPost('https://api.lob.com/v1/postcards', values, 'test_814e892b199d65ef6dbb3e4ad24689559ca')
            addCheck(gift['check'], contact['first'], contact['last'])

@app.route('/contacts', methods=['GET','POST'])
def manageContacts():
    if request.method == "POST":
        #add address data to contacts
        pass
    contacts = client.contacts.find({'user': session.get('user')})
    return render_template('manageContact.html', contacts = contacts)

@app.route('/gifts',methods=['GET','POST'])
def manageGifts():
    if request.method == "POST":
        #add gift data jobs
        pass
    gifts = client.gifts.find({'user': session.get('user')})
    return render_template('manageGift.html', gifts = gifts)

@app.route('/payment',methods=['GET','POST'])
def managePayment():
    if request.method == 'POST':
        values = {
            'routing_number': request.form['routing_number'],
            'account_number': request.form['account_number'],
            'bank_code':request.form['routing_number'],
            'bank_address[name]': request.form['bank_name'],
            'bank_address[address_line1]': request.form['bank_address1'],
            'bank_address[address_city]': request.form['bank_city'],
            'bank_address[address_state]': request.form['bank_state'], 
            'bank_address[address_zip]': request.form['bank_zip'], 
            'bank_address[address_country]': "US",
            'account_address[name]': request.form['first']+request.form['last'],
            'account_address[address_line1]': request.form['address1'],
            'account_address[address_line2]': request.form['address2'],
            'account_address[address_city]': request.form['city'],
            'account_address[address_state]': request.form['state'],
            'account_address[address_zip]': request.form['zip'],
            'account_address[address_country]': "US"
        }
        print values
        account = helpers.lobPost('https://api.lob.com/v1/bank_accounts', values, 'test_814e892b199d65ef6dbb3e4ad24689559ca')
        print account
        client.account.insert({
            "user": session.get('user'),
            "account_id":account["id"],
            "account_address":account["account_address"]
            })
            
        redirect(url_for('index'))
    return render_template('addAccount.html')

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
        elif button == "Manage Payment":
            return redirect(url_for('managePayment'))
    
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
	print "test1i"
        values = {'name': request.form['first'] + " " + request.form['last'],
            'address_line1': request.form['address1'],
            'address_line2': request.form['address2'],
            'address_city': request.form['city'],
            'address_state': request.form['state'],
            'address_zip': request.form['zip'], 
            'address_country': "US"}
	print "test2"
        address = helpers.lobPost('https://api.lob.com/v1/addresses', values, 'test_814e892b199d65ef6dbb3e4ad24689559ca')
        client.contacts.insert({
            "user": session.get('user'),
            "first": request.form['first'],
            "last": request.form['last'],
            "address1": request.form['address1'],
            "address2": request.form['address2'],
            "city": request.form['city'],
            "state": request.form["state"],
            "zip": request.form["zip"],
            "country": "US",
            "addressId": address['id'],
            "gifts": [] 
            })
        return redirect(url_for('manageContacts'))
    
    return render_template('editContact.html')

@app.route('/gifts/add', methods=['GET', 'POST'])
def addGift():
    if request.method == 'POST':
        client.gifts.insert({
           "title": request.form['title'],
           "message": request.form['message'],
           "front": request.form['option1'],
           "user": session.get('user')
        })
        return redirect(url_for('manageGifts'))

    return render_template('editGift.html')

@app.route('/contacts/select', methods=['GET' , 'POST'])
def selectGift():
    if request.method == 'POST':
        gifts = client.contacts.find_one({'first':request.args.get("first", "")
 , 'last': request.args.get("last", "") })['gifts']
	print "test"
        gifts.append({
            "name": request.form["name"],
            "date": request.form['date'],
            "check": request.form['check']})
        
	client.contacts.update({
        'first':request.args.get("first", ""),
        'last': request.args.get("last", "") },
        {'$set': {'gifts': gifts  }
        })
	print "test"
        return redirect(url_for('manageContacts'))

    first = request.args.get("first", "")
    last = request.args.get("last", "")
    gifts = client.gifts.find({'user': session.get('user')})
    return render_template('giftSelect.html', first = first, last = last, gifts = gifts)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
