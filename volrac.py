from flask import Flask, render_template, request

import os
import settings

app = Flask(__name__)

@app.route('/')
def index():
	message = "Trust me, I'm a coder."
	return render_template('index.html', message=message)

def about():
	return render_template('about.html')

def contact():
	return render_template('contact')

if __name__ == "__main__":
	app.run(host='0.0.0.0')