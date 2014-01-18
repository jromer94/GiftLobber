from flask import Flask, render_template, request
app = Flask(__name__)
contacts = {}
jobs = {}

@app.route('/?contact')

def listContacts():
    return contacts


@app.route('/?job')

def listJobs():
    return jobs


@app.route('/')

def home():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run('0.0.0.0' , debug=True)
