from flask import Flask, render_template, request, flash, session

import os
import settings
import random
import string

from hashlib import sha512
from flask_mail import Mail, Message

SIMPLE_CHARS = string.ascii_letters + string.digits

def get_random_string(length=24):
    return ''.join(random.choice(SIMPLE_CHARS) for i in xrange(length))

def get_random_hash(length=24):
    hash = sha512()
    hash.update(get_random_string())
    return hash.hexdigest()[:length]

app = Flask(__name__)

app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = get_random_hash()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token 

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
    app.run(host='0.0.0.0')