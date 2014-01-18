
from giftlobber import app
from flask import render_template




@app.route('/', methods=['GET', 'POST'])
def index():
	return "lol";



