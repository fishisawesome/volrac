from flask import Flask, render_template, request, flash

import os
import settings
from flask_mail import Mail, Message

app = Flask(__name__)

@app.route('/')
def index():
	message = "Trust me, I'm a coder."
	return render_template('index.html', message=message)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		
		contact_sender = request.form['email']
		contact_msg = request.form['message']
		msg = Message(subject="Volrac contact form",
					  body=contact_msg,
					  sender=contact_sender,
					  recipients=[settings.RECEIVER_EMAIL])

		mail = Mail(app)
		mail.send(msg)

		flash('Message successfully sent to the trustworthy coder.', 'success')

	return render_template('contact.html')

if __name__ == "__main__":
	app.secret_key = settings.SECRET_KEY
	app.config['SESSION_TYPE'] = 'filesystem'

	#app.debug = True
	app.run(host='0.0.0.0')