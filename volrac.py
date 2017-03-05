from flask import Flask, render_template, request

import os
import settings
from flask_mail import Mail

app = Flask(__name__)

@app.route('/')
def index():
	message = "Trust me, I'm a coder."
	return render_template('index.html', message=message)

def about():
	return render_template('about.html')

def contact():
	if request.method == 'POST':
		
		contact_msg = request.form['message']
		msg = Message(contact_msg,recipients=[settings.RECEIVER_EMAIL])

		mail = Mail(app)
		mail.send(msg)

	return render_template('contact')

if __name__ == "__main__":
	app.run(host='0.0.0.0')