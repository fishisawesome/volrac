from flask import Flask, render_template, request, flash, session, redirect, jsonify

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

@app.route('/read')
def read():
    return redirect("//thegreat.volrac.net", code=302)

@app.route('/spotify')
def spotify():
    if not 'username' in request.args and not 'code' in request.args:
        return render_template('spotify_form.html')

    import music_taste_over_time as mtot

    session_key = '_volrac_sp_username'
    if 'username' in request.args:
        username = request.args.get('username')
        session[session_key] = username
    else:
        username = session[session_key] if session_key in session else 'carlo.villamayor'

    token = mtot.get_sp_token(username)
    
    if not token:

        if not 'code' in request.args:
            auth_url = mtot.get_auth_url(username)
            return redirect(auth_url)
        else:
            sp_code = request.args.get('code')
            token = mtot.get_token_from_code(username, sp_code)

    #tracks = mtot.get_top_tracks(token, request.args.get('time_range'))

    ranges = ['short_term', 'medium_term', 'long_term']
    tracks = {}
    titles = {}
    for r in ranges:
        tracks[r] = mtot.get_top_tracks(token, time_range=r)
        tracks[r] = tracks[r]['items']
        # Add titles and artist name
        titles[r] = [s['name'] + ' - ' + s['artists'][0]['name'] for s in tracks[r]]
        # Add track Spotify id
        tracks[r] = [s['id'] for s in tracks[r]]

    commons = list( set(tracks['long_term']).intersection(set(tracks['medium_term'])).intersection(set(tracks['short_term'])) )

    favorites = []
    for c in commons:
        favorites.append(mtot.get_track_info(c))

    return render_template('spotify_favorites.html', favorites=favorites, titles = titles)

if __name__ == "__main__":
    app.run(host='0.0.0.0')